# original:https://github.com/pdhruv93/computer-vision/tree/main/fingers-count
# original is modified by takefuji
from operator import truediv
from xmlrpc.client import Boolean
import mediapipe as mp
import cv2
import math
import numpy as np
import os
import  pyfirmata
from time import sleep

Hands = mp.solutions.hands
Draw = mp.solutions.drawing_utils
b=pyfirmata.Arduino('COM7')

class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = Hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence,
                                   min_tracking_confidence=min_tracking_confidence)

    def findHandLandMarks(self, image, handNumber=0, draw=False):
        originalImage = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe needs RGB
        results = self.hands.process(image)
        landMarkList = []

        if results.multi_handedness:
            label = results.multi_handedness[handNumber].classification[0].label  # label gives if hand is left or right
            #account for inversion in cam
            if label == "Left":
                label = "Right"
            elif label == "Right":
                label = "Left"

        if results.multi_hand_landmarks:  # returns None if hand is not found
            hand = results.multi_hand_landmarks[handNumber] #results.multi_hand_landmarks returns landMarks for all the hands

            for id, landMark in enumerate(hand.landmark):
                # landMark holds x,y,z ratios of single landmark
                imgH, imgW, imgC = originalImage.shape  # height, width, channel for image
                xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                landMarkList.append([id, xPos, yPos, label])

            if draw:
                Draw.draw_landmarks(originalImage, hand, Hands.HAND_CONNECTIONS)
        return landMarkList


handDetector = HandDetector(min_detection_confidence=0.7)

def get_num(hand):
    if hand == [0,1,0,0,0]:
        return 1
    elif hand == [0,1,1,0,0]:
        return 2
    elif hand == [0,1,1,1,0]:
        return 3
    elif hand == [0,1,1,1,1]:
        return 4
    elif hand == [1,1,1,1,1]:
        return 5
    elif hand == [1,0,0,0,0]:
        return 6
    elif hand == [1,1,0,0,0]:
        return 7
    elif hand == [1,1,1,0,0]:
        return 8
    elif hand == [1,1,1,1,0]:
        return 9
    else:
        return "Nan"

def light_number(DEC,b,LED_qua):
  if DEC>=2**LED_qua:
    for i in range(LED_qua):
      b.digital[i+2].write(1)
  else:
    BIN_list = list(str(bin(DEC)))[2:]
    for val,i in zip(reversed(BIN_list),range(len(BIN_list))):
      b.digital[LED_qua-i+1].write(int(val))

