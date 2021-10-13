from PIL import Image
from Measurements.FaceRecognition import faceRecognition as fr
from ImageProcessing import superResolution as sr
import cv2
import numpy


def check_recognition(path):
    """
    Check for student FaceRecognition.
    :param path: path to the snapshot image
    :return msg: True or false according to FaceRecognition result
    """
    img = Image.open(path)
    face_recognition_res = {}
    img = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
    # img = sr.SuperResolution(img, 0).get_image()
    fr.FaceRecognition().run(img, face_recognition_res)
    return face_recognition_res[fr.FaceRecognition().__repr__()]


if __name__ == '__main__':
    print(check_recognition(r"C:\Users\User\Downloads\1.jpg"))
