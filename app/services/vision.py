import numpy as np
import cv2
from PIL import Image

def _floor_crop(pil_img, start_ratio=0.55, maxw=480):
    W, H = pil_img.size
    y0 = int(H * start_ratio)
    crop = pil_img.crop((0, y0, W, H))
    if crop.width > maxw:
        nh = int(crop.height * maxw / crop.width)
        crop = crop.resize((maxw, nh), Image.BILINEAR)
    return crop

def _quick_floor_mask(pil_crop):
    """简化的地板二值化，用于几何预判"""
    g = np.array(pil_crop.convert('L'))
    g = cv2.GaussianBlur(g, (3,3), 0)
    bw = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 21, 2)
    # 简单的形态学处理
    k = np.ones((3,3), np.uint8)
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, k, iterations=1)
    return (bw > 0).astype(np.uint8)

def vconcat_full_and_floor(full_pil, floor_pil, maxw=640):
    """竖向拼接全图和地板裁切图 (vconcat)"""
    # 确保两图宽度一致
    if full_pil.width > maxw:
        nh = int(full_pil.height * maxw / full_pil.width)
        full_pil = full_pil.resize((maxw, nh), Image.BILINEAR)
        
    w = max(full_pil.width, floor_pil.width)
    if full_pil.width != w:
        nh = int(full_pil.height * w / full_pil.width)
        full_pil = full_pil.resize((w, nh), Image.BILINEAR)
    if floor_pil.width != w:
        nh = int(floor_pil.height * w / floor_pil.width)
        floor_pil = floor_pil.resize((w, nh), Image.BILINEAR)
    
    # 拼接
    canvas = Image.new("RGB", (w, full_pil.height + floor_pil.height), (0,0,0))
    canvas.paste(full_pil, (0,0))
    canvas.paste(floor_pil, (0,full_pil.height))
    return canvas

def pre_veto_from_frame(pil_img):
    """
    几何预判的入口函数。
    返回 pre_veto, feats, floor_crop_img。
    当前简化版只返回 floor_crop_img 用于 VLM。
    """
    floor_crop_img = _floor_crop(pil_img)
    pre_veto = {} 
    feats = {}
    return pre_veto, feats, floor_crop_img