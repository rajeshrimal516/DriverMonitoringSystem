import time
import cv2
import os

from threading import Thread
from playsound import playsound

def playy():
    print("beep")
    playsound('beep.mp3',block=False)


class EyeLongClosedDetector:
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

    """
        Appends the Mean Eye Area over Distance Ratio (ADR) for 5 seconds.
        After 5 seconds is reached, it calculates the threshold based on the observed ADR values of the eyes
        when the eyes are open.
        Here, 
            Largest 10 ADR values are used to calculate the threshold. These largest ADR values corresponds
             to the open eye ADR value.
            Threshold is calculated as: Average of 10 Maximum ADR - 0.78 % of Average of 10 Maximum ADR
    """

    def setup_adr(self, mean_eye_area_over_distance):
        self._eye_area_over_distance_setup.append(mean_eye_area_over_distance)

    def detect_blink(self, img, mean_eye_area_over_distance, frame_count, time_threshold):
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
            print("Eye Closed check Threshold: (< Threshold is Closed): ", self._eye_area_over_distance_thresh)
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
                    # if close_time > 0.01:
                    #     self._isBlinked = True
                    if close_time > time_threshold:
                        T.start()
                        cv2.putText(img, "Warning, Closed from {:.2f} frame".format(self._start_frame), (10, 270),
                                    cv2.FONT_HERSHEY_PLAIN, 1.5,
                                    (0, 0, 255), 2)
                        self._eye_long_closed = True
                        T.join()

                        # playy()


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
        # cv2.putText(img, "Eye Blink : {}".format(self._blink_total), (400, 150), cv2.FONT_HERSHEY_PLAIN, 1.5,
        #             color, 2)
