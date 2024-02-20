#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin
import time

# Defining row pins for ease of use.
# You should enter the GPIO numbers that you connected your display to.
pin_numbers = [0, 1, 2, 3, 4, 5, 6]
pins = []

def init():
    global pins
    
    # Create a list of machine Pin objects and set them to value 1
    for pin_number in pin_numbers:
        pin = Pin(pin_number, Pin.OUT)
        pins.append(pin)
        pin.value(1)# Turn off LED

def main():
    init()
    p = 0
    direction = 1
    while True:
        # Write the code here to control the row pins in the desired way.
        pins[p].value(1)
        p += direction
        if p >= len(pins):
            p = len(pins) - 1
            direction = -1
        elif p < 0:
            p = 1
            direction = 1
        pins[p].value(0)
        
        time.sleep(0.1)
        
if __name__ == "__main__":
    main()

