#!/usr/bin/env python
"""The CUeStudentSession class and associated functions.

This class contains and stores all functions and variables necessary
for interacting with Curtin's eStudent portal. It accessess and extracts
the timetable information for the provided login details and stores them
in a CurtinUnit object

It contains the following public usable classes/functions: (See the function
docstring for further information)

class CUeStudentSession(object)

def login(self, studentid, password)

def get_timetables(self)

def get_all_timetables(self)

"""

from __future__ import print_function
from bs4 import BeautifulSoup
from CurtinUnit import CurtinUnit
from exceptions import LoginFailedError
import datetime
import getpass
import requests

LOGIN_URL = 'https://oasis.curtin.edu.au/Auth/Logon'
OASIS_URL = 'https://oasis.curtin.edu.au/'
MY_STUDIES_URL = 'https://oasis.curtin.edu.au/MyStudies'
ESTUDENT_URL = 'https://estudent.curtin.edu.au/eStudent/'
TIMETABLE_URL = 'https://estudent.curtin.edu.au/eStudent/SM/StudentTtable10.aspx?r=%23CU.ESTU.STUDENT&f=%23CU.EST.TIMETBL.WEB'
MONTHS = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
    'Nov', 'Dec'
]
SCHOOLDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class CUeStudentSession():
    """Form a requests session for Curtin eStudent.

    This class contains and stores all functions and variables necessary
    for interacting with Curtin's eStudent portal. It accessess and extracts
    the timetable information for the provided login details and stores them
    in a CurtinUnit object

    """

    def __init__(self):
        self.sess = requests.Session()
        self.current_page = None
        self.current_page_date = datetime.datetime.today().date()

    # Login
    def login(self, studentid, password):
        r = self.sess.get(LOGIN_URL)
        data = dict(UserName=studentid, Password=password)
        r = self.sess.post(LOGIN_URL, data=data, allow_redirects=False)
        if r.status_code != requests.codes.found:
            raise LoginFailedError(r)
        else:
            print('\nLogin successful \n')

    # Get today's timetable page
    def navigate_tt_page_today(self):
        # Navigate to the 'My Studies' tab
        r = self.sess.post(MY_STUDIES_URL)
        # Navigate to the 'eStudent'
        r = self.sess.get(ESTUDENT_URL)
        # Navigate to the 'My Classes' tab
        r = self.sess.get(TIMETABLE_URL)
        # Navigate to today's timetable page
        self.set_timetable_page_dated(self.current_page_date)
        # Store the current page as text
        self.current_page = r.text

    def navigate_tt_page_dated(self, date):
        # Convert to compatible date string
        compatible_date = self.datetime_to_estudent(date)
        # Get page data for navigating
        data = self.make_estudent_happy(self.current_page)
        # Add data to navigate to requested date
        data.update({
            'ctl00$Content$ctlFilter$TxtStartDt': date,
            'ctl00$Content$ctlFilter$BtnSearch': 'Refresh',
        })
        r = self.sess.post(TIMETABLE_URL, data=data, allow_redirects=False)
        r.raise_for_status()
        # Update_current page
        self.current_page = r.text

    def advance_tt_page_one_week(self):
        date = self.current_page_date + datetime.timedelta(days=7)
        self.navigate_tt_page_dated(date)

    def get_all_timetables(self):
        """Get all of the timetables for the study period.

        This will process timetables until it finds 3 consectuive empty weeks.
        This signals the end of that study period and will not break when there
        is a 2 week tuition free period. Returns the entire list of dictionaries
        to the caller.
        """
        sem_unit_lst = []
        # Due to the nature of estudent it loads a complete timetable first
        # and we don't actually want this so on the first iteration we need
        # To get the timetable twice... I think.

        self.get_timetable_page()

        while self.consecutive_empty_weeks <= 2:
            unit_lst = self.proc_timetable_page()
            self.set_timetable_page_dated(self.timetable_page_mon_date)
            self.inc_mon_date()
            if self.check_for_empty_week(unit_lst) is False:
                sem_unit_lst.append(unit_lst)

        return (sem_unit_lst)

    def check_for_empty_week(self, dict_):
        """Check if there are only default entries and return True or False.

        Keyword arguments:
        dict_ -- Dictionary containing the CurtinUnits

        """
        empty = False
        num_empty = 0
        for key, value in dict_.iteritems():
            if value.unit_code is 'Default':
                num_empty += 1
        if num_empty == len(dict_):
            empty = True
            self.consecutive_empty_weeks += 1
        else:
            self.consecutive_empty_weeks = 0
        return empty

    def make_estudent_happy(page):
        """Extract required form values for POST requests."""
        values = {}
        soup = BeautifulSoup(page, "lxml")

        for name in '__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION':
            values[name] = soup.find(id=name)['value']

        return values


    def to_24h(time):
        """Convert 12h time string to 24h time string.

        Keyword arguments:
        time - 12h time in the format 00:00xm

        """
        am_pm = time[-2:].lower()
        hour, minute = time[:-2].split(':')
        hour = int(hour)
        if am_pm == 'pm' and hour != 12:
            hour += 12
        # Right align, pad with 0's and use 2 numbers always!
        return '{:>02}:{}'.format(hour, minute)


    # This is potentially useless AF, I hope to delete it
    def date_from_day_abbr(self, string, mon_date):
        """Convert an abbreviated day string i.e. Wed.

        Requires the date of the monday of that week to calculate the date of the
        abbreviated day.

        Keyword arguments:
        mon_date -- the monday date for the week containing the abbreviated day

        """
        for i, day in enumerate(DAYS):
            if day == string:
                date = mon_date + datetime.timedelta(days=i)
                break
        return self.datetime_to_estudent(date)

    def datetime_to_estudent(self, date):
        """Take a datetime object and return a compatible string.
        (2017, 5, 4) -> 04-May-2017
        """
        string = date.strftime('%d-%b-%Y')
        return string

    def estudent_to_datetime(self, string):
        """Take a date in string form and return a datetime object.
        04-May-2017 -> (2017, 5, 4)
        """
        # datetime.date(2017, 5, 4)
        date = datetime.datetime.strptime(string, '%d-%b-%Y').date()
        return date
