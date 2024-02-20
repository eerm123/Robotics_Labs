# -*- coding: utf-8 -*-

# Feel free to add variables and helper functions to this file.
# Do NOT rename or remove the given functions!
values = []

def moving_average(pos):
    """
    Do NOT rename or remove this function!
    Implement a moving average filter.
    :param pos: The latest value that is passed to the filter
    :return: The filtered value
    """
    values.append(pos)
    
    if len(values) > 50:
        values.pop(0)
    average = sum(values) / len(values)
    print(average)
    
    return average