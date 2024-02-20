#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import time
import easygopigo3 as go

myRobot = go.EasyGoPiGo3()

trackbar_defaults = "/home/pi/robotics-i-loti.05.010-eero-jurgenson-c39839-23-24a/labs/lab05/trackbar_defaults.txt"

camera = cv2.VideoCapture(0)

lV = 255
lS = 255
lH = 180
hV = 255
hS = 255
hH = 18

kernelsize = 1

exposure = camera.get(cv2.CAP_PROP_AUTO_EXPOSURE)
temp = camera.get(cv2.CAP_PROP_AUTO_WB)


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


def blur_callback(trackbarPos):
    global kernelsize
    kernelsize = trackbarPos

# NB! This function will be re-used in the future labs
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
        

### TODO 1: Add code from task 5
### TODO 2: Once the main loop is exited, new trackbar values should be written into a text file (that is going to be in a specific lab folder)
### TODO 3: Fill in the get_values_from_file() function which reads in the text file and outputs trackbar values
### TODO 4: Run this program at least twice to make sure the trackbar values are written and read from the text file 

def main():
    global lH, lS, lV, hH, hS, hV, exposure, temp
    global kernelsize
    
    
    saved_values = get_values_from_file(trackbar_defaults)

    if saved_values is not None:
       lH, lS, lV, hH, hS, hV, exposure, temp = saved_values
        
    camera.read()
    
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_AUTO_WB, 0)
    camera.read()
    camera.set(cv2.CAP_PROP_EXPOSURE, exposure)
    camera.set(cv2.CAP_PROP_WB_TEMPERATURE, temp)
    
    cv2.namedWindow("Thresholded")
    cv2.namedWindow("Blur")
    #cv2.createTrackbar('Kernel Size', 'Blur', kernelsize, 51, blur_callback)
    
    blobparams = cv2.SimpleBlobDetector_Params()
    
    blobparams.filterByArea = True
    blobparams.minArea = 50
    blobparams.maxArea = 150000
    blobparams.filterByCircularity = False
    blobparams.filterByInertia = False
    blobparams.filterByConvexity = False
    blobparams.minDistBetweenBlobs = 1
    
    width = 1280
    height = 720
    
    detector = cv2.SimpleBlobDetector_create(blobparams)
    
    new_frame_time = 0
    
    prev_frame_time = 0
    
    current_menu = "SEARCH_PILLARS"
    myRobot.set_speed(150)

    while True:        
        # Read the image from the camera
        ret, frame = camera.read()
        frame = frame[300:400]
        
        print(frame.shape)

        # You will need this later
        framehsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        #blurVal = cv2.getTrackbarPos("Kernel Size", "Blur")
        #frame_blur = 2*blurVal + 1

        #blur = cv2.GaussianBlur(framehsv, (frame_blur, frame_blur), blurVal)
        
        lowerLimits = np.array([lH, lS, lV])
        upperLimits = np.array([hV, hS, hH])
        
        # Our operations on the frame come here
        thresholded = cv2.inRange(framehsv, lowerLimits, upperLimits)
        thresholded = cv2.bitwise_not(thresholded)
        
        #cv2.rectangle(thresholded, (0,0), (width-1, height-1), (255,255,255),2)
        cv2.rectangle(thresholded, (0, 0), (640 - 1, 100 - 1), (255, 255, 255), 2)

        keypoints = detector.detect(thresholded)
        
        #framekp = cv2.drawKeypoints(frame, keypoints, None, (0,255,0),
        #              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                        
        #blur = cv2.GaussianBlur(framekp, (frame_blur, frame_blur), blurVal)
        #blur2 = cv2.medianBlur(framekp, frame_blur)
        
        #new_frame_time = time.time()
        #fps = 1/(new_frame_time - prev_frame_time)
        #prev_frame_time = new_frame_time
        #fps = int(fps)
        #fps = str(fps)
        
        print(current_menu)
        if current_menu == 'SEARCH_PILLARS':
            print('SEARCH_PILLARS')
            
            if len(keypoints) == 0:
                myRobot.steer(30, -30)
            
            elif len(keypoints) == 2:
                parem, vasak = (keypoints[0], keypoints[1]) if keypoints[0].pt[0] > keypoints[1].pt[0] else (keypoints[1], keypoints[0])
                ratio = parem.size / vasak.size
                kesk = (parem.pt[0] + vasak.pt[0]) / 2 - 320
                print(ratio)
                
                if ratio > 1.1 and kesk < 20:
                    myRobot.turn_degrees(-70, True)
                    myRobot.forward()
                    time.sleep(2)
                    myRobot.turn_degrees(80, True)
                    camera.read()
                    camera.read()         
                elif ratio < 0.9 and kesk < 20:
                    myRobot.turn_degrees(70, True)
                    myRobot.forward()
                    time.sleep(2)
                    myRobot.turn_degrees(-80, True)
                    camera.read()
                    camera.read()
                    
                elif 0.9 < ratio < 1.1 and -30 <= kesk <= 30:
                    myRobot.steer(10, 10)
                    current_menu = 'NAVIGATE'     
                elif kesk <= -10:
                    myRobot.steer(20, 40)  #peaks keerama vasakule
                elif kesk >= 10:
                    myRobot.steer(40, 20) #peaks keerama paremale
                else:
                    myRobot.steer(10, 10) #otse
            elif len(keypoints) == 1:
                direction = 1 if keypoints[0].pt[0] > 400 else -1 if keypoints[0].pt[0] < 200 else 0
                myRobot.steer(direction * 30, -direction * 30)
            else:
                myRobot.stop()

        elif current_menu == 'NAVIGATE':
            print('NAVIGATE')

            if len(keypoints) == 2:
                parem, vasak = (keypoints[0], keypoints[1]) if keypoints[0].pt[0] > keypoints[1].pt[0] else (keypoints[1], keypoints[0])
                if parem.pt[0] > 540 and vasak.pt[0] < 100:
                    myRobot.forward()
                    current_menu = 'DONE'
                    print('DONE')
                else:
                    myRobot.steer(25, 25)

            elif len(keypoints) == 0:
                current_menu = 'SEARCH_PILLARS'
        elif current_menu == 'DONE':
            time.sleep(5)
            myRobot.stop()

        
#        print(current_menu)
                
        #cv2.putText(framekp, fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Original", frame)
        cv2.imshow("Thresholded", thresholded)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    write_values_to_file(trackbar_defaults, [lH, lS, lV, hH, hS, hV, exposure, temp])
    
    # When everything done, release the camera
    print("closing program")
    camera.release()
    cv2.destroyAllWindows()
    
    pass # remove this after adding the code


if __name__ == "__main__":
    main()


