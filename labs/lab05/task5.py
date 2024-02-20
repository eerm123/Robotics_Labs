#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time


camera = cv2.VideoCapture(0)

# Colour detection limits
lV = 255
lS = 255
lH = 180
hV = 255
hS = 255
hH = 180
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

def main():
    # Open the camera
    camera.read()
    
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
    
    blobparams = cv2.SimpleBlobDetector_Params()
    
    blobparams.filterByArea = True
    blobparams.minArea = 50
    blobparams.maxArea = 150000
    blobparams.filterByCircularity = False
    blobparams.filterByInertia = True
    blobparams.filterByConvexity = False
    blobparams.minDistBetweenBlobs = 15
    
    width = 1280
    height = 720
    
    detector = cv2.SimpleBlobDetector_create(blobparams)
    
    new_frame_time = 0
    
    prev_frame_time = 0


    while True:        
        # Read the image from the camera
        ret, frame = camera.read()

        # You will need this later
        framehsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    
        # Colour detection limits
        lowerLimits = np.array([lH, lS, lV])
        upperLimits = np.array([hV, hS, hH])
        
        # Our operations on the frame come here
        thresholded = cv2.inRange(framehsv, lowerLimits, upperLimits)
        
        thresholded = cv2.bitwise_not(thresholded)
        
        cv2.rectangle(thresholded, (0,0), (width-1, height-1), (255,255,255),2)

        keypoints = detector.detect(thresholded)
        
        framekp = cv2.drawKeypoints(framehsv, keypoints, None, (0,255,0),
                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        new_frame_time = time.time()
        fps = 1/(new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = str(fps)
        
        keypoints = detector.detect(thresholded)

        for keypoint in keypoints:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            cv2.putText(framekp, f"{x},{y}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            detector = cv2.SimpleBlobDetector_create(blobparams)
        
        cv2.putText(framekp, fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


        cv2.imshow("Original", framekp)
        # Display the resulting frame
        cv2.imshow("Thresholded", thresholded)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    # When everything done, release the camera
    print("closing program")
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
