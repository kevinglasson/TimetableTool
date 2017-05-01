#!/usr/bin/env python
"""Class to hold the information to describe a unit at Curtin University.

Allows the creation of the CurtinUnit object and contains the following publicly
accessible methods to work with the CurtinUnit

def proc_info(self, info)

def add_class(self, info)

def to_string(self)
"""

from CurtinClass import CurtinClass


class CurtinUnit():
    """Class to hold the information to describe a unit at Curtin University.

    Contains functions to initialise the object and process formatted
    unit information

    """

    def __init__(self, info=None):
        """Initialise a new instance and process info if any provided."""
        self.unit_code = 'Default'
        self.class_list = []

        if info is not None:
            self.proc_info(info)

    def proc_info(self, info):
        """Extract information from a formatted dictionary."""
        self.unit_code = info['unit_code']
        self.class_list.append(CurtinClass(info))

    def add_class(self, info):
        """Add a CurtinClass object to this unit.

        unit's generally have multiple classes and so this is a way to add them

        """
        self.class_list.append(CurtinClass(info))

    def to_string(self):
        """Print out all of the information contained within and instance."""
        print "Unit code: " + self.unit_code
        for class_ in self.class_list:
            print "------------------------------------------------------------------"
            class_.to_string()
