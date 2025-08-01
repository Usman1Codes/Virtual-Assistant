# backend/api/auth.py

import os
import pickle
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.errors import HttpError
from core.config import settings

# The file to store the credentials
TOKEN_PICKLE_FILE = 'token.pickle'

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_google_flow():
    """Initializes the Google OAuth2 flow."""
    return Flow.from_client_secrets_file(
        'credentials.json',
        scopes=settings.SCOPES,
        redirect_uri=settings.REDIRECT_URI
    )

@router.get("/google")
async def auth_google(flow: Flow = Depends(get_google_flow)):
    """
    Redirects the user to Google's OAuth 2.0 server to start the authentication process.
    """
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return RedirectResponse(authorization_url)


@router.get("/google/callback")
async def auth_google_callback(request: Request, flow: Flow = Depends(get_google_flow)):
    """
    Handles the callback from Google's OAuth 2.0 server.
    Fetches the token, saves it, and redirects to the frontend dashboard.
    """
    # The full URL is needed to process the callback correctly.
    full_callback_uri = str(request.url)

    # Use the authorization response URL to fetch the token.
    flow.fetch_token(authorization_response=full_callback_uri)
    
    # Get the credentials from the flow
    credentials = flow.credentials

    # Save the credentials for the next run
    with open(TOKEN_PICKLE_FILE, 'wb') as token:
        pickle.dump(credentials, token)

    # Redirect to the frontend dashboard for a seamless experience
    return RedirectResponse("http://localhost:5173/dashboard")


def get_gmail_credentials():
    """
    Loads saved credentials from token.pickle.
    This function will be used by other services.
    """
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Check if credentials are still valid, refresh if expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(GoogleRequest())
        # Save the refreshed credentials
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    if not creds or not creds.valid:
        # If creds are invalid and there's no refresh token, we can't proceed.
        return None
        
    return creds

@router.get("/status", summary="Check Authentication Status")
def auth_status():
    """
    Checks if the user is authenticated by looking for valid credentials.
    """
    creds = get_gmail_credentials()
    if creds:
        # We can do a quick test API call to see if token is truly valid
        try:
            from googleapiclient.discovery import build
            service = build('gmail', 'v1', credentials=creds)
            service.users().getProfile(userId='me').execute()
            return {"authenticated": True}
        except HttpError as e:
            # If the token is invalid (e.g., revoked), the API call will fail.
            if e.resp.status in [401, 403]:
                return {"authenticated": False}
            # Handle other potential http errors if necessary
            return {"authenticated": False}
        except Exception:
            return {"authenticated": False}
    return {"authenticated": False}
