# backend/api/assistant.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core import models, schemas
from core.database import SessionLocal, engine
from core.engine import process_one_email # Import the new engine function

router = APIRouter(prefix="/assistant", tags=["Assistant Engine"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/process-next-email", summary="Process the next unread email")
def handle_next_email(db: Session = Depends(get_db)):
    """
    This is the main endpoint that drives the virtual assistant.
    It fetches one unread email, processes it, and sends a reply.
    """
    result = process_one_email(db)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result