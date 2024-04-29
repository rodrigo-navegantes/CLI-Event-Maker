import datetime
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    # Load existing credentials from a token file if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_event(service, summary, location, description, start_datetime, end_datetime):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'America/Sao_Paulo',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created:', event.get('htmlLink'))

def main():
    # Get credentials and build service (same as before)
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
   
    # Define event details
    summary = input("Summary: ")
    location = input("Location: ")
    description = input("Description: ")
    start_datetime = input("Start Time: ")
    end_datetime = input("End Time: ")    
    # Create the event
    create_event(service, summary, location, description, start_datetime, end_datetime)

if __name__ == '__main__':
    main()
