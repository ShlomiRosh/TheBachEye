from time import sleep

import cv2
import config
from Measurements import abstractMeasurement as am
from Services import loggerService
import mediapipe as mp
import glob
import ntpath
from tabulate import tabulate

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh


class FaceDetector(am.AbstractMeasurement):

    def __init__(self):
        """
        initialize the parent class and the face_mesh model.
        """
        am.AbstractMeasurement.__init__(self)
        self.face_mesh = mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    def run(self, frame, dict_results):
        """
        run the face detector algorithm on the given frame
        :param frame: frame to process.
        :param dict_results: a dictionary which the result will be put there
        :return: pair of key = 'face_detection', value = True if there is face and False otherwise.
            """
        run_result = {repr(self): False}
        try:
            # flip the image in order to represent a true self of the person not mirror of it
            # and convert its colors.
            image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            # make it read only image in order to improve the performance
            image.flags.writeable = False
            # process it by face mesh model
            results = self.face_mesh.process(image)

            if results.multi_face_landmarks:
                # face has been detected
                run_result[repr(self)] = True
                # show face net on image
                if config.DEBUG:
                    self.draw_annotations(image, results)
                # sleep(config.TIMEOUT)
        except Exception as e:
            self.face_mesh.close()
            # write error to log file
            loggerService.get_logger().error(str(e))
        finally:
            dict_results.update(run_result)

    def __repr__(self):
        return 'FaceDetector'

    def draw_annotations(self, image, results):
        """
               draw face annotations on the image.
               :param image: image to draw on.
               :param results: the face detector results.
               :return: void.
               """
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        for face_landmarks in results.multi_face_landmarks:
            # draw face landmark net
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACE_CONNECTIONS,
                landmark_drawing_spec=self.drawing_spec,
                connection_drawing_spec=self.drawing_spec)
        cv2.imshow('MediaPipe FaceMesh', image)


def test_face_detector_measure():
    """
    test the run function by capturing a frame after frame and process it.
    :return: void
    """
    dict_results = {}
    video_capture = cv2.VideoCapture(config.CAM_SRC)
    success, frame = video_capture.read()
    while success:
        FaceDetector().run(frame, dict_results)
        print(dict_results)
        success, frame = video_capture.read()


def test_measurement_on_images(file_list):
    """
    test the faceDetector measurement by static labeled images and print the test results.
    :param file_list: list of images to run the measurement on them.
    :return: void
    """
    test_details_list = []
    for idx, file in enumerate(file_list):
        dict_results = {}
        image = cv2.imread(file)
        FaceDetector().run(image, dict_results)
        file_name = ntpath.basename(file)
        is_there_face = "True" in file_name
        test_details_list.append([file_name, is_there_face, dict_results["FaceDetector"],
                                  is_there_face == dict_results["FaceDetector"]])

    # print test results in a readable table format
    headers = ['File Name', 'Face Exist', 'Measurement Result', 'Test Result']
    print(tabulate(test_details_list, headers))


if __name__ == "__main__":
    file_list = glob.glob(r".\TestImages\FaceDetector\*.jpg")
    test_measurement_on_images(file_list)
    test_face_detector_measure()
