import face_recognition
import pickle
import cv2
from Measurements import abstractMeasurement as am
from ImageProcessing import superResolution as sr
from Services import loggerService as ls
import os


class FaceRecognition(am.AbstractMeasurement):

    def __init__(self):
        """
        initialize the parent class, model, threshold
        """
        am.AbstractMeasurement.__init__(self)
        script_dir = os.path.dirname(__file__)
        # find path of xml file containing haarcascade file
        self.__casc_path_face = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
        # load the harcaascade in the cascade classifier
        self.__face_cascade = cv2.CascadeClassifier(self.__casc_path_face)
        # load the known faces and embeddings saved in last file
        self.__data = pickle.loads(open(os.path.join(script_dir, 'Models/face_enc'), "rb").read())

    def run(self, frame, dict_results):
        """
        report if we detect the student face. if yes
        update the dict_results to false else true.
        :param frame: frame to process
        :param dict_results: a dictionary which the result will be put there
        """
        am.AbstractMeasurement.run(self, frame, dict_results)
        result = {repr(self): False}
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.__get_faces(gray)
            # convert the input frame from BGR to RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # the facial embeddings for face in input
            encodings = face_recognition.face_encodings(rgb)
            names = []
            # loop over the facial embeddings incase we have multiple embeddings for multiple fcaes
            for encoding in encodings:
                # Compare encodings with encodings
                matches = face_recognition.compare_faces(self.__data['encodings'], encoding)
                # check to see if we have found a match
                if True in matches:
                    result[repr(self)] = True
                    if True:
                        self.run_debug(frame, matches, names, faces)
            dict_results.update(result)
        except Exception as e:
            ls.get_logger().error(
                f'Failed in face recognition, due to: {str(e)}')

    def __repr__(self):
        """
        :return: the name of the measurement.
        """
        return 'FaceRecognition'

    def __get_faces(self, gray):
        """
        run the model and return the faces it detected.
        :param gray: cvt - the frame in gray color
        :return: faces: the faces it detected
        """
        faces = self.__face_cascade.detectMultiScale(gray,
                                                     scaleFactor=1.1,
                                                     minNeighbors=5,
                                                     minSize=(60, 60),
                                                     flags=cv2.CASCADE_SCALE_IMAGE)
        return faces

    def run_debug(self, frame, matches, names, faces):
        """
        in debug mode, put txt & boxes on the image we examined
        :param frame: the image to put the txt on
        :param matches: the list of matches
        :param names: list of names of to be updated
        :param faces: faces that we recognized
        """
        name = "Unknown"
        # Find positions at which we get True and store them
        matched_ids = [i for (i, b) in enumerate(matches) if b]
        counts = {}
        # loop over the matched indexes and maintain a count for each recognized face
        for i in matched_ids:
            name = self.__data['names'][i]
            counts[name] = counts.get(name, 0) + 1
        name = max(counts, key=counts.get)
        names.append(name)
        # loop over the recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2), cv2.putText(frame, str(name)
                               , (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


def for_tests_only():
    """
    this function is used only for tests.
    open the camera and start testing
    """
    x = FaceRecognition()
    dict_res = {}
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # # set video width
    # cam.set(3, 640)
    # # set video height
    # cam.set(4, 480)
    while True:
        ret, img = cam.read()
        # img = sr.SuperResolution(img, 0).get_image()
        x.run(img, dict_res)
        print(dict_res[x.__repr__()])
        cv2.imshow('camera', img)
        # Press 'ESC' for exiting video
        k = cv2.waitKey(10) & 0xff
        if cv2.waitKey(10) & 0xff == 27:
            break
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    for_tests_only()
