#!/usr/bin/env python
"""The CUeStudentSession class and associated functions.

This class contains and stores all functions and variables necessary
for interacting with Curtin's eStudent portal. It accessess and extracts
the timetable information for the provided login details and stores them
in a CurtinUnit object

it contains the following public usable functions: (See the function docstring
for further information)

class CUeStudentSession(object):

def login(self, studentid, password):

def get_timetables(self):

def get_all_timetables(self):

"""

from __future__ import print_function
from bs4 import BeautifulSoup
from CurtinUnit import CurtinUnit
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


class LoginFailedError(Exception):
    """Store the html response code on login exception."""

    def __init__(self, response):
        """Store the respose code in instance variable."""
        self.response = response


class CUeStudentSession(object):
    """Form a requests session for Curtin eStudent.

    This class contains and stores all functions and variables necessary
    for interacting with Curtin's eStudent portal. It accessess and extracts
    the timetable information for the provided login details and stores them
    in a CurtinUnit object

    """

    def __init__(self):
        """Create the necessary variables for a session.

        Initialises requests session and sets instance variables to defaults

        """
        self.sess = requests.Session()
        self.timetable_page = None
        # To hold the date of the 'Monday, can figure the rest from that!'
        self.timetable_page_mon_date = None
        self.consecutive_empty_weeks = 0

    # Login
    def login(self, studentid, password):
        """Log in to Curtin Oasis provided a username and password.

        Navigates to the login page and accesses the page with the provided
        username and password, raises a LoginFailedError if login was not
        successful

        Keyword arguments:
        studentid -- The students id number
        password -- The students password

        """
        r = self.sess.get(LOGIN_URL)
        data = dict(UserName=studentid, Password=password)
        r = self.sess.post(LOGIN_URL, data=data, allow_redirects=False)

        # Checks the response code and raise a custom error if login was unsuccessful
        if r.status_code != requests.codes.found:
            raise LoginFailedError(r)
        else:
            print('\nLogin successful \n')

    # Either navigate to the timetable page the first time, or just return the
    # current timetable page
    def get_timetable_page(self):
        """Navigate to the page with the timetable on it."""
        if not self.timetable_page:
            # Navigate to the 'My Studies' tab
            r = self.sess.post(MY_STUDIES_URL)
            # Navigate to the 'eStudent'
            r = self.sess.get(ESTUDENT_URL)
            # Navigate to the 'My Classes' tab
            r = self.sess.get(TIMETABLE_URL)
            self.timetable_page = r.text
            self.set_default_date()

    # TODO: Implement this, so that we can navigate to a specific date to get
    # the timetable for that week 04-May-2017
    def set_timetable_page_dated(self, date):
        """Navigate to a timetable of a specific date.

        Keyword arguments:
        date -- The date to navigate to

        """
        tt_page = self.timetable_page
        date = from_datetime(date)
        data = make_estudent_happy(tt_page)
        data.update({
            'ctl00$Content$ctlFilter$TxtStartDt': date,
            'ctl00$Content$ctlFilter$BtnSearch': 'Refresh',
        })
        r = self.sess.post(TIMETABLE_URL, data=data, allow_redirects=False)
        r.raise_for_status()
        self.timetable_page = r.text
        return r.text

    def set_default_date(self):
        """Set the initial date of the timetable page.

        It is necessary to obtain the first date a different way. After the
        initial date is established all future dates can be calculated.

        """
        page = self.timetable_page
        soup = BeautifulSoup(page, "lxml")
        select = soup.find(
            id='ctl00_Content_ctlFilter_CboStudyPeriodFilter_elbList')
        option = select.find_all('option')
        # '2017-1-May 01, 2017'
        string = option[2]['value']
        # datetime.date(2017, 5, 1)
        date = datetime.datetime.strptime(string[7:], '%b %d, %Y').date()
        date = date - datetime.timedelta(days=date.weekday())
        self.timetable_page_mon_date = date
        print('MONDAY DATE IS {}'.format(date))

    def inc_mon_date(self):
        """Move the monday date forward 7 days.

        Increment the monday date by 7 days, because the scrape happens in 1
        week blocks this will set the next monday date to be navigated to.

        """
        print(
            'processed week starting: {}'.format(self.timetable_page_mon_date))
        print('\n')
        mon_date = self.timetable_page_mon_date + datetime.timedelta(days=7)
        self.timetable_page_mon_date = mon_date

    def get_timetable(self):
        """Get navigate to the timetable page.

        Process the default timetable page navigated to, this will be the timetable of the week containing todays date, this will only get that
        timetable, nothing more.

        """
        self.get_timetable_page()
        return self.proc_timetable_page()

    def get_all_timetables(self):
        """Get all of the timetables for the study period.

        This will process timetables until it finds 3 consectuive empty weeks.
        This signals the end of that study period and will not break when there
        is a 2 week tuition free period. Returns the entire list of dictionaries
        to the caller.
        """
        sem_unit_lst = []
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

    # This is good, each class can be assigned it's date at this point because
    # it is going day by day. Just need to write a get_date function
    def proc_timetable_page(self):
        """Process the timetable page to extract the desired information.

        Returns a dict containing the units that were found in the timetable.
        The key of the dictionary is the unit code and each unit is contained
        in a CurtinUnit object.

        """
        page = self.timetable_page
        soup = BeautifulSoup(page, "lxml")
        unit_lst = {}

        for day in SCHOOLDAYS:
            column = soup.find(
                id='ctl00_Content_ctlTimetableMain_%sDayCol_Body' % day)

            for cls in column.find_all(class_='cssClassInnerPanel'):
                info = {
                    'date':
                    date_from_day_abbr(day, self.timetable_page_mon_date),
                    'start':
                    to_24h(cls.find(class_='cssHiddenStartTm')['value']),
                    'end':
                    to_24h(cls.find(class_='cssHiddenEndTm')['value']),
                    'type':
                    cls.find(class_='cssTtableClsSlotWhat').string,
                    'location':
                    cls.find(class_='cssTtableClsSlotWhere').string,
                    'unit_code':
                    cls.find(class_='cssTtableHeaderPanel').string.strip(),
                }
                if info['unit_code'] in unit_lst:
                    unit_lst[info['unit_code']].add_class(info)
                else:
                    unit_lst[info['unit_code']] = CurtinUnit(info)

        self.check_for_empty_week(unit_lst)
        return unit_lst


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


def date_from_day_abbr(string, mon_date):
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
    return from_datetime(date)


def from_datetime(date):
    """Take a datetime object and return a compatible string.

    A compatible string is one in the format dd.mm.yyyy. It is necessary for
    navigating to the required timetable page.

    """
    month_abbr = ''
    for i, month in enumerate(MONTHS):
        if date.month == i + 1:
            month_abbr = month
    string = "{}-{}-{}".format(date.day, month_abbr, date.year)
    return string


# 04-May-2017
def to_datetime(string):
    """Take a date in string form and return a datetime object.

    Converting date in string format to a datetime object as it is cleaner than
    storing a string, and easier to access.

    """
    # datetime.date(2017, 5, 4)
    date = datetime.datetime.strptime(string, '%d-%b-%Y').date()
    return date
