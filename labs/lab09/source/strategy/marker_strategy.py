# -*- coding: utf-8 -*-

from ..solutions import drive_logic
from .strategy import DistanceMeasuring, SensorStrategy


class MarkerStrategy(SensorStrategy, DistanceMeasuring):
    def __init__(self):
        super().__init__("marker")

    def measure_distance(self):
        # Get the necessary parameters and call the marker index update function
        marker_sensor_value = self.currentState.get_raspberry_pico().get_line_sensor_dict()["IR_RIGHT"]
        current_marker_index = self.currentState.get_current_marker_index()
        self.currentState.set_current_marker_index(drive_logic.check_markers(marker_sensor_value, current_marker_index))
