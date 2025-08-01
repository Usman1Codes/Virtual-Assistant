# backend/api/email.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import email_service

router = APIRouter(prefix="/emails", tags=["Emails"])

class EmailSchema(BaseModel):
    to: str
    subject: str
    body: str

@router.get("/fetch", summary="Fetch Unread Emails")
async def get_emails():
    """
    Fetches the latest unread emails from the authenticated user's inbox.
    """
    emails = email_service.fetch_emails()
    if isinstance(emails, dict) and "error" in emails:
        raise HTTPException(status_code=500, detail=emails["error"])
    return emails

@router.post("/send", summary="Send an Email")
async def send_new_email(email: EmailSchema):
    """
    Sends an email using the authenticated user's Gmail account.
    """
    sent_message = email_service.send_email(
        to=email.to, 
        subject=email.subject, 
        body=email.body
    )
    if isinstance(sent_message, dict) and "error" in sent_message:
        raise HTTPException(status_code=500, detail=sent_message["error"])
    return {"message": "Email sent successfully!", "details": sent_message}