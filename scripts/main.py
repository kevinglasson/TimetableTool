#!/usr/bin/env python

import requests
import requests.packages.urllib3
import getpass
import gcal
import curtin_estudent
import scraper
import constants


def main():
    username = raw_input('OASIS Username: ')
    password = getpass.getpass('OASIS Password: ')
    calendar_name = raw_input('Name of calendar to be created: ')

    # Initialise session and scraper
    session = curtin_estudent.Session()
    getter = scraper.Scraper()
    # Login
    print('Logging in....')
    session.login(username, password)
    # Navigate to timetable
    print('Finding timetables')
    session.navigate_tt_page()
    # Scrape first timetable
    print('Scraping timetables')
    event_list = [getter.scrape_timetable_page(session.current_data)]
    # Scrape timetables until there are no more
    while getter.consecutive_empty_scrapes < 5:
        session.advance_tt_page_one_week()
        event_list.append(getter.scrape_timetable_page(session.current_data))
    # Select and attach the same colour to each unit
    print('Attaching unit colours')
    attach_colours_to_units(event_list)
    # Create and publish the calendar to Google Calendar
    print('Creating calendar')
    print('Please wait....')
    create_calendar(event_list, calendar_name)
    # Completed
    print('Successfully Completed')


def create_calendar(event_list, calendar_name):
    cal_id = gcal.create_calendar(calendar_name)
    for lst in event_list:
        for event in lst:
            gcal.add_event(event, cal_id)


def attach_colours_to_units(event_list):
    unit_names = []
    for lst in event_list:
        for item in lst:
            if item['summary'].split()[0] not in unit_names:
                unit_names.append(item['summary'].split()[0])
            item['colorId'] = constants.COLORS[unit_names.index(item['summary'].split()[0])]


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    main()
