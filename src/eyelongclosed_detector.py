import time
import cv2
import os

from threading import Thread
from src.common import playy


class EyeLongClosedDetector:
    """ This class is used to detect the eye state from the frame.
        The class consist of a member function setup_adr and detect_blink.
    """

    def __init__(self):
        self._eye_long_closed = False
        self._eye_area_over_distance_thresh = 1
        self._eye_area_over_distance_setup = []
        self._blink_total = 0
        self._eye_long_close_start_time = 0
        self._long_closed_count = 0
        self._is_threshold_set = True
        self._start_frame = 0
        self._isBlinked = False

        print('     [INFO] blink Detector INIT done')

    def setup_adr(self, mean_eye_area_over_distance):
        """The function records the values of ADR during the setup period that 
        will be used to calculate the threshold ADR.

        :param float adr: Area over distance ratio (ADR).

        :returns: Nothing.

        """
        self._eye_area_over_distance_setup.append(mean_eye_area_over_distance)

    def detect_blink(self, img, mean_eye_area_over_distance, frame_count, time_threshold):
        """The function is used to detect the eye state.

        :param array img: 640x480 numpy array of pixel values.
        :param float adr: Area over distance ratio (ADR).
        :param int frame_count: Current frame count.
        :param float time_threshold: Time threshold after which the alarm will be raised.

        :returns: Nothing.

        """
        color = (79, 52, 32)
        T = Thread(target=playy)

        if self._is_threshold_set is True:
            self._eye_area_over_distance_setup.sort(reverse=True)
            upperlimit = int(0.15 * len(self._eye_area_over_distance_setup))
            self._eye_area_over_distance_thresh = \
                sum(self._eye_area_over_distance_setup[:upperlimit]) / len(
                    self._eye_area_over_distance_setup[:upperlimit])
            self._eye_area_over_distance_thresh = \
                self._eye_area_over_distance_thresh * 0.90
            self._is_threshold_set = False
            print("Eye Closed check Threshold: (< Threshold is Closed): ",
                  self._eye_area_over_distance_thresh)
            del self._eye_area_over_distance_setup
            del upperlimit
        else:
            mean_eye_area_over_distance = round(mean_eye_area_over_distance, 3)
            if mean_eye_area_over_distance < self._eye_area_over_distance_thresh:

                if self._eye_long_close_start_time == 0:
                    self._eye_long_close_start_time = time.time()
                    self._start_frame = frame_count
                else:
                    close_time = time.time() - self._eye_long_close_start_time
                    cv2.putText(img, "Eye Close Time: {:.2f} secs".format(close_time), (10, 240),
                                cv2.FONT_HERSHEY_PLAIN, 1.5,
                                color, 2)
                    if close_time > time_threshold:
                        T.start()
                        cv2.putText(img, "Warning, Closed from {:.2f} frame".format(self._start_frame), (10, 270),
                                    cv2.FONT_HERSHEY_PLAIN, 1.5,
                                    (0, 0, 255), 2)
                        self._eye_long_closed = True

            else:
                if self._isBlinked is True:
                    self._blink_total += 1
                if self._eye_long_closed is True:
                    self._long_closed_count += 1

                self._eye_long_close_start_time = 0
                self._eye_long_closed = False
                self._isBlinked = False

        cv2.putText(img, "Thresh ADR: {:.2f}".format(self._eye_area_over_distance_thresh), (10, 180),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, color, 2)

        cv2.putText(img, "ADR: {:.2f}".format(mean_eye_area_over_distance), (10, 210), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    color, 2)
        cv2.putText(img, "Eye L. Close : {}".format(self._long_closed_count), (400, 120), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    color, 2)
