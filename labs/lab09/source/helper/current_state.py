import easygopigo3 as go
import cv2

from .pico_facade import RaspberryPicoFacade
from ..helper.velocity import Velocity
from ..solutions import lab09


class CurrentState(object):
    _instance = None

    # A Velocity class object for holding and updating velocities
    velocities = Velocity()

    __gopigo = go.EasyGoPiGo3()
    __raspberry_pico_facade = RaspberryPicoFacade()
    __camera = cv2.VideoCapture(0)

    current_marker_index = -1

    location_estimates = {
        "us": 0,
        "encoder": 0,
        "camera": 0,
        "encoder_marker": 0
    }

    sensor_fusion = {
        "us_velocity": 0,
        "enc_velocity": 0,
        "cam_velocity": 0,
        
        "complementary": 0,
        "complementary_velocity": 0,
        "kalman": 0,
        "kalman_velocity": 0,
        "kalman_result_gaussian": 0,
        "cam_gaussian": 0,
        "enc_gaussian": 0
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrentState, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.__raspberry_pico_facade.set_ultrasonic_callback(self.update_ultrasonic_callback)

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

    def get_encoders_distance(self):
        return self.location_estimates["encoder"]
    
    def get_encoders_enhanced_distance(self):
        return self.location_estimates["encoder_marker"]
    
    def get_camera_distance(self):
        return self.location_estimates["camera"]

    def get_complementary(self):
        return self.sensor_fusion["complementary"]

    def get_complementary_velocity(self):
        return self.sensor_fusion["complementary_velocity"]

    def get_kalman_filter(self):
        return self.kalman_filter

    def get_kalman(self):
        return self.sensor_fusion["kalman"]

    def get_kalman_velocity(self):
        return self.sensor_fusion["kalman_velocity"]

    def get_kalman_result_gaussian(self):
        return lab09.kalman_filter.filtered_result

    def get_cam_gaussian(self):
        return lab09.camera_gaussian

    def get_enc_gaussian(self):
        return lab09.encoder_diff_gaussian

    def update_ultrasonic_distance(self, value):
        self.location_estimates["us"] = value

    # To be called from Lab09.py
    def set_kalman_position_estimate(self, value):
        if value is None:
            return
        self.sensor_fusion["kalman"] = value

        # Update the velocity of Kalman position estimate
        self.sensor_fusion["kalman_velocity"] = \
                self.velocities.update_velocity_for_sensor(value, 'kalman')

    def update_ultrasonic_callback(self, value):
        # Task #1
        self.sensor_fusion["us_velocity"] = self.velocities.update_velocity_for_sensor(value, 'us')

        # Task #3
        self.sensor_fusion["complementary"] = lab09.complementary_filter(
                                              self.get_ultrasonic_distance(), self.get_encoders_distance())
        self.sensor_fusion["complementary_velocity"] = self.velocities.update_velocity_for_sensor(
                                                       self.sensor_fusion["complementary"], 'complementary')

    def update_encoders_distance(self, value):
        self.location_estimates["encoder"] = value
        self.location_estimates["encoder_marker"] = lab09.measure_with_encoders_enhanced(
                                                    self.__gopigo, self.get_current_marker_index())

        # Task #1
        self.sensor_fusion["enc_velocity"] = self.velocities.update_velocity_for_sensor(value, 'enc')

        # Task #3
        self.sensor_fusion["complementary"] = lab09.complementary_filter(
                                              self.get_ultrasonic_distance(), self.get_encoders_distance())
        self.sensor_fusion["complementary_velocity"] = self.velocities.update_velocity_for_sensor(
                                                       self.sensor_fusion["complementary"], 'complementary')

        # Task #4
        self.set_kalman_position_estimate(lab09.on_encoder_measurement(value))

    def update_camera_distance(self, value):
        self.location_estimates["camera"] = value

        # Task #1
        self.sensor_fusion["cam_velocity"] = self.velocities.update_velocity_for_sensor(value, 'cam')

        # Task #4
        self.set_kalman_position_estimate(lab09.on_camera_measurement(value))

    def close(self):
        print("Closing serial and camera")
        self.__camera.release()
        self.__raspberry_pico_facade.close()
        print("Applying robot emergency brake")
        self.__gopigo.stop()
