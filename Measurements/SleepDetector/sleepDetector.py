from Measurements import abstractMeasurement as am
from Services import loggerService as ls
import config
import cv2
import os
import face_recognition
from PIL import ImageTk, Image
from scipy.spatial import distance as dist
from ImageProcessing import superResolution
import numpy


class SleepDetector(am.AbstractMeasurement):

    def __init__(self):
        """
        initialize the parent class and eye_cascade model.
        """
        am.AbstractMeasurement.__init__(self)
        script_dir = os.path.dirname(__file__)
        self.__path = os.path.join(script_dir, "Model/haarcascade_eye_tree_eyeglasses.xml")
        try:
            self.__eye_cascade = cv2.CascadeClassifier(self.__path)
        except FileNotFoundError as f:
            ls.get_logger().error(str(f))
        except Exception as e:
            ls.get_logger().error(f'failed to open files, due to: {str(e)}')

    def run(self, frame, dict_results):
        """
        run the sleep detector algorithm on the given frame & if student asleep
        update the dict_results to false else true.
        :param frame: frame to process
        :param dict_results: a dictionary which the result will be put there
        """
        am.AbstractMeasurement.run(self, frame, dict_results)
        flg_frame = frame
        eyes = None
        closed = True
        result = {repr(self): False}
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = self.__eye_cascade.detectMultiScale(frame, scaleFactor=1.1,
                                                       minNeighbors=1, minSize=(1, 1))
            # try to find eye in other way
            rgb_frame = flg_frame[:, :, ::-1]
            face_landmarks_list = face_recognition.face_landmarks(rgb_frame)
            for face_landmark in face_landmarks_list:
                left_eye = face_landmark['left_eye']
                right_eye = face_landmark['right_eye']
                ear_left = self.get_eye_ratio(left_eye)
                ear_right = self.get_eye_ratio(right_eye)
                closed = ear_left < 0.2 and ear_right < 0.2
            if eyes is None and closed:
                ls.get_logger().error(
                    f'Failed to identify the eyes, due to: There are no eyes in the frame\n'
                    f'Possible reasons: wearing glasses, problematic lighting.')
                dict_results.update(result)
                return
        except Exception as e:
            print(e)
            ls.get_logger().error(
                f'Failed to identify the eyes, due to: {str(e)}')
        if len(eyes) != 0 or (not closed):
            result[repr(self)] = True
        dict_results.update(result)

    @staticmethod
    def get_eye_ratio(eye):
        a = dist.euclidean(eye[1], eye[5])
        b = dist.euclidean(eye[2], eye[4])
        c = dist.euclidean(eye[0], eye[3])
        return (a + b) / (2.0 * c)

    def __repr__(self):
        """
        :return: the name of the measurement.
        """
        return 'SleepDetector'


def for_tests_only():
    """
    A test func to this page only.
    """
    cap = cv2.VideoCapture(config.CAM_SRC, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if ret:
            dict = {}
            SleepDetector().run(frame, dict)
            print(dict[SleepDetector().__repr__()])
            cv2.imshow('Sleep Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def for_test_only_image():
    img = Image.open(r"C:\Users\User\Downloads\9.jpg")
    img = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
    dict = {}
    SleepDetector().run(img, dict)
    print(dict[SleepDetector().__repr__()])


if __name__ == '__main__':
    for_tests_only()
