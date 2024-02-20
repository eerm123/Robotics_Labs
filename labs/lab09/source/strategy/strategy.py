from abc import ABC, abstractmethod

from ..helper.current_state import CurrentState


class SensorStrategy(ABC):
    def __init__(self, name):
        self.name = name
        self.currentState = CurrentState()


class DistanceMeasuring(ABC):
    @abstractmethod
    def measure_distance(self):
        pass
