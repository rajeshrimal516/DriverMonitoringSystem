import cv2

from eyelongclosed_detector import EyeLongClosedDetector
from yawn_detector import YawnDetection
from head_pos_estimator import HeadPosition
from calculations import Calculations
import numpy as np
import time


class FaceDetection:
    """ This class is used to detect the face from the frame.
        The class consist of a member function detectFace.
    """

    def __init__(self):
        print('     [INFO] Face detection INIT done.')
        self.mar = 0
        self.adr = 0
        self.threshold = 0
        self.setup_time = 10
        self.idxEye = [[33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7], [
            362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]]

        self.idxMouth = [62, 183, 42, 41, 38, 12, 268, 271, 272,
                         407, 292, 325, 319, 403, 316, 15, 86, 179, 89, 96]
        self.idxFace = [151, 199, 137, 366]
        self.head_position = HeadPosition()
        self.yawn_detector = YawnDetection()
        self.eye_long_closed_detector = EyeLongClosedDetector()
        self.faceNotDetectedTime = 0

    def detectFace(self, img, results, frame_count, time_elapsed, fps):
        """ The function is used to detect the face.

            :param array img: 640x480 numpy array of pixel values.
            :param array results: Mesh of the face.
            :param int frame_count: Frame count
            :param float time_elapsed: Time elapsed counted from the start of the system.
            :param float fps: Frame per second.

            :returns: Nothing
        """
        height, width, _ = img.shape
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                text = ""
                landmarks = np.array([(lm.x, lm.y, lm.z)
                                     for lm in face_landmarks.landmark]).T
                eyes_left = (
                    (landmarks[0:2, self.idxEye[0]].T * np.array([width, height])[None, :]).astype(int)).tolist()
                eyes_right = (
                    (landmarks[0:2, self.idxEye[1]].T * np.array([width, height])[None, :]).astype(int)).tolist()
                mouth = ((landmarks[0:2, self.idxMouth].T *
                         np.array([width, height])[None, :]).astype(int)).tolist()
                face = ((landmarks[0:2, self.idxFace].T *
                        np.array([width, height])[None, :]).astype(int)).tolist()
                
                self.mar = Calculations.compute_mar(mouth)
                self.adr = Calculations.compute_adr(eyes_left, eyes_right)
                pitch, yaw, roll = self.head_position.calculate_euler_angles(
                    img.shape, landmarks)
                
                if time_elapsed < self.setup_time:
                    self.yawn_detector.setup_mar(self.mar)
                    self.eye_long_closed_detector.setup_adr(self.adr)
                    self.head_position.setup_yaw_pitch(pitch, yaw)
                    cv2.putText(img, "Setting Up!! Please Look Forward!!", (10, 90), cv2.FONT_HERSHEY_PLAIN, 1.5,
                                color=(0, 0, 255), thickness=2)

                else:
                    if fps != 0:
                        factor = 26
                        self.threshold = 1.9  # factor / fps
                    text = self.head_position.detect_headPos(img=img, pitch=pitch, yaw=yaw, roll=roll,
                                                             turn_time_threshold=self.threshold)
                    if text == "Normal Position":
                        self.yawn_detector.detect_yawn(img=img, mar=self.mar, frame_count=frame_count,
                                                       yawn_time_threshold=self.threshold, time_elapsed=time_elapsed)
                        self.eye_long_closed_detector.detect_blink(img=img, mean_eye_area_over_distance=self.adr,
                                                                   frame_count=frame_count,
                                                                   time_threshold=self.threshold)
                '''FACE Bounding Box'''
                x1, y1 = face[2][0], face[0][1]
                x2, y2 = face[3][0], face[1][1]
                h_mar, w_mar = 20, 10
                face_text = "Face Detected"
                cv2.rectangle(img, (x1 - w_mar, y1 - h_mar), (x2 + w_mar, y2 + h_mar), color=(255, 255, 255),
                              thickness=2)
                cv2.rectangle(img, (x1 - w_mar, y1 - h_mar - 20), (x1 - w_mar + 150, y1 - h_mar), color=(255, 255, 0),
                              thickness=-2)

                cv2.putText(img, text=face_text, org=(x1 - w_mar, y1 - h_mar - 5), fontScale=1,
                            fontFace=cv2.FONT_HERSHEY_PLAIN,
                            color=(0, 0, 255), thickness=2)
                """Face Bounding Box drawing complete"""

                '''HeadPosition Bounding Box'''
                cv2.rectangle(img, (x1 - w_mar + 10, y2 + h_mar), (x2 + w_mar, y2 + h_mar + 20), color=(255, 255, 0),
                              thickness=-2)
                cv2.putText(img, text=text, org=(x1 - w_mar + 10, y2 + h_mar + 15), fontScale=1,
                            fontFace=cv2.FONT_HERSHEY_PLAIN,
                            color=(0, 0, 255), thickness=2)

                """Face Bounding Box drawing complete"""
        else:
            cv2.putText(img=img, text="Face Not Detected", org=(10, 120), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,
                        color=(0, 0, 255), thickness=2)
