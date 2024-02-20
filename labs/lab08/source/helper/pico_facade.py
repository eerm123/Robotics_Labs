# -*- coding: utf-8 -*-

import json
import threading
from enum import Enum

import serial


class Sensor(Enum):
    ULTRA_SONIC = "us"
    IR_LEFT = "ir_left"
    IR_MID_LEFT = "ir_mid_left"
    IR_MID = "ir_mid"
    IR_MID_RIGHT = "ir_mid_right"
    IR_RIGHT = "ir_right"


class RaspberryPicoFacade:
    SERIAL_PORT = "/dev/ttyACM0"
    SERIAL_BAUD_RATE = 115200
    SERIAL_CONNECTION_TIMEOUT = 2  # sec
    __serial_buffer = b""

    ultrasonic_callback = None

    __sensor_measurements = {
        Sensor.ULTRA_SONIC.name: 0,
        Sensor.IR_LEFT.name: 0,
        Sensor.IR_MID_LEFT.name: 0,
        Sensor.IR_MID.name: 0,
        Sensor.IR_MID_RIGHT.name: 0,
        Sensor.IR_RIGHT.name: 0
    }

    __keys = {
        Sensor.ULTRA_SONIC.name: "us",
        Sensor.IR_LEFT.name: "ls1",
        Sensor.IR_MID_LEFT.name: "ls2",
        Sensor.IR_MID.name: "ls3",
        Sensor.IR_MID_RIGHT.name: "ls4",
        Sensor.IR_RIGHT.name: "ls5"
    }

    def __init__(self):
        self.serial_lock = threading.Lock()
        self.__initialize_serial()

    def get_us_distance(self):
        return self.__get_data_from_raspberry_pico()[Sensor.ULTRA_SONIC.name]

    def get_line_sensor_dict(self):
        sensor_data = self.__get_data_from_raspberry_pico().copy()
        if Sensor.ULTRA_SONIC.name in sensor_data:
            del sensor_data[Sensor.ULTRA_SONIC.name]
        return sensor_data

    def close(self):
        self.__serial_connection.close()

    def set_ultrasonic_callback(self, callback_func):
        self.ultrasonic_callback = callback_func

    def __initialize_serial(self, com_port=SERIAL_PORT, baudrate=SERIAL_BAUD_RATE):
        try:
            self.__serial_connection = serial.Serial(com_port, baudrate=baudrate, timeout=self.SERIAL_CONNECTION_TIMEOUT)
        except (serial.SerialException or ValueError) as e:
            print("Failed to establish a serial connection: " + str(e))

    def __get_data_from_raspberry_pico(self):
        if self.serial_lock.acquire(blocking=False):
            try:
                self.__read_from_serial()
            finally:
                self.serial_lock.release()
        return self.__sensor_measurements

    def __read_from_serial(self):
        try:
            while self.__serial_connection.in_waiting > 0:
                self.__serial_buffer += self.__serial_connection.read(self.__serial_connection.in_waiting)

            while b"\r\n" in self.__serial_buffer:
                line, self.__serial_buffer = self.__serial_buffer.split(b"\r\n", 1)
                self.__update_sensor_measurements(json.loads(line.decode().strip()))
        except json.JSONDecodeError as e:
            print("Problem with decoding JSON data: " + str(e))
        except serial.serialutil.SerialException as e:
            print("Problem with writing to or reading from serial" + str(e))
        except OSError as e:
            print("Unexpected error:", str(e))

    def __update_sensor_measurements(self, new_data):
        for key, json_key in self.__keys.items():
            if json_key == "us" and json_key in new_data and new_data[json_key] is None:
                print("Received `None` from the ultrasonic sensor - check your wiring!")
            elif json_key in new_data and self.is_number(new_data[json_key]):
                    self.__sensor_measurements[key] = new_data[json_key]
                    if self.ultrasonic_callback is not None and json_key == "us":
                        self.ultrasonic_callback(new_data[json_key])
            elif json_key != "us" or (json_key == "us" and len(new_data) == len(self.__keys)):
                print("Unexpected key or value from serial: ", str(new_data))

    @staticmethod
    def is_number(string):
        try:
            float(string)
        except ValueError:
            return False
        return True