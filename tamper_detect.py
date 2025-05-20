import cv2
import numpy as np
import math
import os

# tampering detected -> return YES and display keypoints that do not match

PATH = os.path.dirname(os.path.realpath(__file__))

def detect_tampering(img_name: str, og_name: str):
    img = cv2.imread(img_name)
    kp, desc, grey_img = get_keypoints(img)

    og_img, og_kp, og_desc = get_original_img(og_name)

    og_points, alt_points, matches = get_matches(kp, desc, og_kp, og_desc)
    
    H, _ = cv2.findHomography(og_points, alt_points, cv2.RANSAC)
    if check_resize(H) or check_rotate(H) or check_crop(H):
        print("Tampering detected")
        name = show_discrepancies(og_img, og_kp, grey_img, kp, matches, img_name)
        return True, name
    return False, None

def show_discrepancies(og_img, og_kp, alt_img, alt_kp, matches, img_name):
    kp_matches = cv2.drawMatches(og_img, og_kp, alt_img, alt_kp, matches,
                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                                 singlePointColor=(255,0,0), matchColor=(0,255,0))
    
    name = get_img_name(img_name)
    cv2.imwrite(name, kp_matches)
    return name

def get_matches(kp, desc, og_kp, og_desc):
    bf = cv2.BFMatcher()
    matching_desc = bf.knnMatch(og_desc, desc, k=2)
    ratio_threshold = 0.75

    matches = []
    for m, n in matching_desc:
        if m.distance < ratio_threshold * n.distance:
            matches.append(m)

    og_points = np.array([og_kp[n.queryIdx].pt for n in matches]).reshape(-1,1,2)
    alt_points = np.array([kp[n.trainIdx].pt for n in matches]).reshape(-1,1,2)
    return og_points, alt_points, matches

def check_crop(h):
    """
    Detect whether the selected image has been cropped.
    """
    i = h[2,2]
    c = np.round(h[0,2]/i, 2)
    f = np.round(h[1,2]/i, 2)

    if c < -1 and f < -1:
        return True
    elif f < -1:
        return True
    return False

def check_resize(h):
    """
    Detect whether the selected image has been resized.
    """
    i = h[2,2]
    checks = [i, 0, 1]

    scale_x = np.round(h[0,0]/i, 2)
    scale_y = np.round(h[1,1]/i, 2)

    if not checks.__contains__(scale_x) or not checks.__contains__(scale_y):
        return True
    return False

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

    if all(abs(d) != 0.0 for d in degs):
        return True
    return False

def normalise_angle(a):
    """
    Get angle as value between -1 and 1.
    """
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
    return kp, desc, grey

def get_original_img(img_name: str):
    """
    Find corresponding original image and return keypoints and feature descriptors.
    """
    img = cv2.imread(img_name)
    kp, desc, grey = get_keypoints(img)
    return grey, kp, desc

def get_img_name(img_name: str) -> str:
    """
    Set filepaths to save resulting images at.
    """
    path = PATH.replace("\\", "/")
    name = img_name.replace(path, "").replace("cv_assignment","")
    name = name.replace("/tampered/", "").replace(".png", "")
    
    result = "cv_assignment/detect_matches/"+name
    path = path.replace("cv_assignment", "")
 
    counter = 1
    while os.path.exists(path+result+"_diff.png"):
        result = result.replace(str(counter-1), "")
        result += str(counter)
        counter += 1

    return result+"_diff.png"