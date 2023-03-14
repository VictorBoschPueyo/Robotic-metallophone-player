import sys
import subprocess
import cv2
import time
import numpy as np

from rectangle import Rectangle
from note import Note
from best_fit import fit
from functions import locate_images, merge_recs

from random import randint


######################## Read templates ########################
path = "masks"
penta_files = [
    path + "/penta2.png",
    path + "/penta.png"]
sost_files = [
    path + "/sostingut-espai.png",
    path + "/sostingut-linia.png"]
bem_files = [
    path + "/bemoll-espai.png",
    path + "/bemoll-linia.png"]
negra_files = [
    path + "/negra.png",
    path + "/negra-gran.png"]
blanca_files = [
    path + "/blanca-espai.png",
    path + "/blanca-espai-gran.png",
    path + "/blanca-linia.png",
    path + "/blanca-linia-gran.png"]
rodona_files = [
    path + "/rodona-espai.png",
    path + "/rodona-espai-gran.png",
    path + "/rodona-linia.png",
    path + "/rodona-linia-gran.png"]

penta_imgs = [cv2.imread(f, 0) for f in penta_files]
sost_imgs = [cv2.imread(f, 0) for f in sost_files]
bem_imgs = [cv2.imread(f, 0) for f in bem_files]
negra_imgs = [cv2.imread(f, 0) for f in negra_files]
blanca_imgs = [cv2.imread(f, 0) for f in blanca_files]
rodona_imgs = [cv2.imread(f, 0) for f in rodona_files]


penta_lower, penta_upper, penta_thresh = 50, 150, 0.77
sost_lower, sost_upper, sost_thresh = 50, 150, 0.70
bem_lower, bem_upper, bem_thresh = 50, 150, 0.77
negra_lower, negra_upper, negra_thresh = 50, 150, 0.70
blanca_lower, blanca_upper, blanca_thresh = 50, 150, 0.70
rodona_lower, rodona_upper, rodona_thresh = 50, 150, 0.70
#################################################################


if __name__ == "__main__":
    img_file = "sheets/himne_alegria.png"
    img = cv2.imread(img_file, 0)

    # aqui ja arribara la imatge filtrada d'abans
    img_gray = img  # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
    ret, img_gray = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    ###

    img_width, img_height = img_gray.shape[::-1]

    # Analyse the pentagram
    print("Matching pentagram image...")
    penta_recs = locate_images(
        img_gray, penta_imgs, penta_lower, penta_upper, penta_thresh)

    print("Filtering weak pentagram matches...")
    penta_recs = [j for i in penta_recs for j in i]
    heights = [r.y for r in penta_recs] + [0]
    histo = [heights.count(i) for i in range(0, max(heights) + 1)]
    avg = np.mean(list(set(histo)))
    penta_recs = [r for r in penta_recs if histo[r.y] > avg]

    print("Merging pentagram image results...")
    penta_recs = merge_recs(penta_recs, 0.01)
    penta_recs_img = img.copy()
    for r in penta_recs:
        r.draw(penta_recs_img, (0, 0, 255), 2)

    cv2.imshow('pentagrama', penta_recs_img)
    cv2.waitKey(0)
    # cv2.imwrite('penta_recs_img.png', penta_recs_img)
