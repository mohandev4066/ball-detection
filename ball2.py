import numpy as np
import cv2
import imutils
from PIL import Image


greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

cap = cv2.VideoCapture(0)


while 1:
    ret, img = cap.read()

    img = imutils.resize(img, width=600)
    blurred = cv2.GaussianBlur(img, (11, 11), 7)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)



    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:

        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        print(radius)


        if(x<200):
            print("left")

        if(x<400 and x>200):
            print("straight")

        if(x>400 and x<600):
            print("right")



        if radius > 5:

            cv2.circle(img, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(img, center, 5, (0, 0, 255), -1)


        if(radius<5):
            print("stop")



    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()