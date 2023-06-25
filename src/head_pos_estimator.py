import numpy as np
import cv2

import time
from face_geometry import get_metric_landmarks, PCF, procrustes_landmark_basis
from threading import Thread
from common import playy

class HeadPosition:

    """ This class is used to detect the head position from the frame.
        The class consist of a member function calculate_euler_angles, setup_yaw_pitch and detect_headPos.
    """
    def __init__(self):
        """Initializes the variables used to detect head position"""
        print('     [INFO] Head Position INIT done.')
        self._turn_count = 0
        '''Turn count'''
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

    def calculate_euler_angles(self, shape, landmarks):
        '''This function is used to calculate the Euler angles from the facial landmark points.

            :param tuple shape: Tuple consisting of height, width and number of color channels.
                                (Height, Width, No. of channels)
            :param array landmarks: Numpy array of the 486 landmarks point.

            :returns: Pitch, yaw and roll of head.

            :rtype: float
        '''
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
        """The function records the values of pitch and yaw during the setup period that 
            will be used to calculate the pitch and yaw mean point.

            :param float pitch: Pitch of the face.
            :param float yaw: Yaw of the face.

            :returns: Nothing.
        """
        self._pitch_meanPoint_setup.append(pitch)
        self._yaw_meanPoint_setup.append(yaw)

    def detect_headPos(self, img, pitch, yaw, roll, turn_time_threshold):
        """The function is used to detect the head position.
            
            :param array img: 640x480 numpy array of pixel values.
            :param float pitch: Pitch of the face.
            :param float yaw: Yaw of the face.
            :param float roll: Roll of the face.
            :param float turn_time_threshold: Time after which the alarm will be raised.

            :returns: Text indicating the face position.

            :rtype: string
        """
        text = "Normal Position"
        color = (36, 53, 78)
        T = Thread(target=playy)
        if self._is_head_position_setup is True:
            self._pitch_meanPoint_setup.sort(reverse=True)
            self._yaw_meanPoint_setup.sort(reverse=True)
            lower_limit = int(0.15 * len(self._yaw_meanPoint_setup))
            upper_limit = int(0.70 * len(self._yaw_meanPoint_setup))
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
