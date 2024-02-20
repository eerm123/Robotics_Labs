#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

def main():
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        cv2.imshow("Window 1", frame)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    camera.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()