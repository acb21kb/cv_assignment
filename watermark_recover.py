import numpy as np
import cv2
import watermark_embed as embed

def get_watermark(img_name, og_name, shape:int):
    # Check all keypoints for changes in shape of watermark (watermark is unknown)
    img = cv2.imread(img_name)
    kp, desc = embed.get_kp(img)

    og_img = cv2.imread(og_name)
    og_kp, og_desc = embed.get_kp(og_img)
    print(len(kp), len(og_kp))
    return