def main():
 cam = cv2.VideoCapture(0)
 progress_bar = "-----"
 progress_num = 0
 before_hand = [0,0,0,0,0]
 before_kigou = "Nane"
 mode = 0
 cal = ""
 cal_dis = ["_","_","_"]
 ans = "_"
 go_next = False
 while True:
    status, image = cam.read()
    image =cv2.flip(image,1)
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    hand = [0,0,0,0,0]
    hand_num = "Nan"
    kigou = "Nane"
    if(len(handLandmarks) != 0):
        if handLandmarks[4][1]+50 < handLandmarks[5][1]:       #Thumb finger
            hand[0] = 1
        if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
            hand[1] = 1
        if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
            hand[2] = 1
        if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
            hand[3] = 1
        if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
            hand[4] = 1

        if mode == 1:
            if (320 <= handLandmarks[8][1] <= 420) and (50 <= handLandmarks[8][2] <= 150):
                kigou = "+"
            elif (450 <= handLandmarks[8][1] <= 550) and (50 <= handLandmarks[8][2] <= 150):
                kigou = "*"
        if mode == 3:
            go_next = Boolean((320 <= handLandmarks[8][1] <= 600) and (50 <= handLandmarks[8][2] <= 150))



    # 数字決定
    hand_num = get_num(hand)
    if hand_num != "Nan" and mode != 3:
        for i in range(7):
            b.digital[i+2].write(0)
        light_number(hand_num,b,7)
    elif mode == 3:
        pass
    else:
        for i in range(7):
            b.digital[i+2].write(0)
    if mode == 1:
        hand_num = kigou

    # progress 進める
    if hand == before_hand and hand_num != "Nan" and (mode == 0 or mode == 2):
        progress_num += 1
    elif before_kigou == kigou and kigou in ["+","*"] and mode == 1:
        progress_num += 1
    elif go_next and mode == 3:
        progress_num += 1
    else:
        progress_num = 0

    # progress bar作製
    if progress_num > 40:
        progress_bar = "#####"
    elif progress_num > 30:
        progress_bar = "####-"
    elif progress_num > 20:
        progress_bar = "###--"
    elif progress_num > 10:
        progress_bar = "##---"
    elif progress_num > 0:
        progress_bar = "#----"
    else:
        progress_bar = "-----"

    # progressが進んだ場合の処理
    if progress_num >50:
        if mode == 0:
            cal += str(hand_num)
            cal_dis[0] = str(hand_num)
            mode = 1
            progress_num = 0
            before_hand = [0,0,0,0,0]
        elif mode == 1:
            cal += str(hand_num)
            cal_dis[1] = str(hand_num)
            mode = 2
            progress_num = 0
            before_hand = [0,0,0,0,0]
        elif mode == 2:
            cal += str(hand_num)
            cal_dis[2] = str(hand_num)
            mode = 3
            ans = eval(cal)
            light_number(int(ans),b,7)
            progress_num = 0
            before_hand = [0,0,0,0,0]
        elif mode == 3:
            progress_bar = "-----"
            progress_num = 0
            before_hand = [0,0,0,0,0]
            before_kigou = "Nane"
            mode = 0
            cal = ""
            cal_dis = ["_","_","_"]
            ans = "_"
            go_next = False







    before_hand = hand
    before_kigou = kigou
    if mode == 1:
        if kigou == "Nane":
            cv2.rectangle(image, (320, 50), (420, 150), (255, 0, 0),thickness=4)
            cv2.putText(image, "+", (333, 128), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
            cv2.rectangle(image, (450, 50), (550, 150), (255, 0, 0),thickness=4)
            cv2.putText(image, "*", (475, 130), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
        elif kigou == "*":
            cv2.rectangle(image, (320, 50), (420, 150), (255, 0, 0),thickness=4)
            cv2.putText(image, "+", (333, 128), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
            cv2.rectangle(image, (450, 50), (550, 150), (255, 0, 0),thickness=-1)
            cv2.putText(image, "*", (475, 130), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
        elif kigou == "+":
            cv2.rectangle(image, (320, 50), (420, 150), (255, 0, 0),thickness=-1)
            cv2.putText(image, "+", (333, 128), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
            cv2.rectangle(image, (450, 50), (550, 150), (255, 0, 0),thickness=4)
            cv2.putText(image, "*", (475, 130), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
    if mode == 3:
        if go_next == False:
            cv2.rectangle(image, (320, 50), (600, 150), (255, 0, 0),thickness=4)
            cv2.putText(image, "Reset", (333, 128), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
        if go_next == True:
            cv2.rectangle(image, (320, 50), (600, 150), (255, 0, 0),thickness=-1)
            cv2.putText(image, "Reset", (333, 128), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)

    cv2.putText(image, str(hand), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(image, str(hand_num), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
    cv2.putText(image, progress_bar, (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(image, f"equation: {cal_dis[0]} {cal_dis[1]} {cal_dis[2]} ", (0, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(image, f"anser:  {cal_dis[0]} {cal_dis[1]} {cal_dis[2]}  = {ans} ", (0, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("result", image)
    cv2.moveWindow("result",200,200)
    cv2.setWindowProperty("result", cv2.WND_PROP_TOPMOST, 1)
    if cv2.waitKey(1) == ord('q'):
        cam.release()
        cv2.destroyWindow("result")
        break

if __name__ == '__main__':
 main()
 os._exit(0)