import cv2
import numpy as np
import math
import os
import watermark_embed as embed
import watermark_recover as recover

# tampering detected -> return YES and display keypoints that do not match
# tampering =
    # cropping - fewer kp than expected?
    # resizing - size/shape of watermarks?
    # rotating - watermark same but rotated

PATH = os.path.dirname(os.path.realpath(__file__))

def detect_tampering(img_name: str):
    img = cv2.imread(img_name)
    kp, desc = get_keypoints(img)

    og_img, og_kp, og_desc = get_original_img(img_name)

    print(len(kp))
    print(len(og_kp))

    bf = cv2.BFMatcher()
    matching_desc = bf.knnMatch(og_desc, desc, k=2)
    ratio_threshold = 0.75

    matches = []
    for m, n in matching_desc:
        if m.distance < ratio_threshold * n.distance:
            matches.append(m)

    og_points = np.array([og_kp[n.queryIdx].pt for n in matches]).reshape(-1,1,2)
    alt_points = np.array([kp[n.trainIdx].pt for n in matches]).reshape(-1,1,2)
    
    H, _ = cv2.findHomography(og_points, alt_points, cv2.RANSAC)
    check_resize(H)
    check_rotate(H)

def process_homography(h):
    a = h[0,0]
    b = h[0,1]
    c = h[0,2]
    d = h[1,0]
    e = h[1,1]
    f = h[1,2]

    p = math.sqrt(a*a + b*b)
    r = (a*e - b*d) / p
    q = (a*d + b*e) /(a*e - b*d)

    translation = (c, f)
    scale = (p, r)
    shear = q
    theta = math.atan2(b, a)
    return translation, theta, scale, shear

def check_crop(h):
    """
    Detect whether the selected image has been cropped.
    """

    return

def check_skew(h):
    """
    Detect whether the selected image has been skewed (shear transform).
    """
    s = [[1, 0.5, 0],
         [0,  1,  1],
         [0,  0,  1]] # top of image moved 0.5 to right
    return

def check_resize(h):
    """
    Detect whether the selected image has been resized.
    """
    i = h[2,2]
    checks = [i, 0, 1]

    a = h[0,0]
    e = h[1,1]

    scale_x = np.round(a/i, 2)
    scale_y = np.round(e/i, 2)

    if not checks.__contains__(scale_x) and not checks.__contains__(scale_y):
        if scale_x == scale_y:
            print(f"Resized by factor of {scale_x}")
        else:
            print(f"Resized in both directions = x: {scale_x}, y: {scale_y}")
    elif not checks.__contains__(scale_x):
        print(f"Resized in x direction = x: {scale_x}")
    elif not checks.__contains__(scale_y):
        print(f"Resized in y direction = y: {scale_y}")
    else: 
        print("Not resized")
        return False
    return True

def check_rotate(h):
    """
    Detect whether the selected image has been rotated.
    """
    i = h[2,2]
    a = normalise_angle(np.round(h[0,0]/i, 2))
    b = normalise_angle(np.round(h[0,1]/i, 2))
    d = normalise_angle(np.round(h[1,0]/i, 2))
    e = normalise_angle(np.round(h[1,1]/i, 2))
    
    degs = [math.acos(a), -math.asin(b), math.asin(d), math.acos(e)]
    print(degs)

    if all(abs(d) != 0.0 for d in degs):
        if all(abs(d) == degs[0] for d in degs):
            print(f"Rotated by {math.degrees(degs[0])} degrees")
        else:
            print("Rotated")
        return True
    return False

def normalise_angle(a):
    if a < -1:
        return normalise_angle(a + 1)
    elif a > 1:
        return normalise_angle(a - 1)
    return a

def get_keypoints(img) -> tuple[list,list]:
    """
    Return keypoints and feature descriptors from image.
    """
    # Import carrier image
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect keypoints and feature descriptions in image
    sift = cv2.SIFT_create()
    kp, desc = sift.detectAndCompute(grey, None)

    # Returns keypoints and feature descriptions
    return kp, desc

def get_original_img(img_name: str):
    """
    Find corresponding original image and return keypoints and feature descriptors.
    """
    if img_name.__contains__("seal"):
        name = "seal"
    elif img_name.__contains__('flower'):
        name = "flower"
    else:
        name = "dashboard"
    
    img = cv2.imread(PATH+"/images/"+name+".png")
    kp, desc = get_keypoints(img)
    return img, kp, desc