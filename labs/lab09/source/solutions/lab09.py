# -*- coding: utf-8 -*-

TASK_NUMBER = 3 # Update this value in the beginning of each task!
prev_marker = -1
reset_value = 0
start = 2000
slip = 0
prev_N = 0
prev_pos_encoder = 0


####################################################
# Task 1: Calculate velocity for different sensors #
####################################################
def calculate_velocity(position1, time1, position2, time2):
    """
    Calculate the velocity based on two positions and 
    the times at which these positions were measured.
    :param position1: A floating point number representing the position of the robot at time1
    :param time1: A floating point number representing the time at which position1 was measured
    :param position2: A floating point number representing the position of the robot at time2
    :param time2: A floating point number representing the time at which position2 was measured
    :return: The velocity calculated from the two positions
    """
    
    velocity = (position2 - position1) / (time2 - time1)
    return velocity


#####################################
# Task 2: Live encoder adjustment   #
#####################################
def measure_with_encoders_enhanced(robot, current_marker_index):
    """
    Calculate the distance to the end of the track using encoders and when the 
    robot moves to the next marker remove any drift accumulated by the encoders.
    :param robot: The same gopigo robot object that you have used in previous labs
    :param current_marker_index: The index of the marker that the robot is currently 
                                 on, it is the same value as the one returned by 
                                 check_markers(marker_sensor_value, current_marker_index) 
                                 that you implemented in the previous lab
    :return: The distance from the end measured with the combination of encoders and markers
    """
    global prev_marker
    global reset_value
    global start
    global slip


    marker_distances = [1800, 1600, 1300, 900, 600, 400, 200]
    current_count = 1800 - robot.read_encoders_average(units="cm") * 10
    
    if current_marker_index > prev_marker:   
    #if current_marker_index == 0 and prev_marker == -1:
        prev_marker = current_marker_index
        #start = marker_distances[current_marker_index]
        #reset_value = current_count
        slip = marker_distances[current_marker_index] - current_count
    #    print(f"New marker. Distance to wall: {distance} mm")
    #    print(f"Total markers: {current_marker_index}")
    #elif current_marker_index > 0:
    #    prev_marker = current_marker_index - 1
    #    distance = (start - current_count) - marker_distances[current_marker_index]
    #    print(f"New marker. Distance to wall: {distance} mm")
    #    print(f"Total markers: {current_marker_index}")
    
    distance_wall = current_count + slip

    return distance_wall



############################################
# Task 3: Implement complementary filter   #
############################################
def complementary_filter(us_pos, enc_pos):
    """
    Implement the complementary filter.
    :param us_pos: The latest reading from the ultrasonic
    :param enc_pos: The latest reading from the encoders
    :return: The updated position estimate from the complementary filter
    """
    # Fill in the function.
    global prev_N
    global prev_pos_encoder
    
    a = 0.01
    b = 0.99
    
    encoder = enc_pos - prev_pos_encoder
    posN = a * us_pos + b * (prev_N + encoder)
    prev_N = posN
    prev_pos_encoder = enc_pos
    
    return posN


##############################################
#           Task 4: Kalman Filter            #
# The following code blocks should be edited #
#    while solving the Kalman filter task.   #
##############################################

# A class for performing operations with Gaussians
class Gaussian:
    def __init__(self, mu, sigma):
        # Initializes a Gaussian with given mu and sigma values
        self.mu = mu
        self.sigma = sigma

    def __repr__(self):
        # Allows the gaussian to be displayed as a string
        return f"Gaussian(mu={self.mu}, sigma={self.sigma})"
        
    #################################################
    # Task 4.2: Implement addition of two Gaussians #
    #################################################
    def __add__(self, other: 'Gaussian'):
        """
        Add two gaussians.
        :param self: The previous location estimate gaussian
        :param other: The gaussian to add
        :return: The sum of the two gaussians (which is also a gaussian)
        """
        return

    #######################################################
    # Task 4.3: Implement multiplication of two Gaussians #
    #######################################################
    def __mul__(self, other: 'Gaussian'):
        """
        Multiply two gaussians.
        :param self: The previous location estimate gaussian
        :param other: The gaussian to multiply
        :return: The product of the two gaussians (which is also a gaussian)
        """
        return


# A Kalman filter class
class Kalman:
    def __init__(self, initial_gaussian: Gaussian):
        # Initializes a Kalman filter with the initial state given as an input
        self.filtered_result = initial_gaussian

    def __repr__(self):
        # Allows the Kalman filter to be displayed as a string
        return f"Kalman({self.filtered_result})"
        
    ########################################
    # Task 4.2: Implement the predict step #
    ########################################
    def predict(self, measurement: Gaussian):
        """
        Kalman filter predict step.
        :param self: The kalman filter instance
        :param measurement: The measurement to predict upon
        :return: The new position estimate
        """
        # Fill in the function
        return 0

    #######################################
    # Task 4.3: Implement the update step #
    #######################################
    def update(self, measurement: Gaussian):
        """
        Kalman filter update step.
        :param self: The kalman filter instance
        :param measurement: The measurement to update upon
        :return: The new position estimate
        """
        # Fill in the function
        return 0

# Global variables for holding the encoder difference and camera Gaussians
# and the Kalman class object for use in other files
# DO NOT CHANGE THE NAMES OF THESE VARIABLES!
camera_gaussian = None
encoder_diff_gaussian = None
kalman_filter = Kalman(None)

def on_encoder_measurement(enc_pos):
    """
    This function is called every time the robot's encoders 
    receive a new reading. Do Kalman prediction here.
    :param enc_pos: The latest reading from the encoders
    :return: The updated position estimate from the Kalman filter or None if the estimate should not change
    """
    return

def on_camera_measurement(cam_pos):
    """
    This function is called every time the robot calculates a new 
    distance estimate from the camera image. Do Kalman update here.
    :param cam_pos: The latest distance estimate based on the image from the camera
    :return: The updated position estimate from the Kalman filter or None if the estimate should not change
    """
    return
