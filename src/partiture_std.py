import cv2
import numpy as np


def undisort_img(img):
    # Load previously saved data from npz file
    with np.load('utils/calibration/calib.npz') as X:
        mtx, dist, newcameramtx, roi = [X[i]
                                        for i in ('mtx', 'dist', 'newcameramtx', 'roi')]
        
    print("Camera matrix: ", mtx)
    print("Distortion coefficients: ", dist)
    print("New camera matrix: ", newcameramtx)
    print("Region of interest: ", roi)

    # Apply the undistortion to the music sheet
    h, w = img.shape[:2]
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # Cut the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    return dst


def wrap_img(img):
    # Get ref points
    h_ref, w_ref = 1571, 1165

    # Define the corners of the source image
    src = np.float32([[124, 121], [1850, 129], [37, 1425], [1973, 1425]])

    # Define the corners of the destination image
    dst = np.float32(
        [[0, 0], [h_ref, 0], [0, w_ref], [h_ref, w_ref]])

    # Get the transformation matrix
    M = cv2.getPerspectiveTransform(src, dst)

    # Apply the transformation
    dst = cv2.warpPerspective(img, M, (h_ref, w_ref))

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

    # Return the binarized image
    return binarized


def partiure_std(img):
    # Undisort the image
    img = undisort_img(img)

    # Wrap the image
    img = wrap_img(img)

    # Binarize the image
    img = binarize_img(img)

    return img
