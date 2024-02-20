#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time

# Colour detection limits
lB = 125
lG = 125
lR = 125
hB = 255
hG = 255
hR = 255

def update_lB(new):
    global lB
    lB = new
def update_lG(new):
    global lG
    lG = new
def update_lR(new):
    global lR
    lR = new
def update_hB(new):
    global hB
    hB = new
def update_hG(new):
    global hG
    hG = new
def update_hR(new):
    global hR
    hR = new

def main():
    # Open the camera
    camera = cv2.VideoCapture(0)
    
    cv2.namedWindow("Thresholded")
    cv2.createTrackbar("lB", "Thresholded", lB, 225, update_lB)
    cv2.createTrackbar("lG", "Thresholded", lG, 225, update_lG)
    cv2.createTrackbar("lR", "Thresholded", lR, 225, update_lR)
    cv2.createTrackbar("hB", "Thresholded", hB, 255, update_hB)
    cv2.createTrackbar("hG", "Thresholded", hG, 255, update_hG)
    cv2.createTrackbar("hR", "Thresholded", hR, 255, update_hR)
    
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
        lowerLimits = np.array([lB, lG, lR])
        upperLimits = np.array([hB, hG, hR])
        
        # Our operations on the frame come here
        thresholded = cv2.inRange(framehsv, lowerLimits, upperLimits)
        
        thresholded = cv2.bitwise_not(thresholded)
        
        cv2.rectangle(thresholded, (0,0), (width-1, height-1), (255,255,255),2)

        keypoints = detector.detect(thresholded)
        
        framekp = cv2.drawKeypoints(frame, keypoints, None, (0,255,0),
                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        new_frame_time = time.time()
        fps = 1/(new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = str(fps)
        
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
