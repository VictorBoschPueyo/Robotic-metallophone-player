import cv2
import math


class Rectangle(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.middle = self.x + self.w/2, self.y + self.h/2
        self.area = self.w * self.h

    def overlap(self, other):
        '''
        Calculates the area that overlapes between 2 rectangles
        '''
        overlap_x = max(0, min(self.x + self.w, other.x +
                        other.w) - max(self.x, other.x))
        overlap_y = max(0, min(self.y + self.h, other.y +
                        other.h) - max(self.y, other.y))
        overlap_area = overlap_x * overlap_y
        return overlap_area / self.area

    def distance(self, other):
        '''
        Calculates the distance between the center of 2 rectangles
        '''
        dx = self.middle[0] - other.middle[0]
        dy = self.middle[1] - other.middle[1]
        return math.sqrt(dx*dx + dy*dy)

    def merge(self, other):
        '''
        Takes 2 rectangles and merges them into one
        '''
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        w = max(self.x + self.w, other.x + other.w) - x
        h = max(self.y + self.h, other.y + other.h) - y
        return Rectangle(x, y, w, h)

    def draw(self, img, color, thickness):
        '''
        Draw the rectangle in the image
        '''
        pos = ((int)(self.x), (int)(self.y))
        size = ((int)(self.x + self.w), (int)(self.y + self.h))
        cv2.rectangle(img, pos, size, color, thickness)
