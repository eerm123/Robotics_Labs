#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from machine import Pin
import time

def show_row(row_number, columns, delay):
    row_pins[row_number - 1].value(0)
    
    for column in columns:
        col_pins[column - 1].value(1)
        
    time.sleep(delay)
    
    row_pins[row_number - 1].value(1)
    
    for column in columns:
        col_pins[column - 1].value(0)
    
    
def main():
    global row_pins, col_pins

    # define row and column pin numbers
    row_pin_numbers = [7, 11, 6, 9, 0, 5, 1]
    col_pin_numbers = [10, 2, 3, 8, 4]

    row_pins = []
    col_pins = []

    # set all the pins as outputs and set column pins high, row pins low
    for row_number in row_pin_numbers:
        row_pins.append(Pin(row_number, Pin.OUT, value = 1))

    for col_number in col_pin_numbers:
        col_pins.append(Pin(col_number, Pin.OUT, value = 0))

    # Sets the waiting time between rows
    wait_time = 2

    # Displays image 50 times
    i = 0
    
    while i < 50:
        col_pins[0].value(1)
        col_pins[2].value(1)
        col_pins[4].value(1)
        row_pins[1].value(0)
        row_pins[1].value(0)
        row_pins[1].value(0)
        
        i += 1
        
    time.sleep(wait_time)
    i = 0
    while i < 200:
        show_row(1, [1, 2, 3, 4, 5], 0.001)
        show_row(2, [5], 0.001)
        show_row(3, [5], 0.001)
        show_row(4, [1, 2, 3, 4, 5], 0.001)
        show_row(5, [5], 0.001)
        show_row(6, [5], 0.001)
        show_row(7, [1, 2, 3, 4, 5], 0.001)
        
        i += 1
        
    i = 0
    while i < 200:
        show_row(1, [2,3,4], 0.001)
        show_row(2, [1,5], 0.001)
        show_row(3, [1,5], 0.001)
        show_row(4, [1], 0.001)
        show_row(5, [1], 0.001)
        show_row(6, [1], 0.001)
        show_row(7, [1], 0.001)
        
        i += 1

if __name__ == "__main__":

    main()
