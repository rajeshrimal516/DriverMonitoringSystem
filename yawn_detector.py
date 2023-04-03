import time
import cv2
import os

from playsound import playsound
from threading import Thread

def playy():
    print("beep")
    playsound('beep.mp3', block=False)

class YawnDetection:
    def __init__(self):
        self._frame_count = 0
        self._mouth_mar_threshold = 1
        self._mouth_min_thresh = 150

        self._mouth_mar_setup = []
        self._mouth_open_consec_frames = 60

        self._mouth_open_count_time = 0
        self._yawn_total = 0

        self._min_mar = 150
        self._max_mar = 0

        self._alert_message = ""
        self._yawn_alarm = False
        self._yawn_time = 0
        self._start_frame = 0
        self._end_frame = 0
        self._mouth_mar_setup_time = 0
        self._is_mar_setup_done = True
        self._yawning = 0
        self.yawnDecrease = False
        #         self.LedPin = 11
        #         GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        #         GPIO.setup(self.LedPin, GPIO.OUT)   # Set LedPin's mode is output
        #         GPIO.output(self.LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

        print('     [INFO] Yawn Detector INIT done')

    def setup_mar(self, mar):
        self._mouth_mar_setup.append(mar)

    def detect_yawn(self, img, mar, frame_count, yawn_time_threshold,time_elapsed):
        T = Thread(target=playy)
        if self._is_mar_setup_done is True:
            self._mouth_mar_setup.sort(reverse=False)
            if min(list(filter(lambda num: num != 0, self._mouth_mar_setup))) < 4.5:
                self._mouth_mar_threshold = 4.5 * 4
            else:
                self._mouth_mar_threshold = min(list(filter(lambda num: num != 0, self._mouth_mar_setup))) * 4
            print("Yawn check Threshold: (> Threshold is Yawn): ", self._mouth_mar_threshold)
            self._is_mar_setup_done = False
        else:

            if mar > self._mouth_mar_threshold:
                if self._mouth_open_count_time == 0:
                    self._mouth_open_count_time = time.time()
                    self._start_frame = frame_count
                else:
                    end_time = time.time()
                    self._yawn_time = end_time - self._mouth_open_count_time
                    cv2.putText(img, "Mouth Open time.: {:.2f} sec".format(self._yawn_time), (10, 360),
                                cv2.FONT_HERSHEY_PLAIN, 1.5,
                                (106, 13, 106), 2)
                    if self._yawn_time > yawn_time_threshold:
                        self._yawn_alarm = True
                        cv2.putText(img, "Warning, Yawning From: {}th frame".format(self._start_frame), (10, 390),
                                    cv2.FONT_HERSHEY_PLAIN, 1.5,
                                    (0, 0, 255), 2)
                        print(frame_count, "Yawning ", self._start_frame)
                    if self._yawning == 0:
                        self._yawning = time.time()
                    else:
                        end_time = time.time()

            else:

                if self._yawn_alarm is True:
                    self._yawn_total += 1
                self._yawn_alarm = False
                self._mouth_open_count_time = 0
                self._yawn_time = 0
        if self._yawn_total > 5:
            T.start()
            cv2.putText(img, "Press Enter to stop beep!!!!!", (10, 450), cv2.FONT_HERSHEY_PLAIN, 1.5,
                        (0, 0, 255), 2)
            if cv2.waitKey(33) == ord('\r'):
                self._yawn_total -= 1
        if int(time_elapsed) % 60 == 0 and self.yawnDecrease is False:
            self._yawn_total -= 1
            self.yawnDecrease = True
            if self._yawn_total < 0:
                self._yawn_total = 0

        cv2.putText(img, "Thresh MAR: {:.2f}".format(self._mouth_mar_threshold), (10, 300), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    (106, 13, 106), 2)
        cv2.putText(img, "MAR.: {:.2f}".format(mar), (10, 330), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    (106, 13, 106), 2)
        cv2.putText(img, "Yawn Count: {}".format(self._yawn_total), (400, 90), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    (255, 0, 0), 2)
