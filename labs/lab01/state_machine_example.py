#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time
import machine
import math

# Needed to convert the values Pico reads (0-65535)
# to the actual voltages (0V - 3.3V)
conversion_factor = 3.3 / 65535

# Initialise the temperature sensor
sensor_temp = machine.ADC(4)

# Initialise the input voltage sensor
machine.Pin(29, machine.Pin.IN)
input_voltage = machine.ADC(3)

# The following function can be used to get the Pico board temperature
# Return board temperature as a character string
def getBoardTemperature():
    reading = sensor_temp.read_u16() * conversion_factor
    # Values needed to convert input voltage into temperature (taken from Pico datasheet)
    temperature = 27 - (reading - 0.706) / 0.001721
    
    temperature_text = f"{temperature:.01f} C"
    
    return temperature_text

# The following function can be used to get the current time
# Return current time as a character string
def getTimeText():
    epoch_time = time.time()
    
    hours = math.floor(epoch_time % 86400 / 3600)
    minutes = math.floor(epoch_time % 3600 / 60)
    seconds = epoch_time % 60
        
    time_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_text

# The following function can be used to get the Raspberry's input voltage
# Return device input voltage as a character string
def getInputVoltage():
    voltage = input_voltage.read_u16() * conversion_factor * 3
    voltage_text = f"{voltage:.03f} V"
    
    return voltage_text

def main():
    # Initialisation of LCD with correct parameters
    lcd_columns = 16
    lcd_rows = 2
    
    # Replace x with the pin number, board.GPx in CircuitPython is the same as machine.Pin(x) in MicroPython
    scl_pin = board.GP1
    sda_pin = board.GP0
    
    i2c = busio.I2C(scl_pin, sda_pin)
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

    # Initialize our state variable.
    # Note that the variable is named so that
    # it reflects the meaning of the state in the program.
    # Also, the state values can be strings and because of this,
    # it is possible to use reasonable names for states.
    current_menu = "INITIAL"

    # The main loop that runs until the program is closed
    while True:
        # Within the main loop we first check the state values
        # as we want to have different behaviour for different states
        if current_menu == "INITIAL":
            if lcd.up_button:
                # Change the state
                current_menu = "VOLTAGE"
                # Do the actions that happen on the corresponding transition
                lcd.clear()
                # Make the screen show a voltage message
                lcd.message = getInputVoltage()
                # After transition wait a bit to allow the user
                # to remove the finger from the button.
                # Otherwise we could have several transitions with a single button press.
                time.sleep(0.5)
                
        if current_menu == "INITIAL":
            if lcd.down_button:
                # Change the state
                current_menu = "TEMP"
                lcd.clear()
                lcd.message = getBoardTemperature()
                time.sleep(0.5)
                
        elif current_menu == "TEMP":
            if lcd.up_button:
                # Change the state
                current_menu = "VOLTAGE"
                lcd.clear()
                lcd.message = getInputVoltage()
                time.sleep(0.5)
                
            elif lcd.down_button:
                # Change the state
                current_menu = "VOLTAGE"
                lcd.clear()
                lcd.message = getInputVoltage()
                time.sleep(0.5)    
                       
        # For other states we can use elif statements, because if we already found the correct
        # state we can skip checking the others
        elif current_menu == "VOLTAGE":
            if lcd.down_button:
                # Change the state
                current_menu = "TEMP"
                # Do the actions that happen on the corresponding transition
                lcd.clear()
                lcd.message = getBoardTemperature()
                time.sleep(0.5)
                
            elif lcd.up_button:
                # Change the state
                current_menu = "TEMP"
                lcd.clear()
                lcd.message = getBoardTemperature()
                time.sleep(0.5) 

        # Having an else statement that is run when no state matched the current one
        # is a good habit and helps for example to discover typos within state names.
        # In the current tasks we should never reach this print command.
        else:
            print("Encountered an unexpected state: ", current_menu)

if __name__ == "__main__":
    main()
