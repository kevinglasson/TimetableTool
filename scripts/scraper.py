from bs4 import BeautifulSoup
import utilities as utils
import datetime
import constants


class Scraper():

    def __init__(self, current_page=None):
        self.current_page = current_page
        self.current_page_date = None

    # Scrape and return the contents of the current page
    def proc_timetable_page(self):
        soup = BeautifulSoup(self.current_page, 'lxml')
        event_lst = {}

        # Find and process each 'day' in the timetable
        for day in constants.DAYS:
            column = soup.find(
                id='ctl00_Content_ctlTimetableMain_{}DayCol_Body'.format(day))

            for item in column.find_all(class_='cssClassInnerPanel'):
                event = {
                    'summary': self.get_summary(item),
                    'location': self.get_location(item),
                    'start': {
                        'dateTime': self.get_start_datetime(item)
                    },
                    'end': {
                        'dateTime': self.get_end_datetime(item)
                    },
                }
                event_lst.append(event)
        return(event_lst)

        def get_summary(item):
            unit_code = item.find(class_='cssTtableHeaderPanel').string.strip()
            _type = item.find(class_='cssTtableitemSlotWhat').string
            summary = '{} - {}'.format(unit_code, _type.capitalize())
            return summary

        def get_location(item):
            location = item.find(class_='cssTtableitemSlotWhere').string
            return location

        def get_start_datetime(item):
            date = utils.date_from_day_abbr(day, self.current_page_date)
            time = utils.to_24h_string(item.find(class_='cssHiddenStartTm')['value'])
            date_string = utils.to_gcal_datetime(date, time)
            return date_string

        def get_end_datetime(item):
            date = utils.date_from_day_abbr(day, self.current_page_date)
            time = utils.to_24h_string(item.find(class_='cssHiddenEndTm')['value'])
            date_string = utils.to_gcal_datetime(date, time)
            return date_string

        def get_page_date(self):
            soup = BeautifulSoup(self.current_page, 'lxml')

            self.current_page_date = soup.find(id='ctl00_Content_ctlFilter_TxtStartDt')['value']
