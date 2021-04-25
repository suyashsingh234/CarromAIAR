#This module runs the game and the AR module in the same process 
# For processing the frames on to camera data make a class or function and import them here 
import cv2
from PIL import Image
from guigame import runner
from queue import Queue 
from threading import Thread
from time import time 
import ar_utilities as utils

def ar_runner():
    print("starting game")
    gamerunner = runner()
    gamerunner.start()
    print("starting video")
    video=cv2.VideoCapture(0)
    marker = cv2.imread("marker.png")
    corners_or, ids_or = utils.detect_markers(marker)

    while True:
        ret,frame=video.read()
        corners_dest, ids_dest = utils.detect_markers(frame)
        board_frame = 0
        try :
            board_state_reciver = gamerunner.board_state_sender()
            if (board_state_reciver == 1):
                print("board not initilized")
            else :
                foto = cv2.imread("tmp.jpg")
                if len(corners_dest) > 0:
                    origin, dest = utils.get_points(ids_or, ids_dest, corners_or, corners_dest)
                    warped_img = utils.warp_image(origin, dest, (frame.shape[0], frame.shape[1]), foto)
                    frame = utils.merge_images(warped_img, frame)
                    cv2.imshow("frame",frame)
                else :
                    cv2.imshow("frame", foto)
        except Exception as e:
            print(e)
            print("image load error")
        k = cv2.waitKey(10)
        if k==ord('z'):
            break
        
    cv2.destroyAllWindows()
    gamerunner.game_quit()
ar_runner()