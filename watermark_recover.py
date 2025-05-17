import numpy as np
import cv2

def get_watermark(img_name, shape:int):
    # Check all keypoints for changes in shape of watermark (watermark is unknown)
    img = cv2.imread(img_name)
    kp, desc = retrieve_kp(img)
    return

def retrieve_kp(img) -> tuple[list,list]:
    """
    Return (unique) keypoints from image.
    """
    # Import carrier image
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect keypoints (and feature descriptions) in image
    sift = cv2.SIFT_create()
    sift.setContrastThreshold(0.1)
    kp, desc = sift.detectAndCompute(grey, None)

    # Get unique keypoints
    kp_pts = set([k.pt for k in kp])
    unique_kp = []
    unique_desc = []
    
    # Return unique keypoints (no need for ones that overlap)
    for k in range(len(kp)):
        if kp_pts.__contains__(kp[k].pt):
            kp_pts.remove(kp[k].pt)
            print(kp[k].size)
            unique_kp.append(kp[k])
            unique_desc.append(desc[k])

    return unique_kp, unique_desc