from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from core import models, schemas
from core.database import SessionLocal

router = APIRouter(prefix="/conversations", tags=["Conversations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Conversation], summary="Get All Conversations")
def read_conversations(db: Session = Depends(get_db)):
    """
    Retrieve all conversations from the database, including their messages.
    This endpoint uses 'joinedload' to efficiently fetch conversations
    and their related messages in a single query.
    """
    conversations = (
        db.query(models.Conversation)
        .options(joinedload(models.Conversation.messages))
        .order_by(models.Conversation.updated_at.desc())
        .all()
    )
    return conversations 