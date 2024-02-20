# -*- coding: utf-8 -*-

from ..solutions import distance_measuring
from .strategy import DistanceMeasuring, SensorStrategy


class UltrasonicStrategy(SensorStrategy, DistanceMeasuring):
    def __init__(self):
        super().__init__("ultrasonic")
        self.__raspberry_pico = self.currentState.get_raspberry_pico()

    def measure_distance(self):
        self.currentState.update_ultrasonic_distance(distance_measuring.measure_with_ultrasonic(self.__raspberry_pico))
