# backend/services/ai_service.py

import json
import google.generativeai as genai
from core.config import settings
from typing import List, Dict, Any, Optional

# --- Model Initialization (No changes here) ---
try:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    print("Gemini Pro model initialized successfully.")
except Exception as e:
    print(f"Error initializing Gemini Pro model: {e}")
    model = None

def format_conversation_history(history: List[Dict[str, str]]) -> str:
    """Helper function to format the conversation history for the prompt."""
    if not history:
        return "No previous conversation history."
    return "\n".join([f"{msg['sender'].capitalize()}: {msg['content']}" for msg in history])


def generate_and_extract_response(
    customer_email_body: str,
    questions_to_ask: List[str],
    business_settings: Dict[str, str],
    conversation_history: List[Dict[str, str]],
    is_first_interaction: bool
) -> Optional[Dict[str, Any]]:
    """
    Analyzes customer email, extracts data, and generates a reply.

    This is the new core of the AI. It takes business settings dynamically
    and decides how to respond.

    Returns a dictionary with 'email_reply' and 'extracted_data', or None on failure.
    """
    if not model:
        return None

    # --- Retrieve dynamic business settings ---
    # We use .get() to safely access settings, providing sensible defaults.
    business_name = business_settings.get("What is your business name?", "Our Business")
    welcome_template = business_settings.get(
        "What is the welcome message for new customers? Use {business_name} as a placeholder.",
        "Hello! Thanks for contacting {business_name}. To get started, I just need a little more information."
    )
    # --- Prompt Engineering ---
    
    # The prompt changes based on whether it's the first time we're talking to this customer.
    if is_first_interaction:
        # Format the welcome message with the actual business name.
        formatted_welcome = welcome_template.format(business_name=business_name)

        prompt_template = f"""
        You are the AI assistant for "{business_name}".
        Your task is to greet a new customer and collect information.

        ### YOUR TASK
        1.  Start with this exact welcome message: "{formatted_welcome}"
        2.  Then, politely ask for ALL of the following pieces of information in a clear list: {questions_to_ask}
        3.  Analyze the customer's first email below. Did they already provide any of the requested information?
        4.  You MUST output a single, valid JSON object. This object must have two keys: "email_reply" and "extracted_data".
            - "email_reply": The complete, friendly email body to send to the customer.
            - "extracted_data": A JSON object containing any information you extracted from their first email. The keys must be the exact question text. If nothing was extracted, this should be an empty object {{}}.

        ### Customer's First Email:
        ---
        {customer_email_body}
        ---
        """
    else:  # This is a follow-up interaction
        prompt_template = f"""
        You are the AI assistant for "{business_name}".
        Your goal is to continue a conversation and collect any remaining information.

        ### CONTEXT
        - Conversation History:
          {format_conversation_history(conversation_history)}
        - Questions we still need answers for:
          {questions_to_ask}

        ### YOUR TASK
        1.  Carefully analyze the "Latest Customer Email" below.
        2.  Extract any answers for the questions we still need.
        3.  Formulate a friendly reply. First, thank them for the information they provided. Then, politely ask for the remaining information from the list. Do not be demanding.
        4.  If the customer has answered all questions, your reply should be a final confirmation message thanking them and stating that you have all the needed information.
        5.  You MUST output a single, valid JSON object with two keys: "email_reply" and "extracted_data".
            - "email_reply": The complete, friendly email body to send to the customer.
            - "extracted_data": A JSON object containing any NEW information you extracted from this specific email. If nothing new was extracted, this should be an empty object {{}}.

        ### Latest Customer Email:
        ---
        {customer_email_body}
        ---
        """

    try:
        print("--- Sending Prompt to Gemini ---")
        # For debugging, you can uncomment the next line
        # print(prompt_template)
        response = model.generate_content(prompt_template)
        
        # We need to be robust in parsing the JSON that Gemini returns.
        json_string = response.text.strip().lstrip("```json").rstrip("```").strip()
        parsed_response = json.loads(json_string)

        # Validate that the response has the keys we expect
        if "email_reply" not in parsed_response or "extracted_data" not in parsed_response:
             raise KeyError("Response from AI is missing required keys.")

        print(f"--- Received Parsed Response from Gemini: ---\n{json.dumps(parsed_response, indent=2)}")
        return parsed_response

    except (json.JSONDecodeError, KeyError) as e:
        print(f"[AI SERVICE ERROR] Could not parse or validate JSON response from Gemini: {e}")
        print(f"Raw response was: {response.text}")
        return None
    except Exception as e:
        print(f"[AI SERVICE ERROR] An unexpected error occurred while calling the Gemini API: {e}")
        return None

def validate_gathered_data(gathered_data: Dict[str, Any], required_questions: List[str]) -> Optional[Dict[str, Any]]:
        """
        Asks the AI to validate the completeness and logical sense of the collected data.
        """
        if not model:
            return None

        prompt = f"""
        You are a data validation expert. Your task is to check if the following collected data is complete and logically valid.

        ### Rules:
        1. All required questions must have a non-empty answer.
        2. The answers should make sense. For example, an order number should look like a number, not a poem.

        ### Data to Validate:
        - Required Questions: {required_questions}
        - Collected Data: {json.dumps(gathered_data, indent=2)}

        ### Your Task:
        Respond with a single, valid JSON object with two keys:
        1. "is_valid": A boolean (true or false).
        2. "reasoning": A string explaining your decision. If invalid, explain what is missing or incorrect. If valid, say "All data is complete and looks correct."
        """
        try:
            response = model.generate_content(prompt)
            json_string = response.text.strip().lstrip("```json").rstrip("```").strip()
            parsed_response = json.loads(json_string)
            return parsed_response
        except Exception as e:
            print(f"[AI VALIDATION ERROR] {e}")
            return {"is_valid": False, "reasoning": "A system error occurred during validation."}