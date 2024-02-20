#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin, PWM
import time

pwm = PWM(Pin(0))
pwm.freq(50)

def turn_servo_deg(input_degree):
    pwm_0_deg = 550000
    pwm_180_deg = 2370000
    one_degree = (pwm_180_deg - pwm_0_deg) / 180
    pwm_input = int(pwm_0_deg + (one_degree * input_degree))
    
    pwm.duty_ns(pwm_input)

def main():
    turn_servo_deg(180)

while True:
    turn_servo_deg(180)
    time.sleep(1)
    turn_servo_deg(0)
    time.sleep(2)


if __name__ == "__main__":
    # Run the main function
    main()

   
