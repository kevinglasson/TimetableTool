#!/usr/bin/env python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

from CurtinUnit import CurtinUnit
from CUeStudentSession import to_datetime

TZ = 'Australia/Perth'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API'


def get_credentials():
    """Get valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        # Needed only for compatibility with Python 2.6
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials


def create_Calendar(cal_name):
    """Get valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.

    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Create a new calendar in Google Calendar
    calendar = {'summary': cal_name, 'timeZone': 'Australia/Perth'}
    created_calendar = service.calendars().insert(body=calendar).execute()
    print(created_calendar['id'])


# Publishes an event to the requested calendar. event is defined as per the
# Google calendar API
def publish_event(event, calendar):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Publish event
    event = service.events().insert(calendarId=calendar, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def convert_to_gcal_event(cls):
    event = {
        'summary': '',
        'location': '',
        'start': {
            'dateTime': '',
            'timeZone': 'TZ',
        },
        'end': {
            'dateTime': '',
            'timeZone': 'TZ',
        }
    }

    event['summary'] = cls.type
    event['location'] = cls.location[0]
    event['start']['dateTime'] = to_gcal_datetime(cls.date, cls.start_time)
    event['end']['dateTime'] = to_gcal_datetime(cls.date, cls.end_time)


def to_gcal_datetime(date, time):
    date = to_datetime(date)
    gcal_datetime = '{}-{}-{}T{}:00'.format(date.year, date.month, date.day,
                                            time)
    return gcal_datetime
