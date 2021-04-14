# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import math
import argparse
import cv2
import imutils
import time
from calibration import calib
import pyautogui
# construct the argument parse and parse the argument


def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


blueLower,blueUpper = calib()
print(blueLower,blueUpper)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

if not args.get("video", False):
    vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm
time.sleep(3.0)
frames = []

i = 0
while (True):
    # grab the current frame
    frame = vs.read()

    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #print(frame.shape)
    fcenter = (frame.shape[0]/2,frame.shape[1]/2)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, blueLower, blueUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if(len(cnts) == 0):
        print("There is no gesture to detect")
        break
    cnts = imutils.grab_contours(cnts)
    #print(cnts)
    if (len(cnts) == 0):
        print("There is no gesture to detect")
        break
    c = max(cnts, key=cv2.contourArea)
    #print(c)
    #cnt = contours[0]
    M = cv2.moments(c)
    #mask = cv2.drawContours(mask,[c], 0, (0,255,255), 3)
    #cnts = imutils.grab_contours(cnts)
    #frames.append(frame)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    angle = getAngle((cx,cy),fcenter,(fcenter[0]+1,fcenter[1]))
    #print(angle)
    if(i%300 == 0):
        if(angle >=315 or angle<45):
            pyautogui.press('d')
            print("right")
        elif(angle>=45 and angle < 135):
            pyautogui.press('w')
            print("up")
        elif (angle >= 135 and angle < 225):
            pyautogui.press('a')
            print("left")
        elif (angle >= 225 and angle < 315):
            pyautogui.press('s')
            print("down")
    i = i + 1


    cv2.imshow("frame",mask)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    i = i+1
    if frame is None:
        break

#cv2.imwrite("image4.png",frames[2])
#vs.release()
cv2.destroyAllWindows()

