import cv2
import numpy as np

# Load reference points in a numpy array
reference_points = np.loadtxt(
    'points_reference.txt', delimiter=',', dtype=np.int32)

# Load points from the image in a numpy array
image_points = np.loadtxt('points_photo_reference.txt',
                          delimiter=',', dtype=np.int32)

# Load the image
img = cv2.imread('sheets/partiture.jpg')
ref_image = cv2.imread('sheets/points_template.png')

# Find the homography matrix
M, _ = cv2.findHomography(image_points, reference_points)

# Warp the image
partiture_std = cv2.warpPerspective(
    img, M, (ref_image.shape[1], 2*ref_image.shape[0]//3))

cv2.imwrite('sheets/partiture_fixed.jpg', partiture_std)
cv2.waitKey(0)
