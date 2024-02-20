from machine import ADC, Pin
import time

some_sensor = ADC(Pin(27, Pin.IN)) # You can use any of Pico's 3 ADC pins
data = some_sensor.read_u16() # Read sensor input from the ADC pin
led = Pin(25, Pin.OUT)


def main():
    LED = "LED_off"
    while True:
        data = some_sensor.read_u16()
        if LED == "LED_on":
            if data < 3000:
                LED = "LED_off"
                led.high()
        elif LED == "LED_off":
            if data > 10000:
                LED = "LED_on"
                led.low()
        time.sleep(0.1)
        print(data)


if __name__ == "__main__":
    main()