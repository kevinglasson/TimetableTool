#!/usr/bin/env python
"""Program to obtain student timetable and publish to google calendar.

This program works with Curtin University's eStudent portal and is able to
obtain a students timetable data and output it to a newly created google calendar.

"""

import requests
import requests.packages.urllib3
import getpass
import pandas as pd
from CurtinUnit import CurtinUnit
from CUeStudentSession import CUeStudentSession, LoginFailedError


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


def main():
    """Get user input and control the program."""
    # Just for me so I don't have to see warning about my python being old!
    requests.packages.urllib3.disable_warnings()

    username = raw_input('USERNAME: ')
    password = getpass.getpass('PASSWORD: ')
    calendar_name = raw_input('New calendar name: ')

    try:
        # This should be a list of CurtinUnit objects
        timetable = get_all_timetables(username, password)
        print_timetable(timetable)
    except LoginFailedError:
        print('{"error":"Login failed. Wrong username or password?"}')


if __name__ == '__main__':
    main()
