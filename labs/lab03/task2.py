#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin, PWM
import time

def turn_servo_deg(servo, input_degree):
    pwm_0_deg = 550000
    pwm_180_deg = 2370000
    one_degree = (pwm_180_deg - pwm_0_deg) / 180
    pwm_input = int(pwm_0_deg + (one_degree * input_degree))
    
    servo.duty_ns(pwm_input)


def main():
    
    valve = Pin(20, Pin.OUT)
    pump = Pin(19, Pin.OUT)
    
    servo_front = PWM(Pin(16))
    servo_front.freq(50)

    servo_back = PWM(Pin(4))
    servo_back.freq(50)

    while True:
        pump.high()
        turn_servo_deg(servo_front, 0)        
        turn_servo_deg(servo_back, 90)        
        time.sleep(1)
        valve.high()
        time.sleep(2)
        
        turn_servo_deg(servo_back, 0)
        turn_servo_deg(servo_front, 90)        
        time.sleep(1)
        valve.low()
        time.sleep(2)
        
if __name__ == "__main__":
    main()

   




