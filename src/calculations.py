from scipy.spatial import distance as dist
import math
import numpy as np
import cv2

class Calculations:
    """This Class will be used to compute the ADR and MAR.

        The class consist of 2 member functions.
    """
    @staticmethod
    def compute_mar(mouth):
        """This method will be used to compute the MAR.

            :param list mouth: Mouth landmark coordinates.

            :returns: Computed MAR value.

            :rtype: float
        """
        a = abs(dist.euclidean(mouth[4], mouth[16]))
        b = abs(dist.euclidean(mouth[6], mouth[14]))
        c = abs(dist.euclidean(mouth[0], mouth[10]))
        return ((a + b) / (2.0 * c)) * 100

    @staticmethod
    def compute_adr(left_eye, right_eye):
        """This method will be used to compute the ADR.

            :param list left_eye: Left eye landmark coordinates.
            :param list right_eye: Right eye landmark coordinates.

            :returns: Computed ADR value.

            :rtype: float
        """
        def eye_center(eye):
            """This method will be used to compute the ADR.

                :param list eye: Eye landmark coordinates.

                :returns: Computed eye center.

                :rtype: float
            """
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
