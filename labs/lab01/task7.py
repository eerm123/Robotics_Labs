#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time
import machine
import math

echo_pin = 7 # < --- YOU HAVE TO ENTER THE GP<x> PIN, YOU HAVE CONNECTED ECHO TO
trig_pin = 6 # < --- YOU HAVE TO ENTER THE GP<x> PIN, YOU HAVE CONNECTED TRIGGER TO

delay_us = 10 # < --- YOU HAVE TO FIND THE MINIMAL VALUE FROM THE DATASHEET

trigger = Pin(trig_pin, Pin.OUT)
echo = Pin(echo_pin, Pin.IN)


def get_ultrasonic_reading(timeout_us=100_000, default_value=-1):
    method_start_us = time.ticks_us()
    trigger.high()
    time.sleep_us(delay_us)
    trigger.low()
    signal_rise = time.ticks_us()
    signal_fall = signal_rise

    while echo.value() == 0:
        signal_rise = time.ticks_us()
        if time.ticks_diff(signal_rise, method_start_us) > timeout_us:
            return default_value

    while echo.value() == 1:
        signal_fall = time.ticks_us()
        if time.ticks_diff(signal_fall, method_start_us) > timeout_us:
            return default_value

    duration_us = signal_fall - signal_rise

    return duration_us
    
def get_distance_in_mm(duration_us):
    
    distance_from_object_in_mm = duration_us/ 5.8

    return distance_from_object_in_mm

def main():
    lcd_columns = 16
    lcd_rows = 2
    
    scl_pin = board.GP17
    sda_pin = board.GP16
    
    i2c = busio.I2C(scl_pin, sda_pin)
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
    
    current_menu = "INITIAL"

    while True:
        duration_us = get_ultrasonic_reading()
        dist_mm = get_distance_in_mm(duration_us)
        if current_menu == "INITIAL":
                lcd.clear()
                lcd.message = f"US measurement \n{str(int(dist_mm))}          mm"
                lcd.color = [0, 0, 100]
                time.sleep(0.5)
        else:
            print("Encountered an unexpected state: ", current_menu)

if __name__ == "__main__":
    main()
    
