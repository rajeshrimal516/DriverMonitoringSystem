from scipy.spatial import distance as dist
import math
import numpy as np
import cv2

""""
    *** compute_mar ***
    
    Takes mouth landmark coordinates (Total 20 points). Only 6 are used.
    Calculates the Mouth Aspect Ratio (MAR) based on the coordinates of the 6 landmarks of the Mouth
    returns calculated MAR value
    
          
              (p4)            (p6)
                *              *
                |              |
    (p0) *------|--------------|----* (p10)
                |              |
                *              *
              (p16)            (p14)
              
                     Mouth
                
    mar =  |(p1-p3)| + |(p2-p4)|
         -------------------------
                 2|(p5-p6)|
    
    *** compute_adr ***
    
    Takes eyes landmark coordinates (16 points) (left and right)
    calculates the areas of the eyes (based on the closed contour of 16 points) 
    and distance between the center of the two eyes.
    
    Calculate the Area over Distance Ratio (ADR) value as 
                     ____________________________________
        ADR =       / Mean area of Eyes (Left and Right)
                \  / --------------------------------------
                 \/        Distance between the Eyes
         
    """


class Calculations:
    @staticmethod
    def compute_mar(mouth):
        a = abs(dist.euclidean(mouth[4], mouth[16]))
        b = abs(dist.euclidean(mouth[6], mouth[14]))
        c = abs(dist.euclidean(mouth[0], mouth[10]))
        return ((a + b) / (2.0 * c)) * 100

    @staticmethod
    def compute_adr(left_eye, right_eye):
        def eye_center(eye):
            x_mid = int((eye[0][0] + eye[8][0]) / 2)
            y_mid = int((eye[4][1] + eye[12][1]) / 2)
            return x_mid, y_mid

        left_eye_area = cv2.contourArea(np.array(left_eye))
        right_eye_area = cv2.contourArea(np.array(right_eye))
        left_eye_center = eye_center(left_eye)
        right_eye_center = eye_center(right_eye)
        eyeDistance = dist.euclidean(left_eye_center, right_eye_center)
        eye_avg_area = (left_eye_area + right_eye_area) / 2
        return math.sqrt(eye_avg_area) / eyeDistance
