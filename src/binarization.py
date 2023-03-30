import cv2
import numpy as np


def order_points(pts):
    # initialzie a list of coordinates that will be ordered such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points in the top-left, top-right, bottom-right, and bottom-left order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


def detect_corners(img):
    img_red = img[:, :, 2]
    _, img_mask = cv2.threshold(img_red, 130, 255, cv2.THRESH_BINARY)

    cv2.imshow('red', img_mask)
    cv2.waitKey(0)

    kernel = np.ones((5, 5), np.uint8)
    kernel_x = np.ones((11, 5), np.uint8)
    kernel_y = np.ones((5, 11), np.uint8)
    kernel_big = np.ones((15, 15), np.uint8)

    img_erosion = cv2.erode(img_mask, kernel, iterations=1)
    img_dil_x = cv2.dilate(img_erosion, kernel_x, iterations=2)
    img_dil_y = cv2.dilate(img_dil_x, kernel_y, iterations=2)
    img_final = cv2.dilate(img_dil_y, kernel_big, iterations=2)

    cv2.imshow('erosion', img_final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    corners = cv2.goodFeaturesToTrack(img_final, 4, 0.01, 10)

    # Convert the corners to integers
    corners = np.intp(corners)

    # Draw the corners on the image
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

    # Display the image
    cv2.imshow('Corners', img_final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return corners


def undisort_img(img):
    # detect corners
    pts = 0

    # Transformation
    img_transformed = four_point_transform(img, pts)

    return img_transformed


# def binarize(img_path):
img_path = "sheets/fons_vermell1.jpg"
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

img_red = cv2.imread(img_path)
img_red = cv2.resize(img_red, dim, interpolation=cv2.INTER_AREA)
a = detect_corners(img_red)
