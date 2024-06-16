import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

def decodeImage(img) :
    decoded_Objects = pyzbar.decode(img)
    for ob in decoded_Objects:
        print('Type = ', ob.type)
        print('Data = ', ob.data,'\n')
    return decoded_Objects

def displayImage(img, decoded_Objects):
    for decoded_Object in decoded_Objects:
        detected_points = decoded_Object.polygon
        if len(detected_points) > 4 :
            hulls = cv2.convexHull(np.array([point for point in detected_points], dtype=np.float32))
            hulls = list(map(tuple, np.squeeze(hulls)))
        else :
            hulls = detected_points;
        size = len(hulls)
        for j in range(0,size):
            cv2.line(img, hulls[j], hulls[ (j+1) % size], (255,0,0), 3)
    cv2.imshow("Results", img);
    cv2.waitKey(0);

img = cv2.imread('images/3.png')
decoded_Objects = decodeImage(img)
displayImage(img, decoded_Objects)    
