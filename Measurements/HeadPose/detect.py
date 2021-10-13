import os
import cv2
import math
import torch
import numpy as np
import torch.nn.functional as F

import config


class Detection:
    def __init__(self):
        """
        init the class with caffe model and decide the amount of confidence.
        """
        caffemodel = config.HEAD_POSE['caffemodel']
        deploy = config.HEAD_POSE['deploy']
        self.detector = cv2.dnn.readNetFromCaffe(deploy, caffemodel)
        self.detector_confidence = 0.7

    def get_bbox(self, img):
        """
        get a bbox representing the corners of the image after normalization
        :param img: image to get its corners.
        :return: an array of corners values.
        """
        height, width = img.shape[0], img.shape[1]
        aspect_ratio = width / height
        if img.shape[1] * img.shape[0] >= 192 * 192:
            img = cv2.resize(img,
                             (int(192 * math.sqrt(aspect_ratio)),
                              int(192 / math.sqrt(aspect_ratio))), interpolation=cv2.INTER_LINEAR)

        blob = cv2.dnn.blobFromImage(img, 1, mean=(104, 117, 123))
        self.detector.setInput(blob, 'data')
        out = self.detector.forward('detection_out').squeeze()
        max_conf_index = np.argmax(out[:, 2])
        left, top, right, bottom = out[max_conf_index, 3] * width, out[max_conf_index, 4] * height, out[
            max_conf_index, 5] * width, out[max_conf_index, 6] * height
        bbox = [int(left), int(top), int(right - left + 1), int(bottom - top + 1)]
        return bbox


class AntiSpoofPredict(Detection):
    def __init__(self, device_id):
        """
        init the class and set calculation device to be cuda if cuda is available and cpu if not.
        :param device_id: the device id.
        """
        super(AntiSpoofPredict, self).__init__()
        self.device = torch.device("cuda:{}".format(device_id) if torch.cuda.is_available() else "cpu")