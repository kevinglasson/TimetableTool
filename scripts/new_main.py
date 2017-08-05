#!/usr/bin/env python

import requests
import requests.packages.urllib3
import getpass
import gcal
import curtin_estudent
import scraper


def main():
    """Get user input and control the program."""
    # Just for me so I don't have to see warning about my python being old!
    requests.packages.urllib3.disable_warnings()

    username = raw_input('OASIS Username: ')
    password = getpass.getpass('OASIS Password: ')
    calendar_name = raw_input('Name of calendar to be created: ')

    session = curtin_estudent.Session()
    session.login(username, password)
    session.navigate_tt_page()

    scrape = scraper.Scraper(session.current_page)

    tt_events = scrape.proc_timetable_page()
    print(scrape.current_page_date)
    session.advance_tt_page_one_week()
    scrape.update_current_page(session.current_page)

    tt_events = scrape.proc_timetable_page()
    print(scrape.current_page_date)
    session.advance_tt_page_one_week()
    scrape.update_current_page(session.current_page)

    tt_events = scrape.proc_timetable_page()
    print(scrape.current_page_date)

    print('Successfully Completed')


if __name__ == '__main__':
    main()
