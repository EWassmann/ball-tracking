# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
import sys
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import cv2
import serial
import time
h = 700
b = 6
nb = 3
ls = 0
q = 2
a = time.perf_counter()
arduino = serial.Serial(
port = '/dev/ttyACM0',
baudrate = 2000000, #perhaps make this lower need to do research
bytesize = serial.EIGHTBITS,
parity = serial.PARITY_NONE,
stopbits = serial.STOPBITS_ONE,
timeout = 5,
xonxoff = False,
rtscts = False,
dsrdtr = False,
writeTimeout = 2
)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# greenLower = (29, 86, 6)
# greenUpper = (64, 255, 255)
# adjust these values
orangeLower = (0, 170, 150)
orangeUpper = (15, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    

    frame = camera.read()
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "orange", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, orangeLower, orangeUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
  
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        nb = 1
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        #print(radius)

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 0, 0), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1)
            #here is where the movement decisions begin
            #0 is forward 1 is left 2 is right 4 is stop and 3 is go backwards
            if radius < 200:
                if radius <150:
                    if x > 400:
                        if b!= 2:
                            arduino.write("2".encode())
                            b = 2
                            #print(2)
                            #time.sleep(1.3)
                    if x <200:
                        if b != 1:
                            arduino.write("1".encode()) 
                            b = 1
                            #print(1)
                            #time.sleep(1.3)
                    if x > 200 and x < 400:
                        if b != 0: 
                            arduino.write("0".encode())
                            b = 0
                            #print(0)
                            #time.sleep(1.3)
                      
                if radius >= 150:
                    if b != 4:
                        arduino.write("4".encode())
                        b=4
                       #print(4)
            if radius > 200:
                if b!= 3:
                    arduino.write("3".encode())
                    b =3
                    #print(3)
        h = x
    if len(cnts) <=0: #subs this with radius?
    
        if q != 1 and b != 5:
            a = time.perf_counter()
            q = 1
            # if h >300 and b!=2:
            #     arduino.write("2".encode())
            #     b = 2
            #     q = 1
            #     print(2)
            # elif b != 1 :
            #     arduino.write("1".encode())
            #     b = 1
            #     q = 1
            #     print(1)
        if  q != 2 and  time.perf_counter() - a > 7 :
            arduino.write("5".encode())
            b = 5
            #print(5)
            q = 2
        
        

  #b keeps track of what the last command given was, ls keeps track of what the last search command rotation was, h is used to retrieve the previous x value.
  # nb keeps track if the robot searched the last time through the loop or if it caught a glimpse of the ball. the intention is that if it was searching in a clockwise motion, caught the ball
  # and went straight or something and then lost it, it should now go in a counter clockwise motion because it probably overshot the ball  q is wether it is in search mode or still looking close to 
  # where it was for the ball, and a is the beggining of the search mode timer     



            
            




    # update the points queue
    pts.appendleft(center)


 
#uncomment below if you want to view the video
    # # show the frame to our screen
    # cv2.imshow("Image Tracker", frame)
    # key = cv2.waitKey(1) & 0xFF

    # # if the 'q' key is pressed, stop the loop
    # if key == ord("q"):
    #     break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
