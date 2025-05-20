import cv2
import numpy as np
import os
import pandas as pd

import watermark_embed as embed

PATH = os.path.dirname(os.path.realpath(__file__))

def recover_watermark(img_name: str, return_img: bool = True):
    """
    Recover watermark from image.
    """
    # Check all keypoints for changes in shape of watermark (watermark is unknown)
    img = cv2.imread(img_name)
    kp, desc = embed.get_kp(img)

    og_name = get_original_img(img_name)
    og_img = cv2.imread(og_name)
    og_kp, og_pts, og_desc = get_og_kp(og_img)

    all_diffs = []
    found_wm = []

    shape = get_watermark_shape(img_name)
    keypoints = find_same_kp(kp, og_pts)

    # For each keypoint in both testing image and original image, compare pixel alterations
    for index in keypoints:
        diff = compare_kp(img, og_img, kp[index[0]], og_kp[index[1]], shape)
        all_diffs.append(diff)
        # Calculate how much the difference matches the watermark with the same shape
        found_wm.append(int(found_watermark(diff, shape)))

    # Take average recovered watermark
    recovery = np.mean(all_diffs, axis=0)
    # Calculate average watermark similarity
    recovery_match = np.mean(found_wm)
    
    # Give leeway for watermark overlap
    if recovery_match > 0.25:        
        recovery *= 255 # Will output inverted to original watermark
        if return_img:
            save_at = save_recovered(img_name)
            cv2.imwrite(save_at, recovery)
            return True, save_at, recovery_match
    else:
        return False, all_diffs, found_wm

def get_og_kp(og_img):
    """
    Return keypoints from corresponding original image.
    """
    kp, desc = embed.get_kp(og_img)
    pts = [(int(p.pt[0]), int(p.pt[1])) for p in kp]
    return kp, pts, desc

def find_same_kp(kp: list, og_kp: list) -> list:
    """
    Return list of keypoints that are in both watermarked and original image to avoid invalid
    searches.
    """
    keypoints = []
    for k in range(len(kp)):
        point = (int(kp[k].pt[0]), int(kp[k].pt[1]))
        try:
            i = og_kp.index(point)
            keypoints.append([k, i])
        except:
            pass
    return keypoints

def compare_kp(img, og_img, kp, og_kp, shape):
    """
    Get area around keypoint in both images and process the difference between them.
    """
    size = np.floor(shape/2)
    x1, x2, y1, y2 = embed.get_kp_crop(img.shape[0], img.shape[1], kp, size)
    x3, x4, y3, y4 = embed.get_kp_crop(og_img.shape[0], og_img.shape[1], og_kp, size)
    alter = img[x1:x2, y1:y2]
    original = og_img[x3:x4, y3:y4]

    diff = np.zeros_like(alter)
    for i in range(alter.shape[0]):
        for j in range(alter.shape[1]):
            for n in range(alter.shape[2]):
                # Gets least significatn bit back from altered image
                diff[i][j][n] = alter[i][j][n] & 0b00000001
    return diff

def save_recovered(img_name: str) -> str:
    """
    Save recovered image without overlapping other files.
    """
    path = PATH.replace("\\", "/")
    name = img_name.replace(path, "")
    name = name.replace("/embedded/wm_img_", "").replace(".png", "")

    result = "cv_assignment/recovered/from_"+name
    path = path.replace("cv_assignment", "")

    counter = 1
    while os.path.exists(path+result+".png"):
        result = result.replace(str(counter-1), "")
        result += str(counter)
        counter += 1

    return result+".png"

def get_original_img(img_name: str):
    """
    Return corresponding original image filename.
    """
    img = img_name.split("/cv_assignment/")
    img = img[-1]
    # Find corresponding watermark size stored in csv by image name
    df = pd.read_csv(PATH+"/watermarks/img_to_wm.csv")
    match = df[df['Image']==img]
    if not match.empty:
        og_img = str(match['Original'].iloc[0])
        return "cv_assignment/"+og_img

def get_watermark_shape(img_name: str) -> int:
    """
    Return shape of watermark in this image.
    """
    path = PATH.replace("\\", "/")
    img = img_name.replace(path+"/", "")

    # Find corresponding watermark size stored in csv by image name
    df = pd.read_csv(PATH+"/watermarks/img_to_wm.csv")
    match = df[df['Image']==img]
    if not match.empty:
        shape = str(match['Size'].iloc[0])
        shape = shape.split("x")
        return int(shape[0])
    
    # If image is not found in csv, return watermark as largest size (9x9) as default
    return 9

def found_watermark(recovered, size) -> bool:
    """
    Return True if recovered watermark matches the actual watermark for the given size.
    """
    path = PATH+"/watermarks/watermark_"
    wm = cv2.imread(path+str(size)+"x"+str(size)+".png")
    watermark = [[[1,1,1] if np.sum(i) < 255 else [0,0,0] for i in j] for j in wm]
    inverted_watermark = [[[0,0,0] if np.sum(i) < 255 else [1,1,1] for i in j] for j in wm]
    
    # If recovered is a perfect match, return True
    if np.array_equal(recovered, watermark) or np.array_equal(recovered, inverted_watermark):
        return 1
    else:
        # Give a percentage error for calculating watermark match due to potential overlaps
        # Otherwise, not a strong enough match to verify watermark
        similarity = get_diff(recovered, watermark)
        similarity_inv = get_diff(recovered, inverted_watermark)
        if similarity > similarity_inv:
            return similarity
        else:
            return similarity_inv

def get_diff(r, wm):
    """
    Calculate percentage match of recovered watermark and actual watermark.
    """
    matches = 0
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            for n in range(r.shape[2]):
                if r[i][j][n] == wm[i][j][n]:
                    matches += 1

    return matches/(r.shape[0]*r.shape[1]*r.shape[2])