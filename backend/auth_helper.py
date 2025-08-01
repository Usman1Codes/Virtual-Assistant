# backend/auth_helper.py

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from core.config import settings

# The file to store the credentials
TOKEN_PICKLE_FILE = 'token.pickle'

def get_gmail_credentials():
    """
    Authenticates with Google and saves the credentials.
    If credentials exist and are valid, loads them.
    Otherwise, initiates the OAuth2 flow for a script.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # For this script-based test, we use the "Installed App" flow.
            # Make sure your credentials.json is for a "Desktop app" or "Other"
            # If it's for a "Web application", this script might not work as expected,
            # but it often does for the initial token generation.
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=settings.SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds

if __name__ == '__main__':
    print("Attempting to authenticate with Google...")
    print("Please ensure 'credentials.json' from Google Cloud Console is in the 'backend' directory.")
    
    credentials = get_gmail_credentials()
    
    if credentials:
        print("\nAuthentication successful!")
        print(f"Token saved to '{TOKEN_PICKLE_FILE}'")
        if credentials.expired:
            print("Token is expired, but a refresh token is available.")
        else:
            print("Token is valid.")
    else:
        print("\nAuthentication failed.")