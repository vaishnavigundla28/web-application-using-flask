import numpy as np
import cv2

def scan(path):
    img = cv2.imread(path)
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe_obj = cv2.createCLAHE(clipLimit = 2.0, tileGridSize = (8,8))
    grayImage = clahe_obj.apply(grayImage)
    edge_enhance = cv2.Laplacian(grayImage, ddepth = cv2.CV_8U, ksize = 3, scale = 1, delta = 0)
    blurredImage = cv2.bilateralFilter(edge_enhance, 13, 50, 50)
    (_, threshold) = cv2.threshold(blurredImage, 55, 255, cv2.THRESH_BINARY)
    
    kernel_morph = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    enhance = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel_morph)
    enhance = cv2.erode(enhance, None, iterations = 4)
    enhance = cv2.dilate(enhance, None, iterations = 4)
    
    (contours, _) = cv2.findContours(enhance.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    con = sorted(contours, key = cv2.contourArea, reverse = True)[0]
    rectangle = cv2.minAreaRect(con)
    boxes = np.int0(cv2.boxPoints(rectangle))
    cv2.drawContours(img, [boxes], -1, (0, 255, 0), 3)
    img = cv2.resize(img, (800,800))
    cv2.imshow("output",img)
    cv2.waitKey(0)


scan("images/4.png")
