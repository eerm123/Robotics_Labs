#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..solutions.lab09 import calculate_velocity
import time

class Velocity:
    def __init__(self, initial_velocities = {}):
        self.velocities = initial_velocities
        self.last_times = {}
        self.last_positions = {}

    def update_velocity_for_sensor(self, new_position, sensor):
        new_measurement_time = time.time()

        sensor_velocity = 0

        if sensor in self.last_times and self.last_positions[sensor] is not None and new_position is not None:
            sensor_velocity = calculate_velocity(self.last_positions[sensor], self.last_times[sensor],
                                                 new_position, new_measurement_time)
            self.velocities[sensor] = sensor_velocity
            
        self.last_times[sensor] = new_measurement_time
        self.last_positions[sensor] = new_position
        return sensor_velocity
