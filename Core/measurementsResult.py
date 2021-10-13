import datetime

from Core.lessonConfiguration import LessonConfiguration
from Core.studentManager import StudentManager
from Measurements import soundCheck, faceDetector, onTop
from Measurements.ObjectDetection import objectDetection as od
from Measurements.SleepDetector import sleepDetector as sd
from Measurements.HeadPose import headPose as hp
from Measurements.FaceRecognition import faceRecognition as fr
from Services import datetimeService


class MeasurementsResult:
    """
    This class holds the result and current time in order to know what time the measures were taken
    """

    def __init__(self, measurements_result):
        """
        initialize the class by setting the result and the current time.
        :param measurements_result: a dictionary which contains all the measurements result.
        """
        self.result = dict(measurements_result)
        self.time = datetime.datetime.now()

    def get_measurement_dto(self):
        """
        return measurements data and time as MeasurementDto as server format
        :return: MeasurementDto in format supported by the server
        """
        self.result['id'] = 0
        self.result['dateTime'] = datetimeService.convert_datetime_to_iso(self.time)
        self.result['lessonId'] = LessonConfiguration.get_lesson()['id']
        self.result['personId'] = StudentManager.get_student()['id']
        return self.result
