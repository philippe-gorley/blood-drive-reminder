import httplib2
import os

import googleapiclient
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class GCalendar:

    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'blood_drive_cal.json'
    APPLICATION_NAME = 'blood-drive-cal'

    def __init__(self):
        pass

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'blood_drive_cal.oauth')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(GCalendar.CLIENT_SECRET_FILE, GCalendar.SCOPES)
            flow.user_agent = GCalendar.APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)
        return credentials

    def add(self, blood_drive):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        if not self.is_duplicate_drive(service, blood_drive.event_id):
            event_body = self.create_event(blood_drive)
            service.events().insert(calendarId='primary', body=event_body).execute()

    def is_duplicate_drive(self, service, blood_drive_id):
        try:
            ev = service.events().get(calendarId='primary', eventId=blood_drive_id).execute()
            return True
        except googleapiclient.errors.HttpError:
            return False

    def create_event(self, blood_drive):
        event_body = {
            'summary': 'Blood Drive',
            'location': blood_drive.address,
            'description': 'A blood drive',
            'start': {
                'dateTime': blood_drive.start_time.isoformat('T'),
                'timeZone': 'America/Toronto',
            },
            'end': {
                'dateTime': blood_drive.end_time.isoformat('T'),
                'timeZone': 'America/Toronto',
            },
        }
        return event_body
