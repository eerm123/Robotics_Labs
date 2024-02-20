from machine import Pin
import time

solenoid = Pin(28, Pin.OUT)

def main():
    while True:
        solenoid.high()
        time.sleep(0.1)
        solenoid.low()
        time.sleep(2)

if __name__ == "__main__":
    #Run the main function
    main()