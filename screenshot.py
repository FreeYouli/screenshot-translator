# -*- coding: utf-8 -*-
from PIL import Image
import mss


def take_region_screenshot(region):
    x1, y1, x2, y2 = region
    monitor = {
        "left": int(x1),
        "top": int(y1),
        "width": int(x2 - x1),
        "height": int(y2 - y1),
    }
    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
