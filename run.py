#This module runs the game and the AR module in the same process 
# For processing the frames on to camera data make a class or function and import them here 
import cv2
from guigame import runner
from queue import Queue 
from threading import Thread
from time import time 

print("starting game")
gamerunner = runner()
gamerunner.daemon=True
gamerunner.start()
print("starting video")
video=cv2.VideoCapture(0)


while True:
    ret,vid=video.read()
    cv2.imshow("frame",vid)

    k = cv2.waitKey(10)
    if k==ord('z'):
        break
     
cv2.destroyAllWindows()
