from machine import Pin
import utime
import json

# Pin definitions
pin_nr_ultrasonic_echo = 0
pin_nr_ultrasonic_trigger = 1
light_sensor_pin_numbers = [2, 3, 4, 5, 6]

# As ultrasonic sensors on different robots would interfere with each 
# other when measuring at the exact same time, it is needed to limit 
# how fast it is being measured. This variable controls the interval 
# between subsequent ultrasonic measurements in milliseconds.
ultrasonic_measurement_interval = 300


def get_ultrasonic_reading(timeout=100):
    measurement_start_time = utime.ticks_ms()
    
    # Ensure that the trigger pin is low when starting a measurement
    pin_ultrasonic_trigger.low()
    utime.sleep_us(2)
    
    # Wait for the echo pin to go low
    while pin_ultrasonic_echo.value() != 0:
        if utime.ticks_ms() - measurement_start_time > timeout:
            return None # Return if timeout occurs
    
    # Generate the trigger impulse
    pin_ultrasonic_trigger.high()
    utime.sleep_us(60)
    pin_ultrasonic_trigger.low()

    # Wait for the echo pin to go high
    while pin_ultrasonic_echo.value() == 0:
        if utime.ticks_ms() - measurement_start_time > timeout:
            return None # Return if timeout occurs
    signal_off = utime.ticks_us()

    # Wait for the echo pin to go back low
    while pin_ultrasonic_echo.value() == 1:
        if utime.ticks_ms() - measurement_start_time > timeout:
            return None # Return if timeout occurs
    signal_on = utime.ticks_us()

    # Calculate the time difference and the distance
    duration_us = signal_on - signal_off
    distance_mm = (duration_us/2) / 2.91
    
    if distance_mm > 4000:
        return None
    return int(distance_mm)


def main():
    # Initialize pins
    global pin_ultrasonic_echo, pin_ultrasonic_trigger
    pin_ultrasonic_echo = Pin(pin_nr_ultrasonic_echo, Pin.IN)
    pin_ultrasonic_trigger = Pin(pin_nr_ultrasonic_trigger, Pin.OUT)
    light_sensor_pins = [Pin(pin_nr, Pin.IN) for pin_nr in light_sensor_pin_numbers]

    last_ultrasonic_measurement_time = utime.ticks_ms()
    while True:
        measurements = {}

        # Measure the light sensor states
        for i, pin in enumerate(light_sensor_pins):
            measurements[f"ls{i+1}"] = pin.value()
        
        # If the timing is right, print the ultrasonic sensor value too
        current_time = utime.ticks_ms()
        if current_time - last_ultrasonic_measurement_time > ultrasonic_measurement_interval:
            last_ultrasonic_measurement_time = current_time
            measurements["us"] = get_ultrasonic_reading()
        
        # Encode the measurements as a JSON formatted string and print it
        print(json.dumps(measurements))
        
        # Limit the responses to 10Hz
        utime.sleep(0.1)


if __name__ == "__main__":
    main()