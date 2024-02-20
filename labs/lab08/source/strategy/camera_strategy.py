# -*- coding: utf-8 -*-

from ..solutions import distance_measuring
from .strategy import DistanceMeasuring, SensorStrategy


class CameraStrategy(SensorStrategy, DistanceMeasuring):
    def __init__(self):
        super().__init__("camera")
        self.__camera = self.currentState.get_camera()

    def measure_distance(self):
        self.currentState.update_camera_distance(distance_measuring.measure_with_camera(self.__camera))
