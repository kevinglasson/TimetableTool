from bs4 import BeautifulSoup
import utilities as utils
import datetime
import constants


class Scraper():

    def __init__(self, page):
        self.current_page = page
        self.current_page_date = None

    def update_current_page(self, new_page):
        self.current_page = new_page

    # Scrape and return the contents of the current page
    def proc_timetable_page(self):
        self.get_page_date()
        soup = BeautifulSoup(self.current_page, 'lxml')
        event_lst = []

        # Find and process each 'day' in the timetable
        for day in constants.DAYS:
            column = soup.find(
                id='ctl00_Content_ctlTimetableMain_{}DayCol_Body'.format(day))

            for item in column.find_all(class_='cssClassInnerPanel'):
                event = {
                    'summary': self.get_summary(item),
                    'location': self.get_location(item),
                    'start': {
                        'dateTime': self.get_start_datetime(item, day)
                    },
                    'end': {
                        'dateTime': self.get_end_datetime(item, day)
                    },
                }
                event_lst.append(event)
        return(event_lst)

    def get_summary(self, item):
        unit_code = item.find(class_='cssTtableHeaderPanel').string.strip()
        _type = item.find(class_='cssTtableClsSlotWhat').string
        summary = '{} - {}'.format(unit_code, _type.capitalize())
        return summary

    def get_location(self, item):
        location = item.find(class_='cssTtableClsSlotWhere').string
        return location

    def get_start_datetime(self, item, day):
        date = utils.date_from_day_abbr(day, self.current_page_date)
        time = utils.to_24h_string(item.find(class_='cssHiddenStartTm')['value'])
        date_string = utils.to_gcal_datetime(date, time)
        return date_string

    def get_end_datetime(self, item, day):
        date = utils.date_from_day_abbr(day, self.current_page_date)
        time = utils.to_24h_string(item.find(class_='cssHiddenEndTm')['value'])
        date_string = utils.to_gcal_datetime(date, time)
        return date_string

    def get_page_date(self):
        print('before if: {}'.format(self.current_page_date))
        if self.current_page_date is None:
            self.current_page_date = datetime.datetime.today()
            print('after if: {}'.format(self.current_page_date))
        else:
            soup = BeautifulSoup(self.current_page, 'lxml')
            print('in else loop')
            print(soup.find(id='ctl00_Content_ctlFilter_TxtStartDt')['Value'])
            self.current_page_date = utils.estudent_to_datetime(soup.find(id='ctl00_Content_ctlFilter_TxtStartDt')['Value'])

        # TODO: delete
        print('get_page_date date is: {}'.format(self.current_page_date))
