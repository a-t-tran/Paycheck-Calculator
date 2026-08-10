# auth.py
# imports
# Built-in library for checking files and interacting with the OS
import os

# represents a saved login session (token) so we don't have to log in every time
from google.oauth2.credentials import Credentials

# runs the browser login flow using credentials.json
from google_auth_oauthlib.flow import InstalledAppFlow

# refreshes an expired token without needing to log in again
from google.auth.transport.requests import Request

# scope
# defines what level of access we're requesting — read-only calendar access
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# function
# handles the full login process: checks for saved token, refreshes it, or logs in fresh
def authenticate():
    # placeholder — will hold our login credentials once we find or create them
    creds = None

    # if we've logged in before, a token.json file will already exist
    if os.path.exists('token.json'):
        # load the saved credentials from token.json
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # if there's no valid login, we need to get one (either refresh or fresh login)
    if not creds or not creds.valid:
        # if we have an expired token that can be refreshed, refresh it instead of logging in again
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # otherwise, run the full browser login using credentials.json
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # save the credentials (new or refreshed) so we don't have to repeat this next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # send the credentials back so other parts of our program can use them
    return creds

# only runs this test code if we run auth.py directly (not if it's imported elsewhere later)
if __name__ == '__main__':
    creds = authenticate()
    print("Authentication successful!")