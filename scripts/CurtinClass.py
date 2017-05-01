#!/usr/bin/env python
"""Class to hold all of the information for describing a class at my university.

Contains the following functions to add and display the information stored in
an instance of this class

def proc_info(self, info)

def to_string(self)

"""


class CurtinClass():
    """Class to hold all of the information for describing a class at my uni."""

    def __init__(self, info=None):
        """Initialise and set to defaults, process info if provided."""
        self.type = "No class"
        self.date = "No class scheduled"
        self.start = "No class scheduled"
        self.end = "No class scheduled"
        self.location = "No bldg or room assigned"
        if info is not None:
            self.proc_info(info)

    def proc_info(self, info):
        """Extract information from a formatted dictionary."""
        self.type = info['type']
        self.date = info['date']
        self.start = info['start']
        self.end = info['end']
        self.location = info['location']

    def to_string(self):
        """Print out all of the information contained within and instance."""
        print "Class type: " + self.type
        print "Class date: " + self.date
        print "Start time: " + self.start
        print "End time: " + self.end
        print "Location ('Bldg' 'Room'): " + self.location
