# backend/api/config.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core import models, schemas
from core.database import SessionLocal

router = APIRouter(prefix="/config", tags=["Configuration"])

# Dependency to get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Question Endpoints ---

@router.post("/questions/", response_model=schemas.Question, summary="Create a Question")
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    """
    Create a new question for the assistant to ask.
    - **text**: The question itself (e.g., "What is your full name?").
    - **field_type**: The type of data expected (e.g., "text", "email").
    - **is_required**: Whether the assistant must get an answer for this.
    """
    db_question = models.Question(
        text=question.text,
        category=question.category, # Explicitly set the category
        field_type=question.field_type,
        is_required=question.is_required
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/questions/", response_model=List[schemas.Question], summary="Get Questions by Category")
def read_questions(category: str = "customer", db: Session = Depends(get_db)):
    """
    Retrieve questions, filtering by category ('customer' or 'business').
    """
    questions = db.query(models.Question).filter(models.Question.category == category).all()
    return questions

@router.delete("/questions/{question_id}", response_model=schemas.Question, summary="Delete a Question")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """
    Delete a question by its ID.
    """
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(db_question)
    db.commit()
    # Pydantic needs a dictionary or ORM model to serialize, so we return the deleted object
    return db_question

@router.post("/settings/", response_model=schemas.Setting, summary="Create or Update a Setting")
def create_or_update_setting(setting: schemas.SettingCreate, db: Session = Depends(get_db)):
    """
    Saves the business owner's answer to a business question.
    """
    db_setting = db.query(models.Setting).filter_by(question_id=setting.question_id).first()
    if db_setting:
        # Update existing setting
        db_setting.value = setting.value
    else:
        # Create new setting
        db_setting = models.Setting(question_id=setting.question_id, value=setting.value)
        db.add(db_setting)
    
    db.commit()
    db.refresh(db_setting)
    return db_setting

@router.get("/settings/", response_model=List[schemas.Setting], summary="Get All Settings")
def read_settings(db: Session = Depends(get_db)):
    """
    Retrieve all saved business settings.
    """
    return db.query(models.Setting).all()