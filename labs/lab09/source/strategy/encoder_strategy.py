from ..solutions import distance_measuring
from .strategy import SensorStrategy, DistanceMeasuring


class EncoderStrategy(SensorStrategy, DistanceMeasuring):
    def __init__(self):
        super().__init__("encoders")
        self.__gopigo = self.currentState.get_gopigo()

    def measure_distance(self):
        self.currentState.update_encoders_distance(distance_measuring.measure_with_encoders(self.__gopigo))
