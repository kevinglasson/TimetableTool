from __future__ import print_function
from bs4 import BeautifulSoup
from CurtinUnit import CurtinUnit
import datetime
import getpass
import requests
import pandas as pd

LOGIN_URL = 'https://oasis.curtin.edu.au/Auth/Logon'
OASIS_URL = 'https://oasis.curtin.edu.au/'
MY_STUDIES_URL = 'https://oasis.curtin.edu.au/MyStudies'
ESTUDENT_URL = 'https://estudent.curtin.edu.au/eStudent/'
TIMETABLE_URL = 'https://estudent.curtin.edu.au/eStudent/SM/StudentTtable10.aspx?r=%23CU.ESTU.STUDENT&f=%23CU.EST.TIMETBL.WEB'
MONTHS = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
    'Nov', 'Dec'
]
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
TZ = 'Australia/Sydney'


class LoginFailedError(Exception):
    def __init__(self, response):
        self.response = response


class CUeStudentSession(object):
    def __init__(self):
        self.sess = requests.Session()
        self.timetable_page = None
        # To hold the date of the 'Monday, can figure the rest from that!'
        self.timetable_page_mon_date = None

    # Login
    def login(self, studentid, password):
        r = self.sess.get(LOGIN_URL)
        data = dict(UserName=studentid, Password=password)
        r = self.sess.post(LOGIN_URL, data=data, allow_redirects=False)

        # Checks the response code and raise a custom error if login was unsuccessful
        if r.status_code != requests.codes.found:
            raise LoginFailedError(r)
        else:
            print('Login successful')

    # Either navigate to the timetable page the first time, or just return the
    # current timetable page
    def get_timetable_page(self):
        if not self.timetable_page:
            # Navigate to the 'My Studies' tab
            r = self.sess.post(MY_STUDIES_URL)
            # Navigate to the 'eStudent'
            r = self.sess.get(ESTUDENT_URL)
            # Navigate to the 'My Classes' tab
            r = self.sess.get(TIMETABLE_URL)
            self.timetable_page = r.text

    # TODO: Implement this, so that we can navigate to a specific date to get
    # the timetable for that week 04-May-2017
    def set_timetable_page_dated(self, date):
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
        self.set_mon_date()
        return r.text

    # Calculates the date of the day provided using the date of the monday
    # of the current timetable page!

    def set_mon_date(self):
        page = self.timetable_page
        soup = BeautifulSoup(page, "lxml")
        date = soup.find(id='ctl00$Content$ctlFilter$TxtStartDt')
        print(date)
        date = to_datetime(date)
        mon_date = date - datetime.timedelta(days=date.weekday())
        self.timetable_page_mon_date = mon_date

    def get_timetable(self):
        self.get_timetable_page()
        self.set_timetable_page_dated(datetime.date.today())
        return self.proc_timetable_page()

    # This is good, each class can be assigned it's date at this point because
    # it is going day by day. Just need to write a get_date function
    def proc_timetable_page(self):
        page = self.timetable_page
        soup = BeautifulSoup(page, "lxml")
        timetable = {}

        unit_lst = {}

        for day in DAYS:
            col = soup.find(
                id='ctl00_Content_ctlTimetableMain_%sDayCol_Body' % day)

            for cls in col.find_all(class_='cssClassInnerPanel'):
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

        return unit_lst


def make_estudent_happy(page):
    """Extract required form values for POST requests."""
    values = {}
    soup = BeautifulSoup(page, "lxml")

    for name in '__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION':
        values[name] = soup.find(id=name)['value']

    return values


def to_24h(time):
    am_pm = time[-2:].lower()
    hour, minute = time[:-2].split(':')
    hour = int(hour)
    if am_pm == 'pm' and hour != 12:
        hour += 12
    # Right align, pad with 0's and use 2 numbers always!
    return '{:>02}:{}'.format(hour, minute)


def date_from_day_abbr(self, string, mon_date):
    for i, day in enumerate(DAYS):
        if day == string:
            date = mon_date + datetime.timedelta(days=i)
            break
    return from_datetime(date)


def from_datetime(date):
    month_abbr = ''
    for i, month in enumerate(MONTHS):
        if date.month == i + 1:
            month_abbr = month
    string = "{}-{}-{}".format(date.day, month_abbr, date.year)
    return string


# 04-May-2017
def to_datetime(string):
    lst = string.split('-')
    for i, month in enumerate(MONTHS):
        if lst[1] == month:
            month_int = i
    return (datetime.date(lst[0], month_int, lst[2]))
