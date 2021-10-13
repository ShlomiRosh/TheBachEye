from Measurements import abstractMeasurement as am
from ImageProcessing import superResolution as sr
from Services import loggerService as ls
import config
import os
import cv2


class ObjectDetection(am.AbstractMeasurement):

    def __init__(self):
        """
        initialize the parent class all paths & list of obj
        & list of the prohibited objects from the list of obj.
        """
        am.AbstractMeasurement.__init__(self)
        script_dir = os.path.dirname(__file__)
        self.__class_file = os.path.join(script_dir, 'Files/objects.names')
        self.__config_path = os.path.join(script_dir, 'Files/objects_config.pbtxt')
        self.__weights_path = os.path.join(script_dir, 'Files/objects_weights.pb')
        self.__prohibited_objects = config.PROHIBITED_OBJECTS
        self.__model = None
        # Threshold to detect object
        self.__threshold = config.THRESHOLD_OD
        self.__init_model()
        try:
            self.__objects = [line.strip() for line in open(self.__class_file, 'rt')]
        except ValueError as v:
            ls.get_logger().error(str(v))
        except Exception as e:
            ls.get_logger().error(f'failed to open files, due to: {str(e)}')

    def run(self, frame, dict_results):
        """
        report if we detect prohibited obj. if yes
        update the dict_results to false else true.
        :param frame: frame to process
        :param dict_results: a dictionary which the result will be put there
        """
        am.AbstractMeasurement.run(self, frame, dict_results)
        result = {repr(self): False}
        try:
            objects, confidence, box = self.__model.detect(frame, confThreshold=self.__threshold)
            # Check for prohibited objects.
            for obj in objects.flatten():
                if self.__objects[obj - 1].upper() in self.__prohibited_objects:
                    dict_results.update(result)
                    return
            result[repr(self)] = True
            dict_results.update(result)
            if config.DEBUG:
                self.__run_debug(objects, confidence, box)
        except Exception as e:
            ls.get_logger().error(
                f'Failed to detect objects, due to: {str(e)}')

    def __repr__(self):
        """
        :return: the name of the measurement.
        """
        return 'ObjectDetection'

    def __run_debug(self, objects, confidence, box):
        """
        if we in debug mode open a pop up window and show the obj
        the system detect with boxes painted over them.
        :param objects: the list of obj the system detect
        :param confidence: for each obj in what confidence the system have for
        identify him correctly.
        :param box: list of boxes
        """
        for obj, conf, b in zip(objects.flatten(), confidence.flatten(), box):
            cv2.rectangle(self.frame, b, color=(0, 145, 145), thickness=1)
            cv2.putText(self.frame, self.__objects[obj - 1].upper(), (b[0] + 10, b[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(self.frame, str(round(conf * 100, 2)), (b[0], b[1] + 70),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
        cv2.imshow("Output", self.frame)
        cv2.waitKey(0)

    def __init_model(self):
        """
        this func will init model input size & scale
        """
        try:
            self.__model = cv2.dnn_DetectionModel(self.__weights_path, self.__config_path)
            self.__model.setInputSize(320, 320)
            self.__model.setInputScale(1.0 / 100.5)
            self.__model.setInputMean((100.5, 100.5, 100.5))
            self.__model.setInputSwapRB(True)
        except ValueError as v:
            ls.get_logger().error(str(v))
        except Exception as e:
            ls.get_logger().error(f'failed to open files, due to: {str(e)}')


def for_tests_only():
    """
    A test func to this page only.
    """
    x = ObjectDetection()
    dict_res = {}
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # set video width
    cam.set(3, 640)
    # set video height
    cam.set(4, 480)
    while True:
        ret, img = cam.read()
        img = sr.SuperResolution(img, 0).get_image()
        x.run(img, dict_res)
        print(dict_res[x.__repr__()])
        cv2.imshow('camera', img)
        # Press 'ESC' for exiting video
        k = cv2.waitKey(10) & 0xff
        if cv2.waitKey(10) & 0xff == 27:
            break
    cam.release()
    cv2.destroyAllWindows()


def test_on_image():
    x = ObjectDetection()
    dict_res = {}
    image = cv2.imread(r"C:\Users\Dell\Desktop\Projects\Final\TheBackEye\ImageProcessing\SavedImages\2.png")
    x.run(image, dict_res)
    print(dict_res[x.__repr__()])


if __name__ == '__main__':
    for_tests_only()
