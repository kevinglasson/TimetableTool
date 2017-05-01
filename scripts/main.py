#!/usr/bin/env python
"""Program to obtain student timetable and publish to google calendar.

This program works with Curtin University's eStudent portal and is able to
obtain a students timetable data and output it to a newly created google calendar.

"""

import requests
import requests.packages.urllib3
import getpass
import pandas as pd
import gcal
import time
from CurtinUnit import CurtinUnit
from CUeStudentSession import CUeStudentSession, LoginFailedError

# TODO: Event colours for Google Events, will move these to a more sane place at
# some stage
COLOURS = ['11', '10', '7', '3', '9', '5']


def print_timetable(timetable):
    """Print the entire timetable.

    This looped printing is purely for debugging and validation.

    """
    for dict_ in timetable:
        for key, value in dict_.iteritems():
            print "------------------------------------------------------------------\n"
            value.to_string()
            # print(value.class_list[0].date)


def get_timetable(studentid, password):
    """Get a single timetable from the default page.

    Keyword arguments:
        studentid -- the students id number
        password -- the students password

    Returns:
        timetable -- the obtained timetable

    """
    session = CUeStudentSession()
    session.login(studentid, password)
    return session.get_timetable()


def get_all_timetables(studentid, password):
    """Get all timetables from the current study period.

    All timetables refers to the individual timetable for each week of the
    study period.

    Keyword arguments:
        studentid -- the students id number
        password -- the students password

    Returns:
        timetable -- the obtained timetable

    """
    session = CUeStudentSession()
    session.login(studentid, password)
    return session.get_all_timetables()


def convert_timetable_for_gcal(timetable):
    """Convert timetable data and return a list of google calendar events.

    Keyword arguments:
        timetable -- List of Dictionaries containing CurtinUnit objects

    Retruns:
        event_list -- List of google calendar compatible events

    """
    # Make a list of the unit names, will use the index to pick a colour
    # for the event
    unit_names = []
    for dict_ in timetable:
        for key, value in dict_.iteritems():
            if value.unit_code not in unit_names:
                unit_names.append(value.unit_code)

    event_list = []
    for dict_ in timetable:
        # value is a CurtinUnit
        for key, value in dict_.iteritems():
            # Get a colour, same one for each unit!
            colour = COLOURS[unit_names.index(value.unit_code)]
            for cls in value.class_list:
                event_list.append(
                    gcal.convert_to_gcal_event(cls, value.unit_code, colour))

    return (event_list)


def main():
    """Get user input and control the program."""
    # Just for me so I don't have to see warning about my python being old!
    requests.packages.urllib3.disable_warnings()

    username = raw_input('OASIS Username: ')
    password = getpass.getpass('OASIS Password: ')
    calendar_name = raw_input('Name of calendar to be created: ')

    try:
        # Get the timetable data
        timetable = get_all_timetables(username, password)
        # Create a calendar and ge the id
        cal_id = gcal.create_calendar(calendar_name)
        event_list = convert_timetable_for_gcal(timetable)
        for event in event_list:
            gcal.add_event(event, cal_id)
    except LoginFailedError:
        print('{"error":"Login failed. Wrong username or password?"}')

    print('Successfully Completed')


if __name__ == '__main__':
    """Exectute the following if this script is run directly."""
    main()
