import cv2
import matplotlib.pyplot as plt
import numpy as np

def fit(img, templates, start_percent, stop_percent, threshold):
    '''
    This function searches the entire sheet the template. 
    In different iterations it looks for the template in diferent scales for more accuracy.
    '''
    
    best_location_count = -1
    best_locations = []
    best_scale = 1

    plt.axis([0, 2, 0, 1])
    plt.show(block=False)

    x = []
    y = []
    for scale in [i/100.0 for i in range(start_percent, stop_percent + 1, 3)]:
        locations = []
        location_count = 0
        for template in templates:
            # Resize the template to the scale
            template = cv2.resize(template, None,
                fx = scale, fy = scale, interpolation = cv2.INTER_CUBIC)
            # Matching in the whole sheet
            result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            # Saves the matches that have a greater percentage fit than the threshold
            result = np.where(result >= threshold)
            location_count += len(result[0])
            locations += [result]
            
        print("scale: {0}, hits: {1}".format(scale, location_count))
        x.append(location_count)
        y.append(scale)
        plt.plot(y, x)
        plt.pause(0.00001)

        if (location_count > best_location_count):
            best_location_count = location_count
            best_locations = locations
            best_scale = scale
            plt.axis([0, 2, 0, best_location_count])
        elif (location_count < best_location_count):
            pass
    plt.close()

    return best_locations, best_scale