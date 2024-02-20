# -*- coding: utf-8 -*-

from ..helper.current_state import CurrentState

# Feel free to add variables and helper functions to this file.
# Do NOT rename or remove the given functions!

raspberry_pico = CurrentState().get_raspberry_pico()  # Use this object to access sensor values from the raspberry pico, see example in drive loop
robot = CurrentState().get_gopigo()  # This is the same gopigo robot object that you have used in previous labs

# Fill this list with marker distances and use it to check them. The furthest marker has index 0.
marker_distances = [1800, 1600, 1300, 900, 600, 400, 200]
speed = 100
marker_counter = 0
prev_marker = False

def follow_line(should_close):
    # Do NOT rename or remove this function!
    robot.reset_encoders()
    robot.set_speed(150)  # feel free to change this
    
    

    while not should_close.isSet():
        line_sensor_values = raspberry_pico.get_line_sensor_dict()  # This returns you the current values of line sensors as python dict
        current_marker_index = CurrentState().get_current_marker_index()  # Use this to get the current marker index
        #print(line_sensor_values)  # So you can see the whole dict to find the keys
        #print(line_sensor_values["IR_LEFT"])  # This is how to access one line sensor value
        #print(current_marker_index)  # Prints -1 since no marker detection has been implemented
        
        if current_marker_index == 6:
            robot.stop()
        # Add your line following logic here
        #if line_sensor_values["IR_RIGHT"] == 0:
        #   robot.set_motor_dps(robot.MOTOR_RIGHT, 0)
        #    robot.set_motor_dps(robot.MOTOR_LEFT, speed)
        if line_sensor_values["IR_MID_RIGHT"] == 0:
            robot.set_motor_dps(robot.MOTOR_LEFT, speed)
            robot.set_motor_dps(robot.MOTOR_RIGHT, 0)
        #elif line_sensor_values["IR_LEFT"] == 0:
        #    robot.set_motor_dps(robot.MOTOR_LEFT, 0)
        #    robot.set_motor_dps(robot.MOTOR_RIGHT, speed)
        elif line_sensor_values["IR_MID_LEFT"] == 0:
            robot.set_motor_dps(robot.MOTOR_LEFT, 0)
            robot.set_motor_dps(robot.MOTOR_RIGHT, speed)
        elif line_sensor_values["IR_MID"] == 0:
            robot.set_motor_dps(robot.MOTOR_RIGHT, speed)
            robot.set_motor_dps(robot.MOTOR_LEFT, speed)
        
        
        should_close.wait(0.02)


def check_markers(marker_sensor_value, current_marker_index):
    global marker_counter, prev_marker
    """
    Do NOT rename or remove this function!
    Use the line sensor connected to the Raspberry Pi Pico to detect markers next to the line. 
    If a new marker is detected then print the distance from it to the wall.
    :param marker_sensor_value: line sensor value that you use for marker detection
    :param current_marker_index: index of current marker
    :return: current_marker_index if no new marker detected or index of new marker
    """
    
    if marker_sensor_value == 0 and not prev_marker:
        prev_marker = True
        current_marker_index += 1
        distance_wall =marker_distances[current_marker_index]  
        print(f"New marker. Distance to wall: {distance_wall} mm")
        print(f"Total markers: {current_marker_index}")
    elif marker_sensor_value == 1 and prev_marker:
        prev_marker = False
    
    return current_marker_index
