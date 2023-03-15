import cv2

from rectangle import Rectangle
from best_fit import fit


def locate_images(img, templates, start, stop, threshold):
    '''
    Creates a Rectangle for each match found with the function fit()
    '''
    locations, scale = fit(img, templates, start, stop, threshold)
    img_locations = []
    for i in range(len(templates)):
        w, h = templates[i].shape[::-1]
        w *= scale
        h *= scale
        img_locations.append([Rectangle(pt[0], pt[1], w, h)
                             for pt in zip(*locations[i][::-1])])
    return img_locations


def merge_recs(recs, threshold):
    '''
    Merge rectangles to find pentagrams in the picture
    '''
    filtered_recs = []
    while len(recs) > 0:
        r = recs.pop(0)
        recs.sort(key=lambda rec: rec.distance(r))
        merged = True
        while (merged):
            merged = False
            i = 0
            for _ in range(len(recs)):
                if r.overlap(recs[i]) > threshold or recs[i].overlap(r) > threshold:
                    r = r.merge(recs.pop(i))
                    merged = True
                elif recs[i].distance(r) > r.w/2 + recs[i].w/2:
                    break
                else:
                    i += 1
        filtered_recs.append(r)
    return filtered_recs


def detect(img, img_gray, figure_name, figure_imgs, lower, upper, thresh):
    print("Matching " + figure_name + " image...")
    # Locate the figures in the image
    recs = locate_images(img_gray, figure_imgs, lower, upper, thresh)

    print("Merging " + figure_name + " image results...")
    recs = merge_recs([j for i in recs for j in i], 0.5)

    # Draw every rectangle in the image
    recs_img = img.copy()
    for r in recs:
        r.draw(recs_img, (0, 0, 255), 2)
    cv2.imwrite(figure_name + '_recs_img.png', recs_img)

    return recs
