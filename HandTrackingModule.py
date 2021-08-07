import cv2
import mediapipe as mp
import time

class handDetector():

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxhands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        #init hand processing vars
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxhands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, hand_num=0, draw=False):
        lm_list = []  #Empty landmark list

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_num] #point to specific hand

            for id, lm in enumerate(myHand.landmark):   #Iterate through all landmarks
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)   #Transform landmark pos values into pixel values
                lm_list.append([id, cx, cy])            #CHOOSE HERE WHAT TO APPEND

                if draw: #Custom draw for circles. Default: False
                    cv2.circle(img, (cx,cy), 8, (255, 0, 0), cv2.FILLED)

        return lm_list


#### Dummy Main Function####

#Ignore if being imported into another file
#Copy main() contents to another file, add import of module and add to file

def main():
    cap = cv2.VideoCapture(0) #Camera

    pTime = 0
    cTime = 0

    detector = handDetector()
    
    while True:
        success, img = cap.read() #Hand image
        img = detector.findHands(img)
        lm_list = detector.findPosition(img)

        if len(lm_list) != 0: #Check if list not empty
            print(lm_list[8])

        #FPS
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (0,210,0), 2) #display in window

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'): #shut down with q
            break

if __name__ == "__main__":
    main()