import face_recognition
import pickle
import cv2
import config
import os


class FaceTraining:

    def __init__(self):
        """
        init the model for training and init the images path.
        """
        script_dir = os.path.dirname(__file__)
        print('Training faces. It will take a few seconds.') if config.DEBUG else None
        self.__image_paths = [os.path.join(script_dir, 'Images/1.jpg'), os.path.join(script_dir, 'Images/2.jpg'),
                              os.path.join(script_dir, 'Images/3.jpg'), os.path.join(script_dir, 'Images/4.jpg'),
                              os.path.join(script_dir, 'Images/5.jpg')]
        self.__known_encodings = []
        self.__known_names = []
        self.__train_images_and_labels()
        self.__save_train_data()
        print('[INFO] faces trained. Exiting Program') if config.DEBUG else None

    def __train_images_and_labels(self):
        """
        get the faces from the image & set the id of a face [we set it to 1]
        """
        for (i, image_path) in enumerate(self.__image_paths):
            # load the input image and convert it from BGR (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Use Face_recognition to locate faces
            boxes = face_recognition.face_locations(rgb, model='hog')
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            # loop over the encodings
            for encoding in encodings:
                self.__known_encodings.append(encoding)
                self.__known_names.append(1)

    def __save_train_data(self):
        """
        save the train data.
        """
        data = {"encodings": self.__known_encodings, "names": self.__known_names}
        # use pickle to save data into a file for later use
        script_dir = os.path.dirname(__file__)
        f = open(os.path.join(script_dir, 'Models/face_enc'), 'wb')
        f.write(pickle.dumps(data))
        f.close()


def for_tests_only():
    """
    this function is used only for tests.
    """
    FaceTraining()


if __name__ == "__main__":
    for_tests_only()
