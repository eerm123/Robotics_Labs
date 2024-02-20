# -*- coding: utf-8 -*-

import threading
from threading import Thread
from typing import List

from ..strategy.strategy import DistanceMeasuring, SensorStrategy


class MeasuringWorker(Thread):
    __strategies: List[SensorStrategy] = []

    def __init__(self, name, strategies, interval=0):
        super().__init__(name=name)
        self.__strategies = strategies
        self.should_close = threading.Event()
        self.interval = interval

    def run(self):
        while not self.should_close.isSet():
            self.should_close.wait(self.interval)
            for strategy in self.__strategies:
                if isinstance(strategy, DistanceMeasuring):
                    strategy.measure_distance()
        print("closing " + self.name)
