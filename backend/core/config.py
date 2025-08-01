# backend/core/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
        # Google OAuth2
        GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
        GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
        GOOGLE_PROJECT_ID: str = os.getenv("GOOGLE_PROJECT_ID")
        REDIRECT_URI: str = os.getenv("REDIRECT_URI")

        # Scopes needed for Gmail API and Google Sheets
        SCOPES = [
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.send",
                "https://www.googleapis.com/auth/spreadsheets",
        ]

        # IMAP/SMTP for standard business emails
        IMAP_SERVER: str = os.getenv("IMAP_SERVER")
        IMAP_USER: str = os.getenv("IMAP_USER")
        IMAP_PASSWORD: str = os.getenv("IMAP_PASSWORD")
        SMTP_SERVER: str = os.getenv("SMTP_SERVER")
        SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
        SMTP_USER: str = os.getenv("SMTP_USER")
        SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")

        SMTP_USER: str = os.getenv("SMTP_USER")
        SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")

        GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")


settings = Settings()