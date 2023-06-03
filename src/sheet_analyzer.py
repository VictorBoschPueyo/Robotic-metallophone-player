import cv2
import numpy as np
from random import randint
import glob

from src.rectangle import Rectangle
from src.note import Note
from src.partiture import Partiture
from src.functions import locate_images, merge_recs, detect



######################## Read templates ########################
path = "utils/masks"

penta_files = glob.glob(path + "/penta/*.png")
sost_files = glob.glob(path + "/sostingut/*.png")
bem_files = glob.glob(path + "/bemoll/*.png")
negra_files = glob.glob(path + "/negra/*.png")
blanca_files = glob.glob(path + "/blanca/*.png")
rodona_files = glob.glob(path + "/rodona/*.png")

penta_imgs = [cv2.imread(f, 0) for f in penta_files]
sost_imgs = [cv2.imread(f, 0) for f in sost_files]
bem_imgs = [cv2.imread(f, 0) for f in bem_files]
negra_imgs = [cv2.imread(f, 0) for f in negra_files]
blanca_imgs = [cv2.imread(f, 0) for f in blanca_files]
rodona_imgs = [cv2.imread(f, 0) for f in rodona_files]


penta_lower, penta_upper, penta_thresh = 50, 150, 0.77
sost_lower, sost_upper, sost_thresh = 50, 150, 0.70
bem_lower, bem_upper, bem_thresh = 50, 150, 0.77
negra_lower, negra_upper, negra_thresh = 50, 150, 0.73
blanca_lower, blanca_upper, blanca_thresh = 50, 150, 0.68
rodona_lower, rodona_upper, rodona_thresh = 50, 150, 0.70
#################################################################

identi = 'identi_alegria.png'

def detect_parallel(args):
    img, img_gray, label, imgs, lower, upper, thresh, display = args
    return detect(img, img_gray, label, imgs, lower, upper, thresh, display)


def analyze_sheet(img_gray, img, display=False, paralelize=False):

    img_width, _ = img_gray.shape[::-1]

    # Analyse the pentagram
    print("Analysing pentagram...")
    recs_penta = locate_images(
        img_gray, penta_imgs, penta_lower, penta_upper, penta_thresh, display)

    # Filtering weak pentagram matches
    recs_penta = [j for i in recs_penta for j in i]
    heights = [r.y for r in recs_penta] + [0]
    histo = [heights.count(i) for i in range(0, max(heights) + 1)]
    avg = np.mean(list(set(histo)))
    recs_penta = [r for r in recs_penta if histo[r.y] > avg]

    # Merging pentagram image results
    recs_penta = merge_recs(recs_penta, 0.01)
    penta_recs_img = img.copy()
    for r in recs_penta:
        r.draw(penta_recs_img, (0, 0, 255), 2)

    if display:
        cv2.imwrite('penta_recs_img.png', penta_recs_img)

    # Discovering staff locations
    penta_boxes = merge_recs([Rectangle(0, r.y, img_width, r.h)
                             for r in recs_penta], 0.01)
    penta_boxes_img = img.copy()
    for r in penta_boxes:
        r.draw(penta_boxes_img, (0, 0, 255), 2)

    if display:
        cv2.imwrite('penta_boxes_img.png', penta_boxes_img)

    # Detection with every template
    print("Analysing notes and figures...")
    if paralelize:
        from multiprocessing import Pool
        detections = [
            (img, img_gray, "sost", sost_imgs, sost_lower, sost_upper, sost_thresh, False),
            (img, img_gray, "bem", bem_imgs, bem_lower, bem_upper, bem_thresh, False),
            (img, img_gray, "negra", negra_imgs, negra_lower, negra_upper, negra_thresh, False),
            (img, img_gray, "blanca", blanca_imgs, blanca_lower, blanca_upper, blanca_thresh, False),
            (img, img_gray, "rodona", rodona_imgs, rodona_lower, rodona_upper, rodona_thresh, False)
        ]

        # Create a pool of workers
        pool = Pool()

        # Execute the detect function calls in parallel
        results = pool.map(detect_parallel, detections)

        # Close the pool and wait for the processes to finish
        pool.close()
        pool.join()

        # Retrieve the results
        recs_sost, recs_bem, recs_negra, recs_blanca, recs_rodona = results
    else:
        recs_sost = detect(img, img_gray, "sost", sost_imgs,
                        sost_lower, sost_upper, sost_thresh, display)
        recs_bem = detect(img, img_gray, "bem", bem_imgs,
                        bem_lower, bem_upper, bem_thresh, display)
        recs_negra = detect(img, img_gray, "negra", negra_imgs,
                            negra_lower, negra_upper, negra_thresh, display)
        recs_blanca = detect(img, img_gray, "blanca", blanca_imgs,
                            blanca_lower, blanca_upper, blanca_thresh, display)
        recs_rodona = detect(img, img_gray, "rodona", rodona_imgs,
                            rodona_lower, rodona_upper, rodona_thresh, display)
    

    # Create all notes and ordenate them
    note_groups = []
    for box in penta_boxes:
        # For every pentagram, creates a note with all the information in it
        penta_sost = [Note(r, "sharp", box)
                      for r in recs_sost if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        penta_bem = [Note(r, "flat", box)
                     for r in recs_bem if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        notes_negres = [Note(r, "negra", box, penta_sost, penta_bem)
                        for r in recs_negra if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        notes_blanques = [Note(r, "blanca", box, penta_sost, penta_bem)
                          for r in recs_blanca if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        notes_rodones = [Note(r, "rodona", box, penta_sost, penta_bem)
                         for r in recs_rodona if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]

        # Join all types of notes in a single group
        penta_notes = notes_negres + notes_blanques + notes_rodones

        # Sort the notes in time order
        penta_notes.sort(key=lambda n: n.rec.x)
        pentagrames = [r for r in recs_penta if r.overlap(box) > 0]
        pentagrames.sort(key=lambda r: r.x)
        note_color = (randint(0, 255), randint(0, 255), randint(0, 255))

        note_group = []
        i = 0
        j = 0
        while (i < len(penta_notes)):
            if (j < len(pentagrames) and penta_notes[i].rec.x > pentagrames[j].x):
                r = pentagrames[j]
                j += 1
                if len(note_group) > 0:
                    note_groups.append(note_group)
                    note_group = []
                note_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            else:
                note_group.append(penta_notes[i])
                penta_notes[i].rec.draw(img, note_color, 2)
                i += 1
        note_groups.append(note_group)

    if not display:
        for r in penta_boxes:
            r.draw(img, (0, 0, 255), 2)
        for r in recs_sost:
            r.draw(img, (0, 0, 255), 2)
        for r in recs_bem:
            r.draw(img, (0, 0, 255), 2)

        cv2.imwrite(identi, img)


    return Partiture(note_groups)
