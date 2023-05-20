import cv2
import numpy as np

# Load reference points in a numpy array
reference_points = np.loadtxt(
    'sheets/points_himne_alegria_full.txt', delimiter=',', dtype=np.int32)

# Load points from the image in a numpy array
image_points = np.loadtxt('sheets/points_foto_himne_alegria.txt',
                          delimiter=',', dtype=np.int32)

# Load the image
img = cv2.imread('sheets/foto_himne_alegria.jpg')
ref = cv2.imread('sheets/himne_alegria_full.png')

# Find the homography matrix
M, _ = cv2.findHomography(image_points, reference_points)

# Warp the image
partiture_std = cv2.warpPerspective(
    img, M, (ref.shape[1], ref.shape[0]))

cv2.imwrite('sheets/himne_alegria_fixed.jpg', partiture_std)
cv2.waitKey(0)
