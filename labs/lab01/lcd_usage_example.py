
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# First you need to import the LCD libraries that you just uploaded
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time

def main():
    lcd_columns = 16 # How many characters we can fit on the screen
    lcd_rows = 2     # How many rows of characters we have

    # Replace x with the pin number, board.GPx in CircuitPython is the same as machine.Pin(x) in MicroPython
    scl_pin = board.GP1
    sda_pin = board.GP0

    i2c = busio.I2C(scl_pin, sda_pin)
    # Initialize the LCD
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

    while True:
        # Print out statuses of buttons. The variables contain a boolean value (True/False)
        print("SELECT button status: ", lcd.select_button)
        if lcd.select_button == True:
        # Set the message on the screen
            lcd.message = "PRESSED     "
        elif lcd.select_button == False:
            lcd.message = "NOT PRESSED"
            time.sleep(1)


if __name__ == "__main__":
    main()
