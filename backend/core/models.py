# backend/core/models.py
import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from .database import Base

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    # NEW: 'business' for owner config, 'customer' for the AI to ask customers
    category = Column(String, default="customer", index=True)
    # field_type helps the frontend render the right input (e.g., text, textarea)
    field_type = Column(String, default="text")
    is_required = Column(Boolean, default=True)

    # This creates a one-to-one link to the setting value for this question
    setting = relationship("Setting", back_populates="question", uselist=False, cascade="all, delete-orphan")
    

class Setting(Base):
    """
    Stores the business owner's answer to a single 'business' category question.
    """
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    # The value is the owner's answer, e.g., "My Awesome Store"
    value = Column(Text, nullable=False)
    # This creates the link back to the question it answers
    question_id = Column(Integer, ForeignKey("questions.id"), unique=True, nullable=False)
    question = relationship("Question", back_populates="setting")


class Conversation(Base):
    """
    Represents a single, continuous email thread with a customer.
    """
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    # The unique thread ID from the Gmail API
    thread_id = Column(String, unique=True, index=True, nullable=False)
    customer_email = Column(String, nullable=False)
    # The current state of the conversation, e.g., "ongoing", "completed"
    status = Column(String, default="ongoing", index=True)
    # A JSON field to efficiently store the information gathered from the user
    gathered_data = Column(JSON, default={})
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # This creates a link to all messages in this conversation
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """
    Represents a single email message within a conversation.
    """
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    # The unique message ID from the Gmail API
    gmail_message_id = Column(String, unique=True)
    # The sender can be the 'customer' or the 'assistant'
    sender = Column(String, nullable=False) 
    # The full text content of the email
    content = Column(Text)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # This links the message back to its parent conversation
    conversation = relationship("Conversation", back_populates="messages")