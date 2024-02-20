import time
from machine import PWM, Pin

pwm = PWM(Pin(4))
pwm.freq(50)


def servo_turn(speed):
    pwm.duty_ns(speed)

def main():
    while True:
        speed = int(input("Enter speed between 1400000-1600000"))
        if speed > 1400000 or speed < 1600000:
            print("Speed must be between 1400000 and 1600000")
        else:
            servo_turn(speed)
            
if __name__ == "__main__":
    main()
            