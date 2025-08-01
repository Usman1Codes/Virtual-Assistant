# backend/services/email_service.py

import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from api.auth import get_gmail_credentials # Import the function to load credentials

def get_gmail_service():
    """Builds and returns a Gmail API service object."""
    creds = get_gmail_credentials()
    if not creds:
        print("Error: No valid credentials found. Please authenticate first via the /auth/google endpoint.")
        return None
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"An error occurred while building the Gmail service: {e}")
        return None

def fetch_emails(max_results=5):
    """
    Fetches unread emails from the inbox.
    Returns a list of dictionaries, each containing 'id', 'sender', 'subject', and 'snippet'.
    """
    service = get_gmail_service()
    if not service:
        return {"error": "Could not connect to Gmail service. Have you authenticated?"}

    try:
        # List unread messages in the INBOX.
        results = service.users().messages().list(
            userId='me', 
            labelIds=['INBOX', 'UNREAD'],
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return [] # Return an empty list if no unread emails are found

        email_list = []
        for msg in messages:
            # Get full message metadata to extract headers
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata').execute()
            headers = msg_data['payload']['headers']
            
            # Find the Subject and From headers
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'No Sender')
            
            email_list.append({
                "id": msg['id'],
                "threadId": msg['threadId'],
                "sender": sender,
                "subject": subject,
                "snippet": msg_data['snippet']
            })
            
        return email_list

    except HttpError as error:
        print(f'An error occurred during fetch: {error}')
        return {"error": f"An HTTP error occurred: {error}"}


def send_email(to: str, subject: str, body: str):
    """
    Creates and sends an email via the Gmail API.
    """
    service = get_gmail_service()
    if not service:
        return {"error": "Could not connect to Gmail service. Have you authenticated?"}

    try:
        # Create the email message object
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        # The 'from' field is automatically set to the authenticated user's email.
        # The message needs to be base64url encoded.
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {'raw': encoded_message}
        
        send_message = service.users().messages().send(userId='me', body=create_message).execute()
        print(f"Message sent. ID: {send_message['id']}")
        return send_message

    except HttpError as error:
        print(f'An error occurred during send: {error}')
        return {"error": f"An HTTP error occurred: {error}"}

def send_reply(to: str, subject: str, body: str, thread_id: str, message_id_to_reply_to: str, references: str):
    """
    Sends a reply to a specific email, creating a proper thread.
    """
    service = get_gmail_service()
    if not service:
        return {"error": "Could not connect to Gmail service."}

    try:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        # --- This is the critical part for threading ---
        message['In-Reply-To'] = message_id_to_reply_to
        message['References'] = references
        # ---------------------------------------------
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message,
            'threadId': thread_id  # Explicitly tell Gmail which thread this belongs to
        }
        
        sent_message = service.users().messages().send(userId='me', body=create_message).execute()
        print(f"Reply sent in thread {thread_id}. New message ID: {sent_message['id']}")
        return sent_message

    except HttpError as error:
        print(f'An error occurred during send_reply: {error}')
        return {"error": f"An HTTP error occurred: {error}"}

def mark_email_as_read(message_id: str):
    """Marks an email as read by removing the 'UNREAD' label."""
    service = get_gmail_service()
    if not service:
        return {"error": "Could not connect to Gmail service."}
    
    try:
        # The body of the request specifies to remove the UNREAD label.
        body = {'removeLabelIds': ['UNREAD']}
        service.users().messages().modify(userId='me', id=message_id, body=body).execute()
        print(f"Message {message_id} marked as read.")
        return {"status": "success"}
    except HttpError as error:
        print(f'An error occurred while marking email as read: {error}')
        return {"error": str(error)}