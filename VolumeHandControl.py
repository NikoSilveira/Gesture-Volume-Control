import cv2
import time
import numpy as np
import HandTrackingModule as htm

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

    if len(lm_list) != 0:
        print(lm_list[4], lm_list[8]) #Tip of index (4) and thumb (8)

    #FPS
    current_Time = time.time()
    fps = 1/(current_Time - prev_Time)
    prev_Time = current_Time
    cv2.putText(img, 'FPS: '+str(int(fps)), (10,30), cv2.FONT_HERSHEY_PLAIN, 1.4, (255,0,160), 2) #display in window

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'): #shut down with q
        break
