# coding: utf-8
"""
Some utilities 
"""

import math
def find_precision(number):
    # https://stackoverflow.com/questions/3018758/determine-precision-and-scale-of-particular-number-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    max_digits = 14
    int_part = int(number)
    magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
    if magnitude >= max_digits:
        return (magnitude, 0)

    frac_part = abs(number) - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10

    scale = int(math.log10(frac_digits))
    return (magnitude+scale, scale)


def str_to_int(events):
    evt_type = type(events)
    if evt_type is int:
        return events
    elif evt_type is not unicode and\
            evt_type is not str:
        return -1
    else:
        events = events.lower()

    if "m" in events:
        res = events.replace('m', "000000")
    elif 'k' in events:
        res = events.replace('k', '000')
    else:
        res = events

    try:
        res = int(res)
    except ValueError:
        print(events, "is not a good input")
        res = -1

    return res


def nersc_hours(queue_name, hours, nnodes, njobs):
    """
    only valid for Haswell
    """
    charge_factor = 0
    if 'regular' in queue_name or 'debug' in queue_name:
        charge_factor = 80
    elif 'shared' in queue_name:
        charge_factor = 2.5
    else:
        print("I don't know which queue you are in")

    return charge_factor*hours*nnodes*njobs
