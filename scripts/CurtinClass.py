#!/usr/bin/env python

# This will be  a class to hold all of the information for describing a class
# at my university including type, time and location


class CurtinClass():
    def __init__(self, info=None):
        self.type = "No class"
        self.date = "No class scheduled"
        self.start = "No class scheduled"
        self.end = "No class scheduled"
        self.location = "No bldg or room assigned"
        if info is not None:
            self.proc_info(info)

    def proc_info(self, info):
        self.type = info['type']
        self.date = info['date']
        self.start = info['start']
        self.end = info['end']
        self.location = info['location']

    def to_string(self):
        print "Class type: " + self.type
        print "Class date: " + self.date
        print "Start time: " + self.start
        print "End time: " + self.end
        print "Location ('Bldg' 'Room'): " + self.location
