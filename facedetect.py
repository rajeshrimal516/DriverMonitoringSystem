import cv2

from calculations import Calculations
from eyelongclosed_detector import EyeLongClosedDetector
from yawn_detector import YawnDetection
from head_pos_estimator import HeadPosition
import numpy as np
import time


def crop(image, points):
    x1, y1 = np.amin(points, axis=0)
    x2, y2 = np.amax(points, axis=0)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    w = (x2 - x1) * 1.2
    h = w * 1
    margin_x, margin_y = w / 2, h / 2
    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)
    rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)
    image = image[rect[1]:rect[3], rect[0]:rect[2]]
    image = cv2.resize(image, (image.shape[1] * 5, image.shape[0] * 5))
    return image, rect


class FaceDetection:
    def __init__(self):
        print('     [INFO] Face detection INIT done.')
        self.mar = 0
        self.adr = 0
        self.threshold = 0
        self.setup_time = 10
        self.idxLeftEye = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
        self.idxRightEye = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
        self.idxMouth = [62, 183, 42, 41, 38, 12, 268, 271, 272, 407, 292, 325, 319, 403, 316, 15, 86, 179, 89, 96]
        self.idxFace = [151, 199, 137, 366]
        self.yawn_detector = YawnDetection()
        self.head_position = HeadPosition()
        self.eye_long_closed_detector = EyeLongClosedDetector()
        self.faceNotDetectedTime = 0

    def detectFace(self, img, results, frame_count, time_elapsed, fps):
        height, width, _ = img.shape
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                text = ""
                landmarks = np.array([(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark]).T
                eyes_left = (
                    (landmarks[0:2, self.idxLeftEye].T * np.array([width, height])[None, :]).astype(int)).tolist()
                eyes_right = (
                    (landmarks[0:2, self.idxRightEye].T * np.array([width, height])[None, :]).astype(int)).tolist()
                mouth = ((landmarks[0:2, self.idxMouth].T * np.array([width, height])[None, :]).astype(int)).tolist()
                face = ((landmarks[0:2, self.idxFace].T * np.array([width, height])[None, :]).astype(int)).tolist()
                self.mar = Calculations.compute_mar(mouth)
                self.adr = Calculations.compute_adr(eyes_left, eyes_right)
                pitch, yaw, roll = self.head_position.head_position_data(img.shape, landmarks)
                if time_elapsed < self.setup_time:
                    self.yawn_detector.setup_mar(self.mar)
                    self.eye_long_closed_detector.setup_adr(self.adr)
                    self.head_position.setup_yaw_pitch(pitch, yaw)
                    cv2.putText(img, "Setting Up!! Please Look Forward!!", (10, 90), cv2.FONT_HERSHEY_PLAIN, 1.5,
                                color=(0,0,255), thickness=2)

                    print("Setting Up!!!")
                else:
                    if fps != 0:
                        factor = 26
                        self.threshold = 1.9#factor / fps
                    text = self.head_position.detect_headPos(img=img, pitch=pitch, yaw=yaw, roll=roll,
                                                             frame_count=frame_count,
                                                             turn_time_threshold=self.threshold)
                    if text == "Normal Position":
                        self.yawn_detector.detect_yawn(img=img, mar=self.mar, frame_count=frame_count,
                                                       yawn_time_threshold=self.threshold,time_elapsed=time_elapsed)
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

                # """Face Bounding Box drawing complete"""
                # if text == "Normal Position":
                #     left_eye_img, _ = crop(img, np.array(eyes_left))
                #     right_eye_img, _ = crop(img, np.array(eyes_right))
                #     mouth_img, _ = crop(img, np.array(mouth))
                #     cv2.imshow("left_eye_img", left_eye_img)
                #     cv2.imshow("right_eye_img", right_eye_img)
                #     cv2.imshow("mouth_img", mouth_img)
                # else:
                #     cv2.waitKey(1)
        else:
            cv2.putText(img=img, text="Face Not Detected", org=(10, 120), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,
                        color=(0, 0, 255), thickness=2)
