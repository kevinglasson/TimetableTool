#!/usr/bin/env python

from CurtinClass import CurtinClass

DEFAULT_TIMEZONE = 'Australia/Perth'


# Takes a CurtinClass object in and extract the necessary information to create
# a Google calendar event
def convert_to_gcal_event(cls):
    event = {
        'summary': '',
        'location': '',
        'start': {
            'dateTime': '',
            'timeZone': 'DEFAULT_TIMEZONE',
        },
        'end': {
            'dateTime': '',
            'timeZone': 'DEFAULT_TIMEZONE',
        }
    }

    event['summary'] = cls.type
    event['location'] = cls.location[0]
    event['start']['dateTime'] =
    event['end']['dateTime'] =

def convert_to_gcal_datetime():
