import pandas as pd

def get_list_for_SQL_string(input_list: list = None, separator = ','):
    return separator.join("'" + str(i) + "'" for i in input_list)

def get_list_for_SQL_nstring(input_list: list = None, separator = ','):
    return separator.join("N'" + str(i) + "'" for i in input_list)

def get_list_for_SQL_number(input_list: list = None, separator = ','):
    return separator.join(str(i) for i in input_list)

def get_list_for_SQL_column(input_list: list = None, separator = ','):
    return separator.join("[" + str(i) + "]" for i in input_list)

def get_list_for_display(input_list: list = None, separator = ', '):
    return separator.join(str(i) for i in input_list)