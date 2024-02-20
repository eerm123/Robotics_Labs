#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import time

def main():
    # Open the camera
    camera = cv2.VideoCapture(0)
    
    new_frame_time = 0
    
    prev_frame_time = 0
    
    while True:
        # Read the image from the camera
        ret, frame = camera.read()
        
        new_frame_time = time.time()
        fps = 1/(new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = str(fps)
        # Write some text onto the frame
        cv2.putText(frame, fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show this image on a window named "Original"
        cv2.imshow("Original", frame)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    # When everything is done, release the camera
    print("closing program")
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
