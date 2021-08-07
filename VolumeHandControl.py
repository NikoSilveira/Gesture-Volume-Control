import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

#### Parameters ####
cam_width, cam_height = 640, 480

#### Video Capture ####
cap = cv2.VideoCapture(0) #Camera
cap.set(3, cam_width)
cap.set(4, cam_height)

prev_Time = 0

detector = htm.handDetector(detectionCon=0.7) #Create detector object; conf 0.7: want to be quite sure it is a hand

while True:
    success, img = cap.read()
    detector.findHands(img)
    lm_list = detector.findPosition(img)

    #Handling of desired landmarks - tip of index (8) and tip of thumb (4)
    if len(lm_list) != 0:
        x4, y4 = lm_list[4][1], lm_list[4][2]
        x8, y8 = lm_list[8][1], lm_list[8][2]
        center_x, center_y = (x4+x8)//2, (y4+y8)//2

        #Custom drawing
        cv2.circle(img, (x4,y4), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x8,y8), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x4,y4), (x8,y8), (255,0,255), 3)
        cv2.circle(img, (center_x,center_y), 8, (255,40,160), cv2.FILLED)

        #Line length variations
        line_length = math.hypot(x8-x4, y8-y4)
        
        if line_length < 50:
            cv2.circle(img, (center_x,center_y), 8, (0,255,0), cv2.FILLED)

    #FPS
    current_Time = time.time()
    fps = 1/(current_Time - prev_Time)
    prev_Time = current_Time
    cv2.putText(img, 'FPS: '+str(int(fps)), (10,30), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,0,160), 2) #display in window

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'): #shut down with q
        break
