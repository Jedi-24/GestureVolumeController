import cv2
import mediapipe as mp
import time  # to check frame rate



class handDetector():
    def __init__(self,mode=False,maxHands = 2,detectionCon=0.5,trackCon=0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # hand detection.
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)  # made an object from the class 'hands'
        self.mpDraw = mp.solutions.drawing_utils
        self.Ftips = [4, 8, 12, 16, 20]


    def findHands(self,img , draw = True):
        imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRgb)  # process() is an inbuilt method.
        # print(results.multi_hand_landmarks)   #to get to know when the hand is detected.

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)  # drawing hand points and lines joining those points.

        return img

    def findPosition(self, img, handNo=0, draw=True):

        self.lmList= []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 255, 0), cv2.FILLED)

        return self.lmList

#important function to be used in virtual mouse project.
    def fingerUp(self):
        fingers = []
        # for thumb only :)
        if self.lmList[self.Ftips[0]][1] < self.lmList[self.Ftips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #for four fingers :)
        for id in range(1, 5):
            if self.lmList[self.Ftips[id]][2] < self.lmList[self.Ftips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers


def main():
    # for frameRate
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()  # no need to give any parameters, because default params are already given.
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        # used to get frame rate.
        cTime = time.time()  # gives us current time.
        fps = 1 / (cTime - pTime)  # don't know the math here. google it.
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow('image:', img)
        cv2.waitKey(1)


# Guarded script to be executed only when this module runs as a 'main' module.
if __name__ == "__main__":
    main()
