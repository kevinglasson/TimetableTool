#!/usr/bin/env python

# For getting the website
import requests

# Disable warnings that are due to the old version of python
import requests.packages.urllib3

# For hiding the user password on entry
import getpass

# For grabbing the tables
import pandas as pd

from CurtinUnit import CurtinUnit


def retrieve_timetable_page():

    login_succeeded = False

    with requests.Session() as sesh:
        base_url = 'https://oasis.curtin.edu.au/'
        auth_url = 'https://oasis.curtin.edu.au/Auth/Logon'

        # Get the username and password and attempt to log in
        # Get the url that we are on and check that it is the same as the base_url
        # if it is not then we have not managed to log in so retry
        while not login_succeeded:
            USERNAME = raw_input("USERNAME: ")
            PASSWORD = getpass.getpass("PASSWORD: ")

            sesh.get(auth_url)

            # Create login data
            login_data = dict(UserName=USERNAME, Password=PASSWORD)

            # This is the part where we attempt to login to the page
            main_page = sesh.post(
                auth_url,
                data=login_data,
                headers={"Referer": "https://oasis.curtin.edu.au"})

            if not main_page.url == base_url:
                print "\nFAILED: TRY AGAIN \n"
            else:
                print "\nSUCCESS: lOGGED IN \n"
                login_succeeded = True

        # Navigate to the 'My Studies' tab
        my_studies_page = sesh.post('https://oasis.curtin.edu.au/MyStudies')

        # Navigate to the 'eStudent'
        estudent_page = sesh.get('https://estudent.curtin.edu.au/eStudent/')

        # Navigate to the 'My Classes' tab
        time_table_page = sesh.get(
            'https://estudent.curtin.edu.au/eStudent/SM/StudentTtable10.aspx?r=%23CU.ESTU.STUDENT&f=%23CU.EST.TIMETBL.WEB'
        )

        return time_table_page


# def filter_timetable_date(time_table_page):
#
#     date_data = {}
#
# with requests.Session() as sesh:
#     request_date_page = sesh.post(
#         auth_url,
#         data=date_data,
#         headers={
#             "Referer":        "https://estudent.curtin.edu.au/eStudent/SM/StudentTtable10.aspx?r=%23CU.ESTU.STUDENT&f=%23CU.EST.TIMETBL.WEB"
#         })


def extract_units(filtered_time_table_page):
    # Before we extract the tables from the page we need to navigate to the
    # correct date and record that date, we then need to extract the tables
    # from the page and process them against that date, from this we can attach # a date to each class based on the list of Monday dates in the
    # ../data/monday_dates.csv file
    dfs = pd.read_html(filtered_timetable_page.text)
    unit_dfs = []
    # Remove unwanted columns from all of the dataframes and print to the console
    for i, df in enumerate(dfs):
        # This is to delete and empty dataframes we have grabbed
        if df.empty:
            del df
        # This is the table that contains the unit code and the unit name
        # probably best to seperate it here while we have access
        elif i % 2 == 0:
            df.drop(df.columns[[0, 3, 4, 5, 6]], axis=1, inplace=True)
        # This is the table that contains the information string for the [i-1]th unit, the string will need to be parse and the information extracted at this point as we
        # have easy access
        else:
            df.drop(df.columns[[0]], axis=1, inplace=True)
            # This is to combine the unit title table into the same dataframe
            # as the info. It appears to work although column 2 has NaN's, but
            # that doesn't matter
            temp_lst = [dfs[i - 1], dfs[i]]
            unit_dfs.append(pd.concat(temp_lst))

    # This corrects the indexes after joining the tables together
    for i, df in enumerate(unit_dfs):
        unit_dfs[i] = df.reset_index(drop=True)

    # To store the CurtinUnit objects we are about to create
    unit_list = []

    for i, df in enumerate(unit_dfs):
        temp_object = CurtinUnit(df)
        unit_list.append(temp_object)

        return unit_list


def print_units(unit_list):
    for unit in unit_list:
        print "------------------------------------------------------------------\n"
        unit.to_string()


if __name__ == '__main__':
    # Just for me so I don't have to see warning about my python being old!
    requests.packages.urllib3.disable_warnings()

    # Get timetable page
    timetable_page = retrieve_timetable_page()

    # For mondays in .csv file
    filtered_timetable_page = filter_timetable_date()

    unit_list = extract_units(timetable_page)
    print_units(unit_list)

# Mmmm Boiiii all the info is in my datastructure!

# TODO: Now I can clean this horrible mess of a main function up a bit before
# processing this information and some how getting it into a google calendar!

# TODO: Fix CurtinClass so it can handle when classes have no information or
# are not on
