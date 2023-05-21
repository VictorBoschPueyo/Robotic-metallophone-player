import cv2
import numpy as np


def undisort_img(img):
    # Load previously saved data from npz file
    with np.load('utils/calibration/calib.npz') as X:
        mtx, dist, newcameramtx, roi = [X[i]
                                        for i in ('mtx', 'dist', 'newcameramtx', 'roi')]

    # Apply the undistortion to the music sheet
    h, w = img.shape[:2]
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # Cut the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    return dst


def wrap_img(img):
    ref_img = cv2.imread("sheets/himne_alegria_full.png")

    # Get the images sizes
    h, w = img.shape[:2]
    h_ref, w_ref = ref_img.shape[:2]

    # Define the corners of the source image
    src = np.float32([[133, 126], [1823, 151], [25, 1458], [1953, 1458]])

    # Define the corners of the destination image
    dst = np.float32(
        [[0, 0], [w_ref, 0], [0, int(h_ref/2)], [w_ref, int(h_ref/2)]])

    # Get the transformation matrix
    M = cv2.getPerspectiveTransform(src, dst)

    # Apply the transformation
    dst = cv2.warpPerspective(img, M, (w_ref, int(h_ref/2)))

    return dst


def binarize_img(img):
    # Convert to grayscale
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    binarized = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 5)

    # Remove noise (solitary pixels)
    kernel_h = np.ones((2, 1), np.uint8)
    binarized = cv2.dilate(binarized, kernel_h, iterations=1)

    kernel_v = np.ones((1, 2), np.uint8)
    binarized = cv2.dilate(binarized, kernel_v, iterations=1)
    '''
    binarized = cv2.erode(binarized, kernel_h, iterations=1)
    binarized = cv2.erode(binarized, kernel_v, iterations=1)'''

    # Return the binarized image
    return binarized


img = cv2.imread("sheets/foto_himne_alegria.jpg")

# Undisort the image
img = undisort_img(img)

# Wrap the image
img = wrap_img(img)

# Binarize the image
img = binarize_img(img)

# Save the image
cv2.imwrite("sheets/himne_alegria_bin.png", img)
