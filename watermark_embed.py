import random
import numpy as np
import cv2

# Number of keypoints to select
N = 100

def embed_watermark(wm_name: str, img_name: str) -> str:
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

    # Embed watermark at each keypoint
    for k in range(len(kp)):
        carrier_img = watermark_kp(carrier_img, kp[k], watermark, wm_size, version)
    cv2.imwrite("cv_assignment/embedded/wm_img_.png", carrier_img)

    return "cv_assignment/embedded/wm_img_.png"

def get_kp(img) -> tuple[list,list]:
    """
    Return N  keypoints from image based on highest response.
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
    
    for k in range(len(kp)):
        if kp_pts.__contains__(kp[k].pt):
            kp_pts.remove(kp[k].pt)
            print(kp[k].size)
            unique_kp.append(kp[k])
            unique_desc.append(desc[k])

    # Sort list of keypoints and select highest N responses
    kp_res = [k.response for k in unique_kp]
    kp_list = [list(s) for s in zip(kp_res, unique_kp, unique_desc)]
    sort_list = sorted(kp_list, key=lambda kp_list: kp_list[0], reverse=True)

    # Returns N keypoints and feature descriptions based on keypoint response
    kp = [s[1] for s in sort_list[:N]]
    desc = [s[2] for s in sort_list[:N]]
    return kp, desc

def watermark_kp(img, kp, watermark, size, version: bool):
    """
    Embed watermark at given keypoint, either as addition to image
    or as subtraction from image.
    """
    x1, x2, y1, y2 = get_kp_crop(img, kp, size)
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

def get_kp_crop(img, kp, size) -> tuple[int,int,int,int]:
    """
    Crop the image around keypoint the size of the watermark.
    """
    # Get keypoint coords as integers
    x_, y_ = kp.pt

    # Get image bounds
    max_x, max_y = img.shape[:2]
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