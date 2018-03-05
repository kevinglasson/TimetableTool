#!/usr/bin/env python
"""Functions for working with Google Calendar's API.

The functions with in offer the ability to grant permission to a google account
using the web browser, create calendars and publish events to that calendar or
any other calendar provided the id is known.

It contains the following public usable classes/functions: (See the function
docstring for further information)

def get_credentials()

def create_calendar(cal_name)

def add_event(event, cal_id)

"""

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'My Project'


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
    credential_path = os.path.join(credential_dir, 'client_secret.json')

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
        print(credentials)

    return credentials


def create_calendar(cal_name, creds):
    """Create a new calendar.

    Create a new calendar of the specified name

    Keyword arguments:
        cal_name -- the name of the calendar to be created

    Returns:
        The id of the newly created calendar

    """
    # credentials = get_credentials()
    credentials = creds
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Create a new calendar in Google Calendar
    calendar = {'summary': cal_name, 'timeZone': 'Australia/Perth'}
    created_calendar = service.calendars().insert(body=calendar).execute()
    print('Created calendar: {}'.format(created_calendar['id']))

    return (created_calendar['id'])


def add_event(event, cal_id, creds):
    """Add an event using the Google Calendar API.

    Creates a Google Calendar API service object
    and creates a new event on the user's calendar.

    Keyword arguments:
        event -- compatible event containing information
        cal_id -- id of the calendar to be posted to

    """
    # credentials = get_credentials()
    credentials = creds
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = service.events().insert(calendarId=cal_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
