#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

# default trackbar value
trackbar_value = 127

def update_thresh(new):
    global trackbar_value
    trackbar_value = new
    
def main():
    # Working with image files stored in the same folder as .py file
    file = "sample02.tiff"

    # Load the image from the given location
    img = cv2.imread(file)

    # Load the image from the given location in greyscale
    img_greyscale = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    
    cv2.namedWindow("Output")

    cv2.createTrackbar("Threshold", "Output", 0, 255, update_thresh)
    
    detector = cv2.SimpleBlobDetector_create()
    
    blobparams = cv2.SimpleBlobDetector_Params()
    
    blobparams.filterByArea = True
    blobparams.minArea = 100
    blobparams.maxArea = 150000
    blobparams.filterByCircularity = True
    blobparams.filterByInertia = False
    blobparams.filterByConvexity = False
    blobparams.minDistBetweenBlobs = 1
    
    width = 1280
    height = 720
    
    while True: 
        # Thresholding the grayscaled image 
        ret, thresh = cv2.threshold(img_greyscale, trackbar_value, 255, cv2.THRESH_BINARY)
        img = cv2.imread(file)
        cv2.rectangle(thresh, (0,0), (width-1, height-1), (255,255,255),2)
        keypoints = detector.detect(thresh)
        
        
        
        for keypoint in keypoints:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            index = keypoints.index(keypoint)
            cv2.putText(img, f"{x},{y},{index}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            detector = cv2.SimpleBlobDetector_create(blobparams)
            
        #img = cv2.drawKeypoints(img, keypoints, None, (0,255,0),
         #                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        imgcopy = cv2.drawKeypoints(img, keypoints, None, (0,255,0),
                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        
        # Display the images
        cv2.imshow("Original", imgcopy)
        cv2.imshow("Threshold", thresh)
        
        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()