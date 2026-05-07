import os.path
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail permissions
SCOPES = ['https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/calendar']


def authenticate_gmail():
    creds = None

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    token_path = os.path.join(BASE_DIR, "token.pickle")
    credentials_path = os.path.join(BASE_DIR, "credentials.json")

    # Load existing token
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # If no valid token, login again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return creds