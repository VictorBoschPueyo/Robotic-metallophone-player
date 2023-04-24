import cv2
import numpy as np


def straighten_sheet(img_path):
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)
    img_gray = cv2.Canny(img_gray, 75, 200)

    contours, _ = cv2.findContours(
        img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    sheet_contour = contours[0]

    peri = cv2.arcLength(sheet_contour, True)
    approx = cv2.approxPolyDP(sheet_contour, 0.02 * peri, True)

    src = np.float32([approx[0], approx[1], approx[2], approx[3]])
    dst = np.float32([[0, 0], [0, 750], [500, 750], [500, 0]])

    M = cv2.getPerspectiveTransform(src, dst)
    img = cv2.warpPerspective(img, M, (500, 750))

    cv2.imshow("Sheet", img)
    cv2.waitKey(0)


straighten_sheet('sheets/sheet10.jpg')

"""img = cv2.imread('sheet10.jpg')


print(img.shape)

src = np.array([[183, 45],   [763, 44],   [1282, 65],
                [131, 829],  [751, 833],  [1331, 817],
                [125, 1659], [741, 1677], [1339, 1661]], dtype=np.float32)


dst = np.array([[0, 0],               [img.shape[1]/2, 0],              [img.shape[1], 0],
                [0, img.shape[0]/2],  [img.shape[1]/2,
                                       img.shape[0]/2], [img.shape[1], img.shape[0]/2],
                [0, img.shape[0]],    [img.shape[1]/2, img.shape[0]],   [img.shape[1], img.shape[0]]], dtype=np.float32)

M, _ = cv2.findHomography(src, dst)

rectangular_sheet = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))

cv2.imwrite('sheet10_fixed.jpg', rectangular_sheet)
cv2.waitKey(0)"""
