"""import the necessary packages"""
import cv2
import sys
import time
import mediapipe as mp
from facedetect import FaceDetection
import numpy as np
import datetime


def loadVideo(FileName, FilePath, skipFrames):
    tstamp = time.time()
    print('[INFO] Initialization in progress')
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5,
                                      min_tracking_confidence=0.5)
    face_detection = FaceDetection()
    print('[INFO] Initialization Complete in  (%.4f sec)' % (time.time() - tstamp))
    print('[INFO] ' + FileName + ' starting video stream thread')
    print("[INFO] Press 'q' to quit  ")
    cap = cv2.VideoCapture(FilePath)
    frame_count = 0
    total_start_time = 0
    previous_frame_time = 0
    is_setup_done = False
    fps = 0
    set_AvgFps = 0
    setup_time = 10

    while True:
        if total_start_time == 0:
            total_start_time = time.time()
        new_frame_time = time.time()
        ret, img = cap.read()

        if not ret:
            if frame_count != 0:
                print("[INFO] Video Finished Loading")
                break
            else:
                print("[Warning] Video Not Loaded!!!!")
                break
        else:
            if frame_count % skipFrames == 0:
                color = (32, 48, 2)
                img = cv2.resize(img, (640, 480))
                img.flags.writeable = False
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(img)
                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                time_elapsed = time.time() - total_start_time
                face_detection.detectFace(img=img, results=results, frame_count=frame_count, time_elapsed=time_elapsed,
                                          fps=set_AvgFps)
                if time_elapsed > setup_time:
                    if is_setup_done is False:
                        set_AvgFps = int(frame_count / time_elapsed)
                        is_setup_done = True
                        print("Set up complete in frame:", frame_count)
                        print("Average Fps", set_AvgFps)
                duration = new_frame_time - previous_frame_time
                previous_frame_time = new_frame_time
                hrMinSec = datetime.timedelta(seconds=int(time_elapsed))
                cv2.putText(img, "Video Name: {}".format(video), (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5,
                            color=color, thickness=2)
                cv2.putText(img, "Frame No: {}".format(frame_count), (10, 60), cv2.FONT_HERSHEY_PLAIN, 1.5,
                            color=color, thickness=2)
                cv2.putText(img=img, text="Time: {}".format(hrMinSec), org=(400, 30),
                            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,
                            color=color, thickness=2)
                cv2.putText(img=img, text="FPS: {:.2f}".format(skipFrames / duration), org=(400, 60),
                            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5,
                            color=color, thickness=2)
                cv2.imshow("Image", img)
                # name = './data/' + str(frame_count) + '.jpg'
                # cv2.imwrite(name, img)
                frame_count += 1
            else:
                frame_count += 1
            if cv2.waitKey(33) == ord('q'):
                cv2.destroyAllWindows()
                cap.release()
                break

    cv2.destroyAllWindows()
    cap.release()
    total_duration = time.time() - total_start_time
    avg_FPS = round(frame_count / total_duration, 2)
    print('[INFO] ' + FileName + ' with ' + str(frame_count) + ' Frames stream finished in  (%.4f sec)'
          % total_duration + " and whole Average FPS: " + str(avg_FPS) + " and setup average FPS: " + str(
        set_AvgFps) + '\n')
    return avg_FPS, set_AvgFps


if __name__ == '__main__':
    directory = "./testVideos/"
    video = "1-Female.avi"
    skipFrames = 1
    path = directory + video
    avgFps, setAvgFps = loadVideo(FileName=video, FilePath=path, skipFrames=skipFrames)
    file = open("./data/FPS_" + str(skipFrames) + ".txt", 'a')
    file.writelines("------ " + video + " ------\n")
    file.writelines("Average FPS: " + str(avgFps) + " Average setup FPS: " + str(setAvgFps) + "\n\n")
    file.close()
    print("\n------------------------------------------------------------------------------\n")
