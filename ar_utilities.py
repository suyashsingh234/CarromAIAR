import cv2
import numpy as np

def detect_markers(img):
    aruco_dict = cv2.aruco.DICT_6X6_1000
    retval = cv2.aruco.getPredefinedDictionary(aruco_dict)
    corners, ids, _ = cv2.aruco.detectMarkers(img, retval)
    return (corners, ids)

def get_points(ids_or, ids_dest, corners_or, corners_dest):
    dest = []
    origin = []
    for i in range(len(ids_dest)):
        list_idx = np.where(ids_or == ids_dest[i])[0]
        if len(list_idx) > 0:
            idx = list_idx[0]
            dest.append(corners_dest[i])
            origin.append(corners_or[idx])

    new_shape = (int(np.prod(np.array(dest).shape) / 2), 2)

    dest = np.array(dest).reshape(new_shape).astype(int)
    origin = np.array(origin).reshape(new_shape).astype(int)
    return (origin, dest)

def warp_image(origin, dest, shape, image):
    homography = cv2.findHomography(origin, dest)[0]
    dst = cv2.warpPerspective(image, homography, dsize=(shape[1], shape[0]))
    return dst

def merge_images(img, frame):
    img1 = img
    img1 = np.where(img1 == 0, 1, img1)
    img1 = np.where(img1 != 1, 0, img1)
    frame *= img1
    frame += img
    np.clip(frame, 0, 255, out=frame)
    return frame

