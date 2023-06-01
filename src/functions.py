import cv2
import sys
import os
import time

from src.rectangle import Rectangle
from src.best_fit import fit


def locate_images(img, templates, start, stop, threshold, display=False):
    # Creates a Rectangle for each match found with the function fit()
    
    locations, scale = fit(img, templates, start, stop, threshold, display)
    img_locations = []
    for i in range(len(templates)):
        w, h = templates[i].shape[::-1]
        w *= scale
        h *= scale
        img_locations.append([Rectangle(pt[0], pt[1], w, h)
                             for pt in zip(*locations[i][::-1])])
    return img_locations


def merge_recs(recs, threshold):
    # Merge rectangles to find pentagrams in the picture

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


def detect(img, img_gray, figure_name, figure_imgs, lower, upper, thresh, display=False):
    # Locate the figures in the image
    recs = locate_images(img_gray, figure_imgs, lower, upper, thresh, display)

    recs = merge_recs([j for i in recs for j in i], 0.5)

    # Draw every rectangle in the image
    if display:
        recs_img = img.copy()
        for r in recs:
            r.draw(recs_img, (0, 0, 255), 2)
        cv2.imwrite(figure_name + '_recs_img.png', recs_img)

    return recs

def load_animation(t):
  
    # String to be displayed when the application is loading
    load_str = "tocant la partitura..."
    ls_len = len(load_str)
  
    # String for creating the rotating line
    animation = "|/-\\"
    anicount = 0
      
    # used to keep the track of the duration of animation
    counttime = 0        
      
    # pointer for travelling the loading string
    i = 0                     
  
    while (counttime != t):   
        # used to change the animation speed smaller the value, faster will be the animation
        time.sleep(0.075) 
                              
        # converting the string to list as string is immutable
        load_str_list = list(load_str) 
          
        # x->obtaining the ASCII code
        x = ord(load_str_list[i])
          
        # y->for storing altered ASCII code
        y = 0                             
  
        # if the character is "." or " ", keep it unaltered switch uppercase to lowercase and vice-versa 
        if x != 32 and x != 46:             
            if x>90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i]= chr(y)
          
        # for storing the resultant string
        res =''             
        for j in range(ls_len):
            res = res + load_str_list[j]
              
        # displaying the resultant string
        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()
  
        # Assigning loading string to the resultant string
        load_str = res
  
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len
        counttime = counttime + 1
      