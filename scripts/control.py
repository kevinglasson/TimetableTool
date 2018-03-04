import requests.packages.urllib3
import gcal
import curtin_estudent
import scraper
import constants


def main(username, password, calendar_name, token):
    # Disable warnings
    requests.packages.urllib3.disable_warnings()

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
    create_calendar(event_list, calendar_name, token)
    # Completed
    print('Successfully Completed')
    return 'Successfully Completed'


def create_calendar(event_list, calendar_name, token):
    cal_id = gcal.create_calendar(calendar_name, token)
    for lst in event_list:
        for event in lst:
            gcal.add_event(event, cal_id, token)


def attach_colours_to_units(event_list):
    unit_names = []
    for lst in event_list:
        for item in lst:
            if item['summary'].split()[0] not in unit_names:
                unit_names.append(item['summary'].split()[0])
            item['colorId'] = constants.COLORS[unit_names.index(item['summary'].split()[0])]