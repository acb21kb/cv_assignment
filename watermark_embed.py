import csv
import cv2
import numpy as np
import os
import random

PATH = os.path.dirname(os.path.realpath(__file__))

def embed_watermark(wm_name: str, img_name: str, display_drastic: int) -> str:
    """
    Implement embedding of watermark.
    """
    # Process watermark into single bits (0 or 1)
    img = cv2.imread(wm_name)
    watermark = np.array([[1 if np.sum(i) < 255 else 0 for i in j] for j in img])

    # All watermarks have same height and width
    wm_size = np.floor(len(watermark)/2)

    # Set version - determines whether the watermark is additive or subtractive
    version = random.choice([True, False])

    # Get keypoints and feature descriptions of carrier image
    carrier_img = cv2.imread(img_name)
    kp, desc = get_kp(carrier_img)

    # Set result image filepaths
    result, result_drastic = get_img_name(img_name)
    store_in_csv(result, wm_name)
    
    # Embed watermark at each keypoint
    for k in range(len(kp)):
        carrier_img = watermark_kp(carrier_img, kp[k], watermark, wm_size, version)

    cv2.imwrite(result, carrier_img)
    if display_drastic == 1:
        watermark_drastic = np.array([[50 if np.sum(i) < 255 else 0 for i in j] for j in img])
        show_img = carrier_img.copy()
        for k in range(len(kp)):
            show_img = watermark_kp(show_img, kp[k], watermark_drastic, wm_size, version)
        cv2.imwrite(result_drastic, show_img)

    return result, result_drastic

def get_kp(img) -> tuple[list,list]:
    """
    Return unique keypoints from image.
    """
    # Import carrier image
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect keypoints (and feature descriptions) in image
    sift = cv2.SIFT_create()
    # sift.setContrastThreshold(0.1)
    kp, desc = sift.detectAndCompute(grey, None)

    # Get unique keypoints
    kp_pts = set([k.pt for k in kp])
    unique_kp = []
    unique_desc = []
    
    for k in range(len(kp)):
        if kp_pts.__contains__(kp[k].pt):
            kp_pts.remove(kp[k].pt)
            unique_kp.append(kp[k])
            unique_desc.append(desc[k])

    # Returns keypoints and feature descriptions
    return unique_kp, unique_desc

def watermark_kp(img, kp, watermark, size: int, version: bool):
    """
    Embed watermark at given keypoint, either as addition to image
    or as subtraction from image.
    """
    x1, x2, y1, y2 = get_kp_crop(img.shape[0], img.shape[1], kp, size)
    carrier = img[x1:x2, y1:y2]

    # Change LSB for each black pixel in watermark
    for i in range(carrier.shape[0]):
        for j in range(carrier.shape[1]):
            for n in range(carrier.shape[2]):
                if version:
                    # Check that value never increases past 255
                    carrier[i][j][n] = min(carrier[i][j][n]+watermark[i][j], 255)
                else:
                    # Check that value never decreases past 0
                    carrier[i][j][n] = max(carrier[i][j][n]-watermark[i][j], 0)

    img[x1:x2, y1:y2] = carrier
    return img

def get_kp_crop(max_x: int, max_y: int, kp, size: int) -> tuple[int,int,int,int]:
    """
    Crop the image around keypoint the size of the watermark.
    """
    # Get keypoint coords as integers
    y_, x_ = kp.pt

    # Get watermark width
    w = (size * 2) + 1
   
    # Ensure area around keypoints are within image bounds
    if x_ - size < w:
        x_ = size
    elif x_ + size + 1 > max_x:
        x_ = max_x - size - 1
    
    if y_ - size < w:
        y_ = size
    elif y_ + size + 1 > max_y:
        y_ = max_y - size - 1

    x1 = int(x_ - size)
    x2 = int(x_ + size + 1)
    y1 = int(y_ - size)
    y2 = int(y_ + size + 1)

    return x1, x2, y1, y2

def get_img_name(img_name: str) -> tuple[str, str]:
    """
    Set filepaths to save resulting images at.
    """
    name = ""
    if img_name.__contains__("seal"):
        name = "seal"
    elif img_name.__contains__('flower'):
        name = "flower"
    else:
        name = "dashboard"
    
    result = "cv_assignment/embedded/wm_img_"+name
    path = PATH.replace("\\", "/").replace("cv_assignment", "")
    
    counter = 1
    while os.path.exists(path+result+".png"):
        result = result.replace(str(counter-1), "")
        result += str(counter)
        counter += 1

    return result+".png", result+"_drastic.png"

def store_in_csv(img_name, watermark):
    """
    Store resulting image and watermark size used in csv file.
    """
    wm_size = get_watermark_size(watermark)
    img = img_name.replace("cv_assignment/", "")
    with open(PATH+"/watermarks/img_to_wm.csv", "a", newline="") as f:
        w = csv.writer(f)
        w.writerow([img, wm_size])

def get_watermark_size(wm_file: str):
    """
    Return size of watermark given the filename.
    """
    wm = wm_file.split("watermark_")
    wm = wm[1].split(".")
    return wm[0]