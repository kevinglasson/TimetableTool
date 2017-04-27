#!/usr/bin/env python

# This will be  a class to hold all of the information for describing a class
# at my university including type, time and location

import re


class CurtinClass():
    def __init__(self, string):
        # TODO: Set the defaults to 'No Class, and NA' etc so they can be left
        # as is when there are no classes on
        self.type = "No class"
        self.day = "No class scheduled"
        self.start_time = "No class scheduled"
        self.end_time = "No class scheduled"
        self.location = ["No bldg or room assigned"]
        # Will need to use dates at some point
        # self.date =
        # Fill variables with actual data
        self.proc_string(string)

    # TODO: Fix CurtinClass so it can handle when classes have no information or
    # are not on, like in Bec's case where my script crashed!
    # Use a try except on the index error to accomplish this
    # try:
    #     gotdata = dlist[1]
    # except IndexError:
    #     gotdata = 'null'

    def proc_string(self, string):
        # Get the type
        try:
            # This should get the type of class even if there is none scheduled
            try:
                self.type = re.findall(r".+?(?=  Registered)", string)[0]
            except:
                self.type = re.findall(r".+?(?=  There)", string)[0]
            # Get the start and end times from the string
            # print "String checked: " + string
            # print "Times Found: \n"
            # print re.findall(r"[0-9]{1}:[0-9]{2} .m", string)
            # print "\n"
            # temp_lst = re.findall(r"[0-9]{2}:[0-9]{2} .m", string)
            # print temp_lst
            # self.start_time = temp_lst[0]
            # self.end_time = temp_lst[1]
            # print "\n" + self.start_time
            # print "\n" + self.end_time
            self.day = re.findall(r"(\w+day)", string)[0]
            self.start_time = re.findall("[0-9]*:[0-9]* .m", string)[0]
            self.end_time = re.findall("[0-9]*:[0-9]* .m", string)[1]
            # Get the location as a string "Bldg Room"
            # For some reason this is staying as a list with one object
            # I have tried putting an index at the end like those above but it does
            # not want to work
            self.location = re.findall(r"(\d+.? \d+)(?!=Location:)", string)
        except IndexError:
            print "\nIndexing error, data will be set to defaults"

    def to_string(self):
        print "Class type: " + self.type
        print "Class day: " + self.day
        print "Start time: " + self.start_time
        print "End time: " + self.end_time
        print "Location ('Bldg' 'Room'): " + self.location[0]
