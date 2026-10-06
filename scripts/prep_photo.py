"""Prep photo (background already removed, e.g. via macOS Preview): CLAHE contrast -> composite on white.
Usage: python scripts/prep_photo.py source-photo.png"""
import sys
import numpy as np
import cv2
from PIL import Image

src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.png"
arr = np.array(Image.open(src).convert("RGBA"))
alpha = arr[..., 3].astype(np.float32) / 255.0
gray = cv2.cvtColor(arr[..., :3], cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
out = (gray * alpha + 255 * (1 - alpha)).astype(np.uint8)
Image.fromarray(out, "L").save("source-prepped.png")
print("saved source-prepped.png")
