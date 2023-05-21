import cv2
import numpy as np
import glob

# Tamaño del tablero de ajedrez
chessboard_size = (7, 6)

# Tamaño de los cuadrados en el tablero (en mm)
square_size = 25.0

# Criterios de terminación
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Preparación de los puntos del objeto
objp = np.zeros((chessboard_size[1]*chessboard_size[0], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0],
                       0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# Arrays para guardar los puntos del objeto y los puntos de la imagen de todas las imágenes.
objpoints = []  # puntos 3d en el espacio del mundo real
imgpoints = []  # puntos 2d en el plano de la imagen.

images = glob.glob('utils/calibration/*.jpg')

for fname in images:
    print(fname)
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Encuentra las esquinas del tablero de ajedrez
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # Si se encuentran, agrega los puntos del objeto, los puntos de la imagen (después de refinarlos)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Dibuja y muestra las esquinas
        img = cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
cv2.destroyAllWindows()


# Calibración de la cámara
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

# Ahora puedes utilizar la matriz mtx y los coeficientes de distorsión para corregir la distorsión de las imágenes:

img = cv2.imread('utils/calibration/chess_9.jpg')
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
    mtx, dist, (w, h), 1, (w, h))

# Corrección de la distorsión
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# Recortar la imagen
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv2.imshow('calibresult.png', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('calibresult.png', dst)

# Guardar los parámetros de la cámara para su uso posterior
np.savez('utils/calibration/calib.npz', mtx=mtx,
         dist=dist, newcameramtx=newcameramtx, roi=roi)
