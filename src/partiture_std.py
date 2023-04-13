import cv2
import numpy as np

img = cv2.imread('sheet10.jpg')


print(img.shape)

src = np.array([[183, 45],   [763, 44],   [1282, 65], 
                [131, 829],  [751, 833],  [1331, 817],
                [125, 1659], [741, 1677], [1339, 1661] ], dtype=np.float32)


dst = np.array([[0, 0],               [img.shape[1]/2, 0],              [img.shape[1], 0],
                [0, img.shape[0]/2],  [img.shape[1]/2, img.shape[0]/2], [img.shape[1], img.shape[0]/2], 
                [0, img.shape[0]],    [img.shape[1]/2, img.shape[0]],   [img.shape[1], img.shape[0]]], dtype=np.float32)

M, _ = cv2.findHomography(src, dst)

rectangular_sheet = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))

cv2.imwrite('sheet10_fixed.jpg', rectangular_sheet)
cv2.waitKey(0)