#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import machine
import time

from pololu import IMU

# Constants for sensors
SENSITIVITY_baro = 4096 # (LSB/hPa)
SENSITIVITY_accel = 0.122 # (mg/LSB)
SENSITIVITY_gyro = 8.75  # (mdps/LSB)
SENSITIVITY_mag = 3421   # (LSB/gauss)
SENSITIVITY_temp = 480

# Variable for the multi-sensor object
m_sense = None


def init():
    global m_sense
    i2c = machine.I2C(0,
                  scl=machine.Pin(5),
                  sda=machine.Pin(4))
    m_sense = IMU(i2c)
    m_sense.barometer_init(IMU.BAROMETER_FREQ_1HZ)
    m_sense.accelerometer_init(IMU.ACCELEROMETER_FREQ_26HZ, IMU.ACCELEROMETER_SCALE_4G)
    m_sense.gyroscope_init(IMU.GYROSCOPE_FREQ_26HZ, IMU.GYROSCOPE_SCALE_245DPS)
    m_sense.magnetometer_init(IMU.MAGNETOMETER_FREQ_5HZ, IMU.MAGNETOMETER_SCALE_8GAUSS)
    time.sleep(1)

def main():
    init()
    
    while True:
        baro_raw = m_sense.barometer_raw_data()
        baro = baro_raw / SENSITIVITY_baro
        print(f"B: {baro:.2f} hPa")
        time.sleep(1)
        
        accel_raw = m_sense.accelerometer_raw_data()
        accel_x = accel_raw["x"] * SENSITIVITY_accel / 1000
        accel_y = accel_raw["y"] * SENSITIVITY_accel / 1000
        accel_z = accel_raw["z"] * SENSITIVITY_accel / 1000
        print(f"Accelerometer (g): X={accel_x:.2f} g Y={accel_y:.2f} g Z={accel_z:.2f} g")
        time.sleep(1)
        
        gyro_raw = m_sense.gyroscope_raw_data()
        gyro_x = gyro_raw["x"] * SENSITIVITY_gyro / 1000
        gyro_y = gyro_raw["y"] * SENSITIVITY_gyro / 1000
        gyro_z = gyro_raw["z"] * SENSITIVITY_gyro / 1000
        print(f"Gyroscrope (dps): X={gyro_x:.2f} dps Y={gyro_y:.2f} dps Z={gyro_z:.2f} dps")
        time.sleep(1)
        
        mag_raw = m_sense.magnetometer_raw_data()
        mag_x = mag_raw["x"] / SENSITIVITY_mag
        mag_y = mag_raw["y"] / SENSITIVITY_mag
        mag_z = mag_raw["z"] / SENSITIVITY_mag
        print(f"Magnetometer (gauss): X={mag_x:.2f} gauss Y={mag_y:.2f} gauss Z={mag_z:.2f} gauss")
        time.sleep(1)
        
        temp_raw = m_sense.lps25h_raw_temp()
        temp = 42.5 + (temp_raw / SENSITIVITY_temp)
        print(f"Temperature (°C): {temp}")

if __name__ == "__main__":
    main()
