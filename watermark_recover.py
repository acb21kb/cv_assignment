import cv2
import numpy as np
import os
import pandas as pd
import watermark_embed as embed

PATH = os.path.dirname(os.path.realpath(__file__))

def recover_watermark(img_name: str) -> str | None:
    """
    Recover watermark from image.
    """
    # Check all keypoints for changes in shape of watermark (watermark is unknown)
    img = cv2.imread(img_name)
    kp, desc = embed.get_kp(img)
    
    og_kp, og_pts, og_desc, og_img = get_og_kp(img_name)

    all_diffs = []
    shape = get_watermark_shape(img_name)
    keypoints = find_same_kp(kp, og_pts)

    for index in keypoints:
        diff = compare_kp(img, og_img, kp[index[0]], og_kp[index[1]], shape)
        all_diffs.append(diff)

    recovery = np.mean(all_diffs, axis=0)

    clean_recovery = recovery.copy()
    clean_recovery[clean_recovery>=127] = 255
    clean_recovery[clean_recovery<127] = 0

    if found_watermark(clean_recovery):
        save_at = save_recovered(img_name)
        cv2.imwrite(save_at, recovery)
        return save_at
    else:
        return None

def get_og_kp(img_name: str) -> tuple[list, list]:
    """
    Return keypoints from corresponding original image.
    """
    if img_name.__contains__("seal"):
        name = "seal"
    elif img_name.__contains__('flower'):
        name = "flower"
    else:
        name = "dashboard"
    
    og_img = cv2.imread(PATH+"/images/"+name+".png")
    kp, desc = embed.get_kp(og_img)
    pts = [(int(p.pt[0]), int(p.pt[1])) for p in kp]
    return kp, pts, desc, og_img

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
    diff = alter - original
    d = np.array(diff)
    d[np.where(d!=0)] = 50
    d[np.where(d==0)] = 255
    d[np.where(d==50)] = 0
    return d

def save_recovered(img_name: str) -> str:
    """
    Save recovered image without overlapping other files.
    """
    name = ""
    if img_name.__contains__("seal"):
        name = "seal"
    elif img_name.__contains__('flower'):
        name = "flower"
    else:
        name = "dashboard"
    result = "cv_assignment/recovered/from_"+name
    path = PATH.replace("\\", "/").replace("cv_assignment", "")
    
    counter = 1
    while os.path.exists(path+result+".png"):
        result = result.replace(str(counter-1), "")
        result += str(counter)
        counter += 1

    return result+".png"

def get_watermark_shape(img_name: str) -> int:
    """
    Return shape of watermark in this image.
    """
    path = PATH.replace("\\", "/")
    img = img_name.replace(path+"/", "")

    df = pd.read_csv(PATH+"/watermarks/img_to_wm.csv")
    match = df[df['Image']==img]
    if not match.empty:
        shape = str(match['Size'].iloc[0])
        shape = shape.split("x")
        return int(shape[0])
    else:
        return 9

def found_watermark(recovered) -> bool:
    path = PATH+"/watermarks/watermark_"
    for i in range(9,1,-2):
        wm = cv2.imread(path+str(i)+"x"+str(i)+".png")
        if np.array_equal(recovered, wm):
            return True
    return False
        
