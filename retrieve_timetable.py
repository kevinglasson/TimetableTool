#!/usr/bin/env python

import requests

## Disable warnings that are due to the old version of python
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup
import getpass

with requests.Session() as sesh:
    base_url = 'https://oasis.curtin.edu.au/'
    auth_url = 'https://oasis.curtin.edu.au/Auth/Logon'

##    Get the username and password
    USERNAME = raw_input("USERNAME: ")
    PASSWORD = getpass.getpass("PASSWORD: ")
    
    sesh.get(auth_url)

##    Create login data
    login_data = dict(UserName=USERNAME, Password=PASSWORD)

##    This is the part where we attempt to login to the page
    page = sesh.post(
        auth_url,
        data=login_data,
        headers={"Referer": "https://oasis.curtin.edu.au"})

##    Get the url that we are on and check that it is the same as the base_url
##    if it is not then we have not managed to log in
    if page.url == base_url:
        print "SUCCESS: lOGGED IN"

##    Navigate to the 'My Studies' tab
    my_studies = sesh.post('https://oasis.curtin.edu.au/MyStudies')

##    Navigate to the 'eStudent'
    estudent = sesh.get('https://estudent.curtin.edu.au/eStudent/')

##    Navigate to the 'My Classes' tab
    time_table = sesh.get(
        'https://estudent.curtin.edu.au/eStudent/SM/StudentTtable10.aspx?r=%23CU.ESTU.STUDENT&f=%23CU.EST.TIMETBL.WEB'
    )

    table_soup = BeautifulSoup(time_table.content, "html.parser")

    tables = table_soup.find_all('table')

    tables_seperated = []

##    The unit Name has been saved in a Table[0] and the details of the classes
##    are in Table[1], I need to fix this here. I think it is because they are actually
##    seperate tables on the website so all I need to do is just join them!
    for i, table in enumerate(tables):
        tables_seperated.append([])
        for row in table.find_all('tr'):
            for data in row.find_all('td'):
                strip = data.text
                strip = strip.strip()
                strip = strip.replace("\n", "")
                strip = strip.replace("\t", " ")
                strip = strip.replace("\r", "")
                if not strip == "":
                    tables_seperated[i].append(strip)
                    
##    Still need to join them though

    unit_tables = []

    for i, table in enumerate(tables_seperated):
        if i % 2 == 0:
            unit_tables.append(tables_seperated[i] + tables_seperated[i+1])

    for units in unit_tables:
        print "\n"
        for info in units:
            print info

##    This is printing out fairly well, I will need to write a class to hold my unit
##    information so that it can be cleanly accessed, I can probably clean up some of
##    this code as will as it looks very messy!!
##
##    But this is a good start!
