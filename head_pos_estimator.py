import numpy as np
import cv2

import time
from face_geometry import get_metric_landmarks, PCF, procrustes_landmark_basis
from threading import Thread
from playsound import playsound


def playy():
    print("beep")
    playsound('beep.mp3', block=False)


class HeadPosition:
    def __init__(self):
        print('     [INFO] Head Position INIT done.')

        self._turn_count = 0
        self._isTurned = False
        self._turn_threshold = 30
        self.frame = 0
        self._yaw_meanPoint_setup = []
        self._pitch_meanPoint_setup = []
        self._yaw_mean_point = 0
        self._pitch_mean_point = 0
        self._is_head_position_setup = True
        self._turn_timer = 0
        self.points_idx = [33, 263, 61, 291, 199]
        self.points_idx = self.points_idx + [key for (key, val) in procrustes_landmark_basis]
        self.points_idx = list(set(self.points_idx))
        self.points_idx.sort()

    def head_position_data(self, shape, landmarks):
        frame_height, frame_width, _ = shape
        center = (frame_width / 2, frame_height / 2)
        focal_length = shape[1]
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )
        dist_matrix = np.zeros((4, 1))
        pcf = PCF(near=1, far=10000, frame_height=frame_height, frame_width=frame_width, fy=camera_matrix[1, 1])
        metric_landmarks, pose_transform_mat = get_metric_landmarks(landmarks.copy(), pcf)
        model_points = metric_landmarks[0:3, self.points_idx].T
        image_points = landmarks[0:2, self.points_idx].T * np.array([shape[1], shape[0]])[None, :]
        success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                    dist_matrix, flags=cv2.SOLVEPNP_ITERATIVE)

        rotationMatrix, jac = cv2.Rodrigues(rotation_vector)
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rotationMatrix)
        pitch = angles[0]
        yaw = angles[1]
        roll = angles[2]
        if angles[0] < 0:
            pitch = 360 + angles[0]
        return pitch, yaw, roll

    def setup_yaw_pitch(self, pitch, yaw):
        self._pitch_meanPoint_setup.append(pitch)
        self._yaw_meanPoint_setup.append(yaw)

    def detect_headPos(self, img, pitch, yaw, roll, frame_count, turn_time_threshold):
        text = "Normal Position"
        color = (36, 53, 78)
        T = Thread(target=playy)
        if self._is_head_position_setup is True:
            self._pitch_meanPoint_setup.sort(reverse=True)
            self._yaw_meanPoint_setup.sort(reverse=True)
            lower_limit = int(0.15 * len(self._yaw_meanPoint_setup))
            upper_limit = int(0.70 * len(self._yaw_meanPoint_setup))
            print(self._pitch_meanPoint_setup)
            self._pitch_mean_point = round(sum(self._pitch_meanPoint_setup[lower_limit:upper_limit]) /
                                           len(self._pitch_meanPoint_setup[lower_limit:upper_limit]), 4)
            self._yaw_mean_point = round(sum(self._yaw_meanPoint_setup[lower_limit:upper_limit]) /
                                         len(self._yaw_meanPoint_setup[lower_limit:upper_limit]), 4)
            self._is_head_position_setup = False
            del self._pitch_meanPoint_setup
            del self._yaw_meanPoint_setup
            del lower_limit
            del upper_limit
        else:
            if yaw < - 35:
                text = "Face Left"
                if self._turn_timer == 0:
                    self._turn_timer = time.time()
                if time.time() - self._turn_timer > turn_time_threshold:
                    text = 'Left Warning'
                    T.start()

            elif yaw > 35:
                text = "Face Right "

                if self._turn_timer == 0:
                    self._turn_timer = time.time()
                if time.time() - self._turn_timer > turn_time_threshold:
                    text = 'Right Warning'
                    T.start()

            elif pitch > self._pitch_mean_point + 35:
                text = "Face Down"
                if self._turn_timer == 0:
                    self._turn_timer = time.time()
                if time.time() - self._turn_timer > turn_time_threshold:
                    text = 'Down Warning'
                    T.start()

            elif pitch < self._pitch_mean_point - 30:
                text = "Face Up"
                if self._turn_timer == 0:
                    self._turn_timer = time.time()
                if time.time() - self._turn_timer > turn_time_threshold:
                    text = 'Up Warning'
                    T.start()

            elif roll < -30:
                text = "Roll-Right"

                if self._turn_timer == 0:
                    self._turn_timer = time.time()
                if time.time() - self._turn_timer > turn_time_threshold:
                    text = 'Roll-Right Warn'
                    T.start()
            elif roll > + 30:
                text = 'Roll-Left'
                if self._turn_timer == 0:
                    self._turn_timer = time.time()
                if time.time() - self._turn_timer > turn_time_threshold:
                    text = "Roll-Left Warn"
                    T.start()
            else:
                text = "Normal Position"
                self._turn_timer = 0

        cv2.putText(img, "Pitch: {:.2f}".format(pitch), (10, 90), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    color, 2)
        cv2.putText(img, "Yaw: {:.2f}".format(yaw), (10, 120), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    color, 2)
        cv2.putText(img, "Roll: {:.2f}".format(roll), (10, 150), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    color, 2)
        return text
