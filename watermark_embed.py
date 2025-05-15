import numpy as np
import cv2

def get_kp(img_name: str):
    print(img_name)
    img = cv2.imread(img_name)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    kp = sift.detect(grey, None)

    img = cv2.drawKeypoints(grey, kp, img)
    print("get kp")
    cv2.imwrite("cv_assignment/images/sift_kp_.png", img)

