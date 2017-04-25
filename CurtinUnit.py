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


# >>> print unit_dfs[4].loc[0, 1]
# MXEN2002

# >>> print unit_dfs[4].loc[0, 2]
# Mechatronics Microcontroller Project

# >>> print unit_dfs[4].loc[2, 1]
# Lecture  Registered Class 1 Time: Monday 11:00 am-12:00 pm Location: Bentley Campus 408 2038>>> print unit_dfs[4].loc[2, 1]
