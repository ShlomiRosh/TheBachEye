from Measurements import faceDetector as fd
from Measurements.SleepDetector import sleepDetector as sd
from Measurements.HeadPose import headPose as hp
import multiprocessing as mp
import tkinter as tk
import cv2
import threading
import numpy
from ImageProcessing import superResolution as sr
from Measurements.FaceRecognition import faceTraining as ft
from PIL import ImageTk, Image

MSGS = {
    'FaceDetector': 'Please upload a pic with face in it.\n',
    'SleepDetector': 'Please upload a pic with eyes open.\n',
    'HeadPose': 'Pleas upload a pic when you look straight to the camera.\n'
}


def check_pic(results):
    """
    Check if the user image is a good image, if not return msg
    :param results: array of result measurements
    :return msg: return a msg for a good & bad pic.
    """
    msg = ''
    for key, val in results.items():
        if not val:
            msg += MSGS[key]
    return msg


def upload_pic(pics):
    """
    If its a good pics save it. return a msg for a good & bad pics.
    :param pics: the pics from user
    :return msg: return a dict of msgs for a good & bad pics for all images.
    """
    dict_results = mp.Manager().dict()
    processes = []
    for key, val in pics.items():
        img = cv2.cvtColor(numpy.asarray(val), cv2.COLOR_RGB2BGR)
        process = mp.Process(target=run_images_checks, args=(img, dict_results, pics, key))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
        process.close()
    flg = all(elem == '' for elem in dict_results.values())
    if flg:
        save_pic_and_train_face_recognition(pics)
        return 'OK'
    return dict_results


def save_pic_and_train_face_recognition(pics):
    """
    save the images & train the face recognition model on this images for future using.
    :param pics: images to train and save
    """
    # save the pictures
    i = 1
    for img in pics.values():
        img.save("Measurements/FaceRecognition/Images/" + str(i) + ".jpg")
        i += 1
    # train the face recognition model on the saved images
    ft.FaceTraining()


def run_images_checks(image, dict_res, pics, i):
    """
    processes func to run measurements for each image.
    :param image: the image to run measurements on
    :param pics: the images dict
    :param dict_res: dict of msgs for the images if all measurements return true,
    the msg will be ''
    :param i: key to put the msg into in the dict of msgs
    """
    # update the images in the pics dict to images in super resolution
    # image = sr.SuperResolution(image, 0).get_image()
    # pics[i] = image
    measurements = [sd.SleepDetector(), fd.FaceDetector(), hp.HeadPose()]
    measurements_results = {}
    for measure in measurements:
        measure.run(image, measurements_results)
    msg = check_pic(measurements_results)
    dict_res[i] = msg


def send_user_pic():
    upload_pic({'0': Image.open(r"C:\Users\User\Downloads\1.jpg"), '1': Image.open(r"C:\Users\User\Downloads\2.jpg")})


def try_func():
    x = threading.Thread(target=lambda: send_user_pic())
    x.setDaemon(True)
    x.start()


if __name__ == '__main__':
    root = tk.Tk()
    w = tk.Button(root, width=640, height=480, command=try_func).pack()
    root.mainloop()

