import os
import numpy as np
import cv2

N = 40

def get_kp(img):
    # Import carrier image
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect keypoints (and feature descriptions) in image
    sift = cv2.SIFT_create()
    sift.setContrastThreshold(0.1)
    kp, desc = sift.detectAndCompute(grey, None)

    # Returns N keypoints and feature descriptions
    return kp[:N], desc[:N]

def process_watermark(wm_name: str, img_name: str):
    # Process watermark into single bits (0 or 1)
    img = cv2.imread(wm_name)
    watermark = np.array([[1 if np.sum(i) < 255 else 0 for i in j] for j in img])

    # All watermarks have same height and width (5x5, 7x7 or 9x9)
    wm_size = np.floor(len(watermark)/2)
    print(wm_size)

    # Get keypoints and feature descriptions of carrier image
    carrier_img = cv2.imread(img_name)
    kp, desc = get_kp(carrier_img)

    for k in kp:
        watermark_kp(carrier_img, k, watermark, wm_size)

    # embedded = (img & watermark)
    return

def watermark_kp(img, kp, watermark, size):
    carrier = get_kp_crop(img, kp)
    # change LSB for each black pixel in watermark

    return

def get_kp_crop(img, kp, size):
    x1 = int(kp.pt[0] - size)
    x2 = int(kp.pt[0] + size)
    y1 = int(kp.pt[1] - size)
    y2 = int(kp.pt[1] + size)

    return img[x1:x2, y1:y2]