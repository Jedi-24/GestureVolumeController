import cv2
import mediapipe as mp
import numpy as np
import time
import HandTrackingModule as htm
import math


wcam, hcam = 640, 480



cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0
#detector is an object of the class handDetector
detector = htm.handDetector(detectionCon=0.75 , trackCon= 0.69)  #default parameters present in class already , no need to pass anything



from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)








while True:
     success, img = cap.read()
     img = detector.findHands(img)
     lmList = detector.findPosition(img, draw=False)
     if len(lmList) !=0:
          x1, y1 = lmList[4][1], lmList[4][2]
          x2, y2 = lmList[8][1], lmList[8][2]
          cx, cy = (x1+x2)//2, (y1+y2)//2
          #print(lmList[4], lmList[8])
          cv2.circle(img, (x1, y1), 8, (255, 255, 0), cv2.FILLED)
          cv2.circle(img, (x2, y2), 8, (255, 255, 0), cv2.FILLED)
          cv2.circle(img, (cx, cy), 9, (0, 0, 255), cv2.FILLED)
          cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 3)


          length = math.hypot(x2-x1, y2-y1)
          print(length)  # 30 --> 220


          if length < 33:
               cv2.circle(img, (cx, cy), 9, (0, 255, 0), cv2.FILLED)



     cTime = time.time()
     fps = 1/(cTime-pTime)
     pTime = cTime

     cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0),3)


     cv2.imshow('image', img)
     cv2.waitKey(1)
