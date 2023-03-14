import sys
import subprocess
import cv2
import time
import numpy as np
from best_fit import fit
from rectangle import Rectangle
from note import Note
from random import randint

# Read templates
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
