import cv2
import numpy as np

# def binarize(img_path):
img_path = "sheets/sheet10_fixed.jpg"
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Resize image
scale_percent = 40
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

# Thresholing with gaussian
img_th = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 5)

cv2.imshow('image', img_th)
cv2.waitKey(0)

