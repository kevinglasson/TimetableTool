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

import datetime

from CurtinUnit import CurtinUnit
from CUeStudentSession import to_datetime

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

    return credentials


def create_calendar(cal_name):
    """Create a new calendar.

    Create a new calendar of the specified name

    Keyword arguments:
        cal_name -- the name of the calendar to be created

    Returns:
        The id of the newly created calendar

    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Create a new calendar in Google Calendar
    calendar = {'summary': cal_name, 'timeZone': 'Australia/Perth'}
    created_calendar = service.calendars().insert(body=calendar).execute()
    print('Created calendar: {}'.format(created_calendar['id']))

    return (created_calendar['id'])


def add_event(event, cal_id):
    """Add an event using the Google Calendar API.

    Creates a Google Calendar API service object
    and creates a new event on the user's calendar.

    Keyword arguments:
        event -- compatible event containing information
        cal_id -- id of the calendar to be posted to

    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = service.events().insert(calendarId=cal_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


# TODO: This should probably be moved to my my class I think, as it is added
# functionality for it
def convert_to_gcal_event(cls, unit_code, colour):
    """Convert a CurtinClass object to a Google Calendar compatible event.

    From a CurtinClass object extract all necessary fields to create a calendar
    event, also prepend the unit_code to the summary and set the event colour

    Keyword arguments:
        cls -- CurtinClass object
        unit_code -- string containing the unit code
        colour -- integer as per Google's API representing event colour

    Returns:
        event -- converted event

    """
    event = {
        'summary': '',
        'location': '',
        'start': {
            'dateTime': ''
        },
        'end': {
            'dateTime': ''
        },
        'colorId': ''
    }

    event['summary'] = '{} - {}'.format(unit_code, cls.type.capitalize())
    event['location'] = cls.location
    event['start']['dateTime'] = to_gcal_datetime(cls.date, cls.start)
    event['end']['dateTime'] = to_gcal_datetime(cls.date, cls.end)
    event['colorId'] = colour

    return (event)


# This method should be in CurtinClass as well, as it is specific for the
# CurtinClass formatting
def to_gcal_datetime(date, time):
    """Convert date and time to google formatted dattime.

    Keyword arguments:
        date -- date string containing the date
        time -- time string containing the time

    Returns:
        gcal_datetime -- formatted date string

    """
    date = to_datetime(date)
    gcal_datetime = '{}-{:>02}-{:>02}T{}:00+08:00'.format(
        date.year, date.month, date.day, time)
    return gcal_datetime
