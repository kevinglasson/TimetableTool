#!/usr/bin/env python

# This will be a class to hold the information that is required to describe
# a 'unit' at my university

from CurtinClass import CurtinClass


class CurtinUnit():
    def __init__(self, info=None):
        self.unit_code = "Default"
        self.class_list = []

        if info is not None:
            self.proc_info(info)

    def proc_info(self, info):
        self.unit_code = info['unit_code']
        self.class_list.append(CurtinClass(info))

    def add_class(self, info):
        self.class_list.append(CurtinClass(info))

    def to_string(self):
        print "Unit code: " + self.unit_code
        for class_ in self.class_list:
            print "------------------------------------------------------------------"
            class_.to_string()
