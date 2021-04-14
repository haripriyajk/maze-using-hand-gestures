from imutils.video import VideoStream
import numpy as np
import math
import argparse
import cv2
import imutils
import time

def nothing(x):
    pass
def calib():
    def_range = [[0,10,60]]
    vs = VideoStream(src=0).start()

    time.sleep(6.0)
    name = 'Calibrate '+ 'skin'
    cv2.namedWindow(name)
    cv2.createTrackbar('Hue', name, def_range[0][0]+20, 180,nothing)
    cv2.createTrackbar('Sat', name, def_range[0][1]   , 255, nothing)
    cv2.createTrackbar('Val', name, def_range[0][2]   , 255, nothing)
    while(1):

        frameinv = vs.read()
        frame=cv2.flip(frameinv ,1)
        frame = imutils.resize(frame, width=600)
        cv2.imshow('frame',frame)
        k = cv2.waitKey(5) & 0xFFdd

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hue = cv2.getTrackbarPos('Hue', name)
        sat = cv2.getTrackbarPos('Sat', name)
        val = cv2.getTrackbarPos('Val', name)

        lower = np.array([hue-20,sat,val])
        upper = np.array([hue+20,255,255])

        mask = cv2.inRange(hsv, lower, upper)
        eroded = cv2.erode( mask,None, iterations=1)
        dilated = cv2.dilate( eroded,None, iterations=1)

        cv2.imshow(name, dilated)

        k = cv2.waitKey(5) & 0xFF
        if k == ord('s'):
            cv2.destroyAllWindows()
            return((hue-20,sat,val),(hue+20,255,255))

if __name__ == '__main__':

    print(calib())