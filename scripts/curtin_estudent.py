#!/usr/bin/env python
"""The CUeStudentSession class and associated functions.

This class contains and stores all functions and variables necessary
for interacting with Curtin's eStudent portal. It accessess and extracts
the timetable information for the provided login details and stores them
in a CurtinUnit object

It contains the following public usable classes/functions: (See the function
docstring for further information)
"""

from __future__ import print_function
from bs4 import BeautifulSoup
import exceptions
import datetime
import getpass
import requests
import utilities as utils

LOGIN_URL = 'https://oasis.curtin.edu.au/Auth/Logon'
OASIS_URL = 'https://oasis.curtin.edu.au/'
MY_STUDIES_URL = 'https://oasis.curtin.edu.au/MyStudies'
ESTUDENT_URL = 'https://estudent.curtin.edu.au/eStudent/'
TIMETABLE_URL = 'https://estudent.curtin.edu.au/eStudent/SM/StudentTtable10.aspx?r=%23CU.ESTU.STUDENT&f=%23CU.EST.TIMETBL.WEB'
MONTHS = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
    'Nov', 'Dec'
]


class Session():
    """Form a requests session for Curtin eStudent."""

    def __init__(self):
        self.sess = requests.Session()
        self.current_page = None
        self.current_page_date = None
        self.current_data = (self.current_page, self.current_page_date)

    # Login
    def login(self, studentid, password):
        r = self.sess.get(LOGIN_URL)
        data = dict(UserName=studentid, Password=password)
        r = self.sess.post(LOGIN_URL, data=data, allow_redirects=False)
        if r.status_code != requests.codes.found:
            raise exceptions.LoginFailedError(r)
        else:
            print('\nLogin successful')

    # Get today's timetable page by navigating to the monday of
    # this week.
    def navigate_tt_page(self):
        # Navigate to the 'My Studies' tab
        r = self.sess.post(MY_STUDIES_URL)
        # Navigate to the 'eStudent'
        r = self.sess.get(ESTUDENT_URL)
        # Navigate to the 'My Classes' tab
        r = self.sess.get(TIMETABLE_URL)
        # Update current page
        self.current_page = r.text
        # Navigate to today's timetable page
        self.navigate_tt_page_dated(self.get_this_monday())
        # Store the current page as text
        self.current_page = r.text

    def navigate_tt_page_dated(self, date):
        # Convert to compatible date string
        compatible_date = utils.datetime_to_estudent(date)
        # Get page data for navigating
        data = self.make_estudent_happy()
        # Add data to navigate to requested date
        data.update({
            'ctl00$Content$ctlFilter$TxtStartDt': compatible_date,
            'ctl00$Content$ctlFilter$BtnSearch': 'Refresh',
        })
        r = self.sess.post(TIMETABLE_URL, data=data, allow_redirects=False)
        r.raise_for_status()
        # Update current_page
        self.current_page = r.text
        # Update current_page_date
        self.current_page_date = date

    def advance_tt_page_one_week(self):
        date = self.current_page_date + datetime.timedelta(days=7)
        self.navigate_tt_page_dated(date)

    def get_this_monday(self):
        monday = datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().weekday())
        return monday

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

    def make_estudent_happy(self):
        """Extract required form values for POST requests."""
        values = {}
        soup = BeautifulSoup(self.current_page, "lxml")

        for name in '__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION':
            values[name] = soup.find(id=name)['value']
        return values
