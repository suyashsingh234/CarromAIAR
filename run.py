#This module runs the game and the AR module in the same process 
# For processing the frames on to camera data make a class or function and import them here 
import cv2
from PIL import Image
from guigame import runner
from queue import Queue 
from threading import Thread
from time import time 
import numpy as np
import base64

print("starting game")
gamerunner = runner()
gamerunner.start()
print("starting video")
video=cv2.VideoCapture(0)


while True:
    ret,vid=video.read()
    cv2.imshow("frame",vid)
    try :
        board_state_reciver = gamerunner.board_state_sender()
        if (board_state_reciver == 1):
            print("board not initilized")
        else :
            img = cv2.imread("tmp.jpg", cv2.IMREAD_COLOR) 
            cv2.imshow("board", img)
    except :
        print("image load error")
         
    k = cv2.waitKey(10)
    if k==ord('z'):
        break
     
cv2.destroyAllWindows()
