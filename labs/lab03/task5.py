#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin, PWM, ADC
import time
import sys
import select


def handle_input(servo, in_value):
    if in_value > 1600000 or in_value < 1400000:
            print("Speed must be between 1400000 and 1600000")
    else:
        servo.duty_ns(in_value)
        
    """
    Arguments:
        servo           -- PWM, servo object
        in_value        -- int, input from Shell
    
    Returns:
        nothing
    """

blocked = "False"
previous_servo_time = 0

def calculate_rpm(als, low_thresh, high_thresh):
    global previous_time
    global blocked
    global previous_servo_timing
    data = als.read_u16()
    current_time = time.ticks_ms()
    previous_time = current_time
    
    if data < low_thresh and blocked == "False":
        blocked = "True"
        servo_time = time.ticks_ms()
        print(str(60/((servo_time - previous_servo_time)/1000)) + " RPM")
        previous_servo_time = servo_time
    elif data > high_thresh and blocked == "True":
        blocked = "False"
    
    
    """
    Arguments:
        als              -- ADC, sensor object
        low_thresh       -- int, lower threshold for RPM calculation
        high_thresh      -- int, upper threshold for RPM calculation
    
    Returns:
        nothing    
    """

def light(als):
    global previous_time
    current_time = time.ticks_ms() # Get the current time in milliseconds

    if current_time > previous_time + 50:
        data = als.read_u16()
        previous_time = current_time
        print(data)
    

def main():
    global previous_time
    servo = PWM(Pin(6))
    servo.freq(50)
    
    als = ADC(Pin(27, Pin.IN))
    low_thresh = 4000 # Choose a suitable value
    high_thresh = 20000 # Choose a suitable value
    
    previous_time = 0
    
    while True:
        light(als)
        data_in = select.select([sys.stdin], [], [], 0)[0]
        if not data_in:
            calculate_rpm(als, low_thresh, high_thresh)
        else:
            line = data_in[0].readline()
            if line.rstrip():
                handle_input(servo, int(line))


if __name__ == "__main__":
    main()

