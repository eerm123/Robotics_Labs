#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import easygopigo3 as go
import numpy as np
import time

# Global variable for determining GoPiGo speed
gospeed = 1000

# Global variable for video feed
camera = None

new_frame_time = 0
prev_frame_time = 0
prev_error = 0
integral = 0


# Global variable for robot object
my_robot = go.EasyGoPiGo3()

trackbar_defaults = "/home/pi/robotics-i-loti.05.010-eero-jurgenson-c39839-23-24a/labs/lab05/trackbar_defaults.txt"

lV = 255
lS = 255
lH = 180
hV = 255
hS = 255
hH = 18

def update_lV(new):
    global lV
    lV = new
def update_lS(new):
    global lS
    lS = new
def update_lH(new):
    global lH
    lH = new
def update_hV(new):
    global hV
    hV = new
def update_hS(new):
    global hS
    hS = new
def update_hH(new):
    global hH
    hH = new
def update_exposure(new):
    global exposure
    exposure = new
    camera.set(cv2.CAP_PROP_EXPOSURE, new)
def update_temp(new):
    global temp
    temp = new
    camera.set(cv2.CAP_PROP_WB_TEMPERATURE, new)

def init():
    global camera
    # This function should do everything required to initialize the robot
    # Some of this has already been filled in
    # You are welcome to add your own code if needed

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    camera.read()
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_AUTO_WB, 0)

    my_robot.set_speed(gospeed) # This sets the maximum speed of the GoPiGo


def get_values_from_file(trackbar_defaults):
    """
    This function reads the text file and returns all of the trackbar values
    """
    try:
        with open(trackbar_defaults, "r", encoding="utf-8") as fail:
            väärtused = [int(rida.strip()) for rida in fail]

        return väärtused
    except FileNotFoundError:
        return None
        
def write_values_to_file(trackbar_defaults, väärtused):
    with open(trackbar_defaults, "w", encoding="utf-8") as fail:
        for väärtus in väärtused:
            fail.write(str(väärtus) + "\n")


# TASK 1
def get_line_location(frame):
    global new_frame_time
    global prev_frame_time
    
    framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Colour detection limits
    lowerLimits = np.array([lH, lS, lV])
    upperLimits = np.array([hV, hS, hH])
    
    # Our operations on the frame come here
    thresholded = cv2.inRange(framehsv, lowerLimits, upperLimits)
    
    #thresholded = cv2.bitwise_not(thresholded)
    
    new_frame_time = time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    fps = str(fps)
    
    cv2.putText(thresholded, fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Original', thresholded)
    

    #extractin koordinaadid
    xy = np.nonzero(thresholded)
    line = np.median(xy[1])# võtan average horizontal koordinaadi
    return line


    # This function should use a single frame from the camera to determine line location
    # It should return the location of the line in the frame
    # Feel free to define and use any global variables you may need
    # YOUR CODE HERE

    #pass


# TASK 2
def bang_bang(linelocation):
    # This function should use the line location to implement a simple bang-bang controller
    # YOUR CODE HERE
    
    if linelocation < 640:
        my_robot.left()
    elif linelocation > 640:
        my_robot.right()

# TASK 3
def bang_bang_hysteresis(linelocation):
    # This function should use the line location to implement a bang-bang controller with hysteresis
    # YOUR CODE HERE
    
    if linelocation < 640-20:
        my_robot.left()
    elif linelocation > 640+20:
        my_robot.right()


# TASK 4
def proportional_controller(linelocation):
    # This function should use the line location to implement a proportional controller
    # Feel free to define and use any global variables you may need
    # YOUR CODE HERE

    if np.isnan(linelocation) == True:
        pass
    else:
        error = linelocation - 640
        constant = 0.6
        pout = error*constant
        left = 500 + pout
        right = 500 - pout
        my_robot.set_motor_dps(my_robot.MOTOR_LEFT, left)
        my_robot.set_motor_dps(my_robot.MOTOR_RIGHT, right)

# TASK 5
def pid_controller(linelocation):
    # This function should use the line location to implement a PID controller
    # Feel free to define and use any global variables you may need
    # YOUR CODE HERE
    global prev_error, integral
    if np.isnan(linelocation) == True:
        pass
    else:
        KU = 1.3 #tuned parameters by trial and error
        TU = 34.6 #tuned parameters by trial and error
        
        error = linelocation - 640
        Kp = 0.6 * KU
        Ki = (1.2 * KU) / TU
        Kd = (3 * KU * TU) / 40
        
        integral += error
        
        P = Kp * error
        I = Ki * integral
        D = Kd * (error - prev_error)
        
        Pout = P + I + D
        
        prev_error = error
        
        left = 500 + Pout
        right = 500 - Pout
        my_robot.set_motor_dps(my_robot.MOTOR_LEFT, left)
        my_robot.set_motor_dps(my_robot.MOTOR_RIGHT, right)
                
def main():
    global lH, lS, lV, hH, hS, hV, exposure, temp
    global new_frame_time
    global prev_frame_time
    
    saved_values = get_values_from_file(trackbar_defaults)
    
    if saved_values is not None:
       lH, lS, lV, hH, hS, hV, exposure, temp = saved_values
       
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_AUTO_WB, 0)
    
    cv2.namedWindow("Thresholded")
    cv2.createTrackbar("lV", "Thresholded", lV, 255, update_lV)
    cv2.createTrackbar("lS", "Thresholded", lS, 255, update_lS)
    cv2.createTrackbar("lH", "Thresholded", lH, 180, update_lH)
    cv2.createTrackbar("hV", "Thresholded", hV, 255, update_hV)
    cv2.createTrackbar("hS", "Thresholded", hS, 255, update_hS)
    cv2.createTrackbar("hH", "Thresholded", hH, 180, update_hH)
    cv2.createTrackbar("exposure", "Thresholded", int(exposure), 500, update_exposure)
    cv2.createTrackbar("temp", "Thresholded", int(temp), 6500, update_temp)
       
    new_frame_time = 0
    
    prev_frame_time = 0
        
    try:
        while True:
            # We read information from the camera
            ret, frame = camera.read()
            frame = frame[0:20]
                        
            # Task 1: uncomment the following line and implement get_line_location function
            linelocation = get_line_location(frame)
            print(linelocation)

            # Task 2: uncomment the following line and implement bang_bang function
            #bang_bang(linelocation)

            # Task 3: uncomment the following line and implement bang_bang_hysteresis function
            #bang_bang_hysteresis(linelocation)

            # Task 4: uncomment the following line and implement proportional_controller function
            #proportional_controller(linelocation)

            # Task 5: uncomment the following line and implement pid_controller function
            pid_controller(linelocation)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Got KeyBoardInterrupt, closing program.")
    finally:
        camera.release()
        cv2.destroyAllWindows()
        my_robot.stop()


if __name__ == "__main__":
    # Initialisation
    init()
    # Calling the main function
    main()
