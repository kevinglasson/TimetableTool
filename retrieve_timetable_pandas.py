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

login_succeeded = False

# Just for me so I don't have to see warning about my python being old!
requests.packages.urllib3.disable_warnings()

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

    dfs = pd.read_html(time_table_page.text)

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

# Printing out to see where I am at, this is printing dataframe position
# 1, column 1, row 3
# I think there is a way in pandas to do this that may be more efficient
# however, but this does work if needed

# print "\n" + dfs[1][1][3] + "\n"

for i, df in enumerate(unit_dfs):
    # print df.to_string(index = False, header = False)
    # This corrects the indexes after joining the tables together
    unit_dfs[i] = df.reset_index(drop=True)
    print df.to_string()
    print "\n\n"

# Now I need to parse the strings in the even tables
my_unit_list = []

for i, df in enumerate(unit_dfs):
    temp_object = CurtinUnit(df)
    my_unit_list.append(temp_object)

print "Check my datastructure"
print "Unit code: " + my_unit_list[0].unit_code
print "Unit name: " + my_unit_list[0].unit_name
print "Class type: " + my_unit_list[0].class_list[0].type
print "Start time: " + my_unit_list[0].class_list[0].start_time
print "End time: " + my_unit_list[0].class_list[0].end_time
print "Location ('Bldg' 'Room'): " + my_unit_list[0].class_list[0].location[0]

# Mmmm Boiiii all the info is in my datastructure!

# TODO: Now I can clean this horrible mess of a main function up a bit before
# processing this information and some how getting it into a google calendar!

# TODO: Fix CurtinClass so it can handle when classes have no information or
# are not on
