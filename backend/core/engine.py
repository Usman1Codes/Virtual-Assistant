from sqlalchemy.orm import Session
from . import models
from services import email_service, ai_service, sheets_service

def process_one_email(db: Session):
    """
    This is the core engine of the virtual assistant.
    It fetches one unread email, processes it, and sends a reply.
    """
    # 1. Fetch the latest unread email
    unread_emails = email_service.fetch_emails(max_results=1)
    if not unread_emails or "error" in unread_emails:
        print("Engine: No unread emails to process.")
        return {"message": "No unread emails to process."}
    
    email_data = unread_emails[0]
    
    # Fetch the full email object, including headers
    full_email = email_service.get_gmail_service().users().messages().get(userId='me', id=email_data['id'], format='full').execute()
    customer_email_body = full_email['snippet']
    headers = full_email['payload']['headers']

    # Extract necessary headers for threading
    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')
    message_id = next((h['value'] for h in headers if h['name'].lower() == 'message-id'), '')
    references = next((h['value'] for h in headers if h['name'].lower() == 'references'), '')
    new_references = f"{references} {message_id}" if references else message_id

    # 2. Load all necessary configuration from the database
    customer_questions = db.query(models.Question).filter_by(category="customer").all()
    customer_questions_list = [q.text for q in customer_questions]
    
    all_settings = db.query(models.Setting).join(models.Question).all()
    business_settings = {s.question.text: s.value for s in all_settings}

    # 3. Find or Create the Conversation
    conversation = db.query(models.Conversation).filter_by(thread_id=email_data['threadId']).first()
    is_first_interaction = False
    if not conversation:
        is_first_interaction = True
        conversation = models.Conversation(
            thread_id=email_data['threadId'],
            customer_email=email_data['sender'],
            status="ongoing",
            gathered_data={}
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Store the incoming customer message
    db.add(models.Message(
        conversation_id=conversation.id,
        gmail_message_id=email_data['id'],
        sender='customer',
        content=customer_email_body
    ))
    db.commit()

    # 4. Determine which questions still need to be asked
    answered_questions_keys = conversation.gathered_data.keys()
    questions_to_ask_texts = [q for q in customer_questions_list if q not in answered_questions_keys]

    # --- COMPLETION AND VALIDATION LOGIC ---
    if not questions_to_ask_texts:
        validation_result = ai_service.validate_gathered_data(
            gathered_data=conversation.gathered_data,
            required_questions=customer_questions_list
        )
        
        if validation_result and validation_result.get("is_valid"):
            print("AI validation successful. Writing to Google Sheets.")
            sheet_id = business_settings.get("What is the ID of the Google Sheet for data entry?")
            if sheet_id:
                sheets_service.write_to_sheet(
                    sheet_id=sheet_id,
                    headers=customer_questions_list,
                    data=conversation.gathered_data
                )
            
            conversation.status = "completed"
            db.commit()
            final_reply = "Thank you! I have all the information I need. We will be in touch shortly."
            email_service.send_reply(
                to=conversation.customer_email, 
                subject=f"Re: {subject}", 
                body=final_reply,
                thread_id=conversation.thread_id,
                message_id_to_reply_to=message_id,
                references=new_references
            )
            email_service.mark_email_as_read(email_data['id'])
            return {"message": "Conversation completed and data saved.", "thread_id": conversation.thread_id}
        
        else:
            clarification_reason = validation_result.get("reasoning", "there was an issue with the information provided.")
            questions_to_ask_texts = [f"Please clarify based on this feedback: {clarification_reason}"]

    # --- This is the main loop for ongoing conversations ---
    ai_result = ai_service.generate_and_extract_response(
        customer_email_body=customer_email_body,
        questions_to_ask=questions_to_ask_texts,
        business_settings=business_settings,
        conversation_history=[{"sender": m.sender, "content": m.content} for m in conversation.messages],
        is_first_interaction=is_first_interaction
    )

    if not ai_result:
        # Don't raise HTTPException here, just return an error dict
        return {"error": "Failed to get a response from the AI service."}

    # 6. Update conversation state with newly extracted data
    if ai_result['extracted_data']:
        updated_data = conversation.gathered_data.copy()
        updated_data.update(ai_result['extracted_data'])
        conversation.gathered_data = updated_data
        db.commit()

    # 7. Send the AI-generated reply and store the message
    ai_reply_text = ai_result['email_reply']
    email_service.send_reply(
        to=conversation.customer_email, 
        subject=f"Re: {subject}", 
        body=ai_reply_text,
        thread_id=conversation.thread_id,
        message_id_to_reply_to=message_id,
        references=new_references
    )
    
    db.add(models.Message(
        conversation_id=conversation.id,
        sender='assistant',
        content=ai_reply_text
    ))
    db.commit()

    # 8. Mark the original email as read
    email_service.mark_email_as_read(email_data['id'])

    return {
        "message": "Successfully processed email and sent threaded reply.",
        "thread_id": conversation.thread_id,
        "data_extracted": ai_result['extracted_data']
    } 