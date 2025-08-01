# backend/main.py
import asyncio
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from api import auth, email, config, assistant, conversations
from core.database import engine, SessionLocal
from core import models
from core.engine import process_one_email


app = FastAPI(
    title="Personalized E-Commerce Virtual Assistant",
    description="An AI-powered assistant to handle customer queries via email.",
    version="0.1.0"
)

# --- Background Scheduler ---
async def run_assistant_scheduler():
    loop = asyncio.get_running_loop()
    while True:
        print("Scheduler: Checking if ready to process emails...")
        db = SessionLocal()
        try:
            # 1. Check if the business configuration is complete
            business_questions = db.query(models.Question).filter_by(category="business", is_required=True).all()
            required_question_ids = {q.id for q in business_questions}
            
            saved_settings = db.query(models.Setting).filter(models.Setting.question_id.in_(required_question_ids)).all()
            saved_question_ids = {s.question_id for s in saved_settings}

            if required_question_ids.issubset(saved_question_ids):
                print("Scheduler: Configuration is complete. Running email processing engine in background thread.")
                # Run the synchronous, blocking function in a separate thread
                await loop.run_in_executor(None, process_one_email, db)
            else:
                missing_ids = required_question_ids - saved_question_ids
                print(f"Scheduler: Assistant setup is not complete. Waiting for settings for question IDs: {missing_ids}")
        except Exception as e:
            # Add robust error handling for the task itself
            print(f"SCHEDULER ERROR: An exception occurred: {e}")
        finally:
            db.close()
        
        # 2. Wait for 30 seconds before the next cycle
        await asyncio.sleep(30)

# --- Database Seeding Function ---
def seed_database():
    db = SessionLocal()
    try:
        # Check if the first business question already exists
        first_question = db.query(models.Question).filter_by(text="What is your business name?").first()
        if not first_question:
            print("Database is empty. Seeding with default business questions...")
            default_business_questions = [
                models.Question(text="What is your business name?", category="business", field_type="text", is_required=True),
                models.Question(text="Provide a short description of your business.", category="business", field_type="textarea", is_required=True),
                models.Question(text="What is the welcome message for new customers? Use {business_name} as a placeholder.", category="business", field_type="textarea", is_required=True),
                models.Question(text="What is the assistant's primary tone?", category="business", field_type="text", is_required=True),
                models.Question(text="What is the ID of the Google Sheet for data entry?", category="business", field_type="text", is_required=True)
            ]
            db.add_all(default_business_questions)
            db.commit()
            print("Default business questions have been seeded.")
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    # Create DB tables
    models.Base.metadata.create_all(bind=engine)
    # Run the seeding function
    seed_database()
    # Start the background task
    asyncio.create_task(run_assistant_scheduler())


origins = [
    "http://localhost:5173", # The default port for Vite React apps
    "http://localhost:3000", # A common port for other React apps
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)


# Include the authentication router
app.include_router(auth.router)
app.include_router(email.router)
app.include_router(config.router)
app.include_router(assistant.router)
app.include_router(conversations.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Virtual Assistant API"}
