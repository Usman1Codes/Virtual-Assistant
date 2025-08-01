# backend/core/schemas.py
import datetime
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


# Update Question schemas
class QuestionBase(BaseModel):
    text: str
    category: str = "customer"
    field_type: str = "text"
    is_required: bool = True

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    class Config:
        from_attributes = True

# Add new Setting schemas
class SettingBase(BaseModel):
    value: str

class SettingCreate(SettingBase):
    question_id: int

class Setting(SettingBase):
    id: int
    question_id: int
    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    sender: str
    content: str

class MessageCreate(MessageBase):
    conversation_id: int
    gmail_message_id: Optional[str] = None

class Message(MessageBase):
    id: int
    created_at: datetime.datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    thread_id: str
    customer_email: str
    status: str = "ongoing"
    gathered_data: Dict[str, Any] = {}

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    messages: List[Message] = [] # A conversation includes a list of its messages

    class Config:
        from_attributes = True