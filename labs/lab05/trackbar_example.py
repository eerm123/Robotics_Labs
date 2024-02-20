#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

# Open the default video camera
camera = cv2.VideoCapture(0)

# Global variable for the latest trackbar value (exposure is a float here)
exposure = camera.get(cv2.CAP_PROP_EXPOSURE)

# A callback function for a trackbar
# It is triggered every time the trackbar slider is used
def update_exposure(new):
    global exposure
    exposure = new
    camera.set(cv2.CAP_PROP_EXPOSURE, new)


def main():
    # Read a single frame from the camera before changing any camera settings, otherwise they may reset
    camera.read()
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    
    # setting to manual mode of the video capture device
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

    # Create a named window and name it "Output"
    cv2.namedWindow("Output")

    # Attach a trackbar to a window named "Output"
    cv2.createTrackbar("Exposure", "Output", int(exposure), 500, update_exposure)

    # An infinite while-loop
    while True:
        # Read a single frame from the capture device (i.e. the camera)
        ret, frame = camera.read()

        # Add the trackbar value as text on the read frame
        cv2.putText(frame, str(exposure), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 125, 255), 2)

        # Display the frame in the window named "Output"
        cv2.imshow("Output", frame)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    # Close the video capturing device
    camera.release()

    # Close any windows associated with OpenCV GUI
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
