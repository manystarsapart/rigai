import pandas as pd
import numpy as np
from enum import Enum

def create_enum_from_list(enum_name: str, values: list):
    '''
    Creates an Enum class using a list of unique values.
    To be used in concurrence with Pydantic classes.
    '''
    enum_dict = {v.lower().replace(" ", "_").replace("+", "plus").replace("-", "_"): v for v in values}
    return Enum(enum_name, enum_dict)

def get_colours(colour_array: list):
    ''' 
    Obtains a list of all unique colours from a list containing values 
    such as "Black" or "White / Gray", where colours are separated with slashes.
    '''
    l = [list(map(str.strip, entry.split('/'))) for entry in colour_array]
    return list(set(np.hstack([x for x in l])))

def convert_to_enum_name(s: str):
    ''' 
    Converts string value to its corresponding Enum value.
    '''
    if isinstance(s, str):
        return s.lower().replace(" ", "_").replace("+", "plus").replace("-", "_")
    return s