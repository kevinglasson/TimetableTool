#!/usr/bin/env python

# This will be a class to hold the information that is required to describe
# a 'unit' at my university, it may also contain methods to process this info
# from a pandas dataframe of my making

import re
from CurtinClass import CurtinClass


class CurtinUnit():
    def __init__(self, data_frame):
        # Set up variables to defaults and then call process_df
        self.unit_code = "Default"
        self.unit_name = "Default"
        self.class_list = []

        # Fill variables with the data
        self.proc_df(data_frame)

    def proc_df(self, df):
        self.unit_code = df.loc[0, 1]
        self.unit_name = df.loc[0, 2]

        self.proc_class_strings(df)

    def proc_class_strings(self, df):
        df_index_lst = df.index.values
        for i in range(2, len(df_index_lst)):
            self.class_list.append(CurtinClass(df.loc[i, 1]))

    def to_string(self):
        print "Unit code: " + self.unit_code
        print "Unit name: " + self.unit_name
        for cls in self.class_list:
            print "------------------------------------------------------------------"
            cls.to_string()
