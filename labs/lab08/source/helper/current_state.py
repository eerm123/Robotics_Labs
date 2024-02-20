# -*- coding: utf-8 -*-

import cv2
import easygopigo3 as go

from .pico_facade import RaspberryPicoFacade
from ..solutions.filters import moving_average


class CurrentState(object):
    _instance = None

    __gopigo = go.EasyGoPiGo3()
    __raspberry_pico_facade = RaspberryPicoFacade()
    __camera = cv2.VideoCapture(0)

    current_marker_index = -1

    location_estimates = {
        "us": 0,
        "us_avg": 0,
        "encoder": 0,
        "camera": 0
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrentState, cls).__new__(cls)
        return cls._instance

    def get_gopigo(self):
        return self.__gopigo

    def get_raspberry_pico(self):
        return self.__raspberry_pico_facade

    def get_camera(self):
        return self.__camera

    def get_current_marker_index(self):
        return self.current_marker_index

    def set_current_marker_index(self, new_value):
        self.current_marker_index = new_value

    def get_ultrasonic_distance(self):
        return self.location_estimates["us"]

    def get_ultrasonic_averaged_distance(self):
        return self.location_estimates["us_avg"]
    
    def get_encoders_distance(self):
        return self.location_estimates["encoder"]

    def get_camera_distance(self):
        return self.location_estimates["camera"]

    def update_ultrasonic_distance(self, value):
        self.location_estimates["us"] = value
        self.location_estimates["us_avg"] = moving_average(value)

    def update_encoders_distance(self, value):
        self.location_estimates["encoder"] = value

    def update_camera_distance(self, value):
        self.location_estimates["camera"] = value

    def close(self):
        print("Closing serial and camera")
        self.__camera.release()
        self.__raspberry_pico_facade.close()
        print("Applying robot emergency brake")
        self.__gopigo.stop()
