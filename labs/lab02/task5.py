#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from machine import Pin, PWM
import machine
import time

from pololu import IMU

# Constants for sensors
SENSITIVITY_accel = 0.122
SENSITIVITY_temp = 480

pwm = PWM(Pin(9))
pwm.freq(50)

# Variable for the multi-sensor object
m_sense = None

def map_value(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled*rightSpan)

def servo_turn(speed):
    speed = int(map_value(speed, -1,1,1400000,1600000))
    print(speed)
    pwm.duty_ns(speed)
    
def init():
    global m_sense
    i2c = machine.I2C(0,
                  scl=machine.Pin(5),
                  sda=machine.Pin(4))
    m_sense = IMU(i2c)
    m_sense.accelerometer_init(IMU.ACCELEROMETER_FREQ_26HZ, IMU.ACCELEROMETER_SCALE_4G)
    time.sleep(1)

def main():
    init()
    
    while True:
        
        accel_raw = m_sense.accelerometer_raw_data()
        accel_x = accel_raw["x"] * SENSITIVITY_accel / 1000
        accel_y = accel_raw["y"] * SENSITIVITY_accel / 1000
        accel_z = accel_raw["z"] * SENSITIVITY_accel / 1000
        servo_turn(accel_z)
        print(f"Accelerometer (g): X={accel_x:.2f} g Y={accel_y:.2f} g Z={accel_z:.2f} g")
        time.sleep(0.2)
        
        
        temp_raw = m_sense.lps25h_raw_temp()
        temp = 42.5 + (temp_raw / SENSITIVITY_temp)
        print(f"Temperature (°C): {temp}")

if __name__ == "__main__":
    main()

