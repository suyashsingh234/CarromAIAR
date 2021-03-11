import cv2

video=cv2.VideoCapture(0)

while True:
    ret,vid=video.read()
    cv2.imshow("frame",vid)
    
    
    k = cv2.waitKey(10)
    if k==ord('q'):
        break
     
cv2.destroyAllWindows()