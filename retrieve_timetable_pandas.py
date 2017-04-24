#!/usr/bin/env python

##For getting the website
import requests

##Disable warnings that are due to the old version of python
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

##For hiding the user password on entry
import getpass

##For grabbing the tables
import pandas as pd

login_succeeded = False

##Just for me so I can viualise the data while troubleshooting in terminal
pd.set_option('display.width', 1000)

with requests.Session() as sesh:
    base_url = 'https://oasis.curtin.edu.au/'
    auth_url = 'https://oasis.curtin.edu.au/Auth/Logon'

##    Get the username and password and attempt to log in
##    Get the url that we are on and check that it is the same as the base_url
##    if it is not then we have not managed to log in so retry
    while not login_succeeded:
        USERNAME = raw_input("USERNAME: ")
        PASSWORD = getpass.getpass("PASSWORD: ")
        
        sesh.get(auth_url)

##        Create login data
        login_data = dict(UserName=USERNAME, Password=PASSWORD)

##        This is the part where we attempt to login to the page
        main_page = sesh.post(
            auth_url,
            data=login_data,
            headers={"Referer": "https://oasis.curtin.edu.au"})

        if not main_page.url == base_url:
            print "\nFAILED: TRY AGAIN \n"
        else: 
            print "\nSUCCESS: lOGGED IN \n"
            login_succeeded = True

##    Navigate to the 'My Studies' tab
    my_studies_page = sesh.post('https://oasis.curtin.edu.au/MyStudies')

##    Navigate to the 'eStudent'
    estudent_page = sesh.get('https://estudent.curtin.edu.au/eStudent/')

##    Navigate to the 'My Classes' tab
    time_table_page = sesh.get(
        'https://estudent.curtin.edu.au/eStudent/SM/StudentTtable10.aspx?r=%23CU.ESTU.STUDENT&f=%23CU.EST.TIMETBL.WEB'
    )
    
    dfs = pd.read_html(time_table_page.text)

##    Remove unwanted columns from all of the dataframes and print to the console
    for i, df in enumerate(dfs):
##        This is to delete and empty dataframes we have grabbed
        if df.empty:
            del df
##        This is the table that contains the unit code and the unit name, probably
##        best to seperate it here while we have access
        elif i % 2 == 0:
            df.drop(df.columns[[0, 3, 4, 5, 6]], axis = 1, inplace = True)
##        This is the table that contains the information string for the [i-1]th unit, the
##        string will need to be parse and the information extracted at this point as we
##        have easy access
        else:
            df.drop(df.columns[[0]], axis = 1, inplace = True)
##        print df.to_string(index = False)

##Printing out to see where I am at, this is printing dataframe position 1, column 1, row 3
##I think there is a way in pandas to do this that may be more efficient however, but this
##does work if needed

##print "\n" + dfs[1][1][3] + "\n"

for df in dfs:
    print df.to_string(index = False, header = False)
    print "\n\n"

#Now I need to parse the strings in the even tables
