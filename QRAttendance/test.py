'''
import time    
dd = time.strftime('%Y-%m-%d')
print(dd)
'''
'''
import cv2

detector = cv2.QRCodeDetector()

img = cv2.imread("read1.png")
data, bbox, _ = detector.detectAndDecode(img)
if bbox is not None:
    for i in range(len(bbox)):
        cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)

    if data:
        print("[+] QR Code detected, data:", data)

# display the result
cv2.imshow("img", img)
cv2.waitKey(0)

'''
import numpy as np
import cv2
'''
def scan(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    edge_enh = cv2.Laplacian(gray, ddepth = cv2.CV_8U, ksize = 3, scale = 1, delta = 0)
    blurred = cv2.bilateralFilter(edge_enh, 13, 50, 50)
    (_, thresh) = cv2.threshold(blurred, 55, 255, cv2.THRESH_BINARY)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations = 4)
    closed = cv2.dilate(closed, None, iterations = 4)
    
    # find contours left in the image
    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
    image = cv2.resize(image, (800,800))
    cv2.imshow("aa",image)
    cv2.waitKey(0)


scan("images/4.png")
'''


import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

def decode(im) :
    decodedObjects = pyzbar.decode(im)
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')
    return decodedObjects

def display(im, decodedObjects):
    for decodedObject in decodedObjects:
        points = decodedObject.polygon
        if len(points) > 4 :
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else :
            hull = points;
        n = len(hull)
        for j in range(0,n):
            cv2.rect(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)
    cv2.imshow("Results", im);
    cv2.waitKey(0);

if __name__ == '__main__':
    for i in range(1,6):
        im = cv2.imread('images/'+str(i)+'.png')
        decodedObjects = decode(im)
        display(im, decodedObjects)

