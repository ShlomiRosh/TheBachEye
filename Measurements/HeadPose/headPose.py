import glob
import ntpath

import config
from Measurements import abstractMeasurement as am
from Services import loggerService
import warnings
import numpy as np
import torch
import math
from torchvision import transforms
import cv2
from Measurements.HeadPose.detect import AntiSpoofPredict
from Measurements.HeadPose.pfld.pfld import PFLDInference

warnings.filterwarnings('ignore')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class HeadPose(am.AbstractMeasurement):

    def __init__(self):
        """
        initialize the parent class.
        """
        am.AbstractMeasurement.__init__(self)
        self.video_writer = get_video_writer() if config.DEBUG else None

    def run(self, frame, dict_results):
        """
        run the head pose algorithm on the given frame
        :param frame: frame to process.
        :param dict_results: a dictionary which the result will be put there
        :return: pair of key = 'HeadPose',
        value = True if the face is looking toward the screen and False otherwise.
            """
        run_result = {repr(self): False}
        try:
            # get dictionary point and a few key points (1,31,51)
            point_dict = get_point_dict(frame)
            point1 = [get_num(point_dict, 1, 0), get_num(point_dict, 1, 1)]
            point31 = [get_num(point_dict, 31, 0), get_num(point_dict, 31, 1)]
            point51 = [get_num(point_dict, 51, 0), get_num(point_dict, 51, 1)]
            crossover51 = get_intersection(point51, [point1[0], point1[1], point31[0], point31[1]])

            # get yaw, pitch and roll measures
            yaw = get_yaw(point1, point31, crossover51)
            pitch = get_pitch(point51, crossover51)
            roll = get_roll(point_dict)

            run_result[repr(self)] = True
            is_looking = {'yaw': True, 'pitch': True, 'roll': True}

            # check the valid range of yaw and pitch
            hp_range = config.HEAD_POSE['range']
            if yaw < hp_range['yaw'][0] or yaw > hp_range['yaw'][1]:
                run_result[repr(self)] = is_looking['yaw'] = False
            if pitch < hp_range['pitch'][0] or pitch > hp_range['pitch'][1]:
                run_result[repr(self)] = is_looking['pitch'] = False

            if config.DEBUG:
                self.write_measures_to_video(frame, yaw, pitch, roll, is_looking)

        except Exception as e:
            # write error to log file
            loggerService.get_logger().error(str(e))
        finally:
            dict_results.update(run_result)

    def write_measures_to_video(self, frame, yaw, pitch, roll, is_looking):
        """
        write all the measures (yaw, pitch, roll) to an output video
        :param frame: frame to write the result to
        :param yaw: the yaw (left and right movements) measure in degrees.
        :param pitch: the pitch (up and down movements) measure in degrees.
        :param roll: the roll (tilt the head diagonally left and right) measure in degrees.
        :param is_looking: a dictionary which hold for each measure
        the decision whether the person is looking toward the screen or not.
        :return: void
        """

        x, y, font_face, color, thickness = 30, 50, 1, (0, 255, 0), 2
        distance = 50

        cv2.putText(frame, f"Yaw(degree): {yaw}", (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, font_face, color, thickness)
        cv2.putText(frame, f"Pitch(degree): {pitch}", (x, y + distance), cv2.FONT_HERSHEY_COMPLEX_SMALL, font_face,
                    color, thickness)
        cv2.putText(frame, f"Roll(degree): {roll}", (x, y + (2 * distance)), cv2.FONT_HERSHEY_COMPLEX_SMALL, font_face,
                    color, thickness)

        cv2.putText(frame, f"look  {is_looking['yaw']}", (x, y + (3 * distance)), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    font_face, color, thickness)
        cv2.putText(frame, f"look  {is_looking['pitch']}", (x, y + (4 * distance)), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    font_face, color, thickness)
        cv2.putText(frame, f"look  {is_looking['roll']}", (x, y + (5 * distance)), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    font_face, color, thickness)

        self.video_writer.write(frame)

    def __repr__(self):
        return 'HeadPose'


def get_num(point_dict, name, axis):
    """
    get the number from the points dictionary according to the given params
    :param point_dict: dictionary of points in the space
    :param name: number of point
    :param axis: what axis (x = 0 or y = 1)
    :return: the number
    """
    num = point_dict.get(f'{name}')[axis]
    num = float(num)
    return num


def get_intersection(point, line):
    """
    get the intersection point of a point and a line.
    :param point: a point (x,y).
    :param line: two edge points in array representing a line.
    :return: the intersection point.
    """
    x1 = line[0]
    y1 = line[1]
    x2 = line[2]
    y2 = line[3]

    x3 = point[0]
    y3 = point[1]

    k1 = (y2 - y1) * 1.0 / (x2 - x1)
    b1 = y1 * 1.0 - x1 * k1 * 1.0
    k2 = -1.0 / k1
    b2 = y3 * 1.0 - x3 * k2 * 1.0
    x = (b2 - b1) * 1.0 / (k1 - k2)
    y = k1 * x * 1.0 + b1 * 1.0
    return [x, y]


def get_distance(point_1, point_2):
    """
    get the euclidean distance between two given points.
    :param point_1: point in space.
    :param point_2: point in space.
    :return: the euclidean distance between the two.
    """
    x1 = point_1[0]
    y1 = point_1[1]
    x2 = point_2[0]
    y2 = point_2[1]
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance


def get_frame_cropped(frame):
    """
    get a cropped frame of a given frame.
    :param frame: frame to crop.
    :return: the cropped frame.
    """
    height, width = frame.shape[:2]
    model_test = AntiSpoofPredict(config.CAM_SRC)
    image_bbox = model_test.get_bbox(frame)

    x1 = image_bbox[0]
    y1 = image_bbox[1]
    x2 = image_bbox[0] + image_bbox[2]
    y2 = image_bbox[1] + image_bbox[3]
    w = x2 - x1
    h = y2 - y1

    size = int(max([w, h]))
    cx = x1 + w / 2
    cy = y1 + h / 2
    x1 = cx - size / 2
    x2 = x1 + size
    y1 = cy - size / 2
    y2 = y1 + size

    dx = max(0, -x1)
    dy = max(0, -y1)
    x1 = max(0, x1)
    y1 = max(0, y1)

    edx = max(0, x2 - width)
    edy = max(0, y2 - height)
    x2 = min(width, x2)
    y2 = min(height, y2)

    cropped = frame[int(y1):int(y2), int(x1):int(x2)]
    if dx > 0 or dy > 0 or edx > 0 or edy > 0:
        cropped = cv2.copyMakeBorder(cropped, dy, edy, dx, edx, cv2.BORDER_CONSTANT, 0)

    return cropped


def get_point_dict(frame):
    """
    get the head's points based on the frame and put in a dictionary.
    :param frame: frame to detect the point of the head.
    :return: dictionary of head's points in the space.
    """
    # get cropped
    cropped = get_frame_cropped(frame)
    cropped = cv2.resize(cropped, (112, 112))

    # get input
    transform = transforms.Compose([transforms.ToTensor()])
    input = cv2.resize(cropped, (112, 112))
    input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
    input = transform(input).unsqueeze(0).to(device)

    # get landmark
    plfd_backbone = init_plfd_backbone()
    _, landmarks = plfd_backbone(input)
    pre_landmark = landmarks[0]
    pre_landmark = pre_landmark.cpu().detach().numpy().reshape(-1, 2) * [112, 112]

    # build the points dictionary
    point_dict = {}
    i = 0
    for (x, y) in pre_landmark.astype(np.float32):
        point_dict[f'{i}'] = [x, y]
        i += 1

    return point_dict


def init_plfd_backbone():
    """
    initialize plfd_backbone object with data from checkpoint.
    :return: the plfd_backbone object.
    """
    checkpoint = torch.load(config.HEAD_POSE['snapshot_file'], map_location=device)
    plfd_backbone = PFLDInference().to(device)
    plfd_backbone.load_state_dict(checkpoint['plfd_backbone'])
    plfd_backbone.eval()
    plfd_backbone = plfd_backbone.to(device)
    return plfd_backbone


def get_yaw(point1, point31, crossover51):
    """
    get the yaw measure (left and right) based on the given head's points.
    :param point1: one side of the face.
    :param point31: the other side of the face.
    :param crossover51: the lne cross between the two.
    :return: the yaw measure in degrees
    """
    yaw_mean = get_distance(point1, point31) / 2
    yaw_right = get_distance(point1, crossover51)
    yaw = (yaw_mean - yaw_right) / yaw_mean
    yaw = int(yaw * 71.58 + 0.7037)
    return yaw


def get_pitch(point51, crossover51):
    """
        get the pitch measure (up and down) based on the given head's points.
        :param point51: one side of the face.
        :param crossover51: the lne cross between the two.
        :return: the pitch measure in degrees
        """
    pitch_dis = get_distance(point51, crossover51)
    if point51[1] < crossover51[1]:
        pitch_dis = -pitch_dis
    pitch = int(1.497 * pitch_dis + 18.97)
    return pitch


def get_roll(point_dict):
    """
     get the roll (tilt the head diagonally left and right) measure in degrees.
    :param point_dict: the head's points dictionary.
    :return: the roll measure in degrees.
    """
    roll_tan = abs(get_num(point_dict, 60, 1) - get_num(point_dict, 72, 1)) / abs(
        get_num(point_dict, 60, 0) - get_num(point_dict, 72, 0))
    roll = math.atan(roll_tan)
    roll = math.degrees(roll)
    if get_num(point_dict, 60, 1) > get_num(point_dict, 72, 1):
        roll = -roll
    roll = int(roll)
    return roll


def get_video_writer():
    """
    get a video writer in order to write a video
    :return: a video writer.
    """
    video_capture = cv2.VideoCapture(config.CAM_SRC, cv2.CAP_DSHOW)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # print("fps:", fps, "size:", size)
    video_writer = cv2.VideoWriter(config.HEAD_POSE['video_file'], cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), fps,
                                   size)
    return video_writer


def test_head_pose_measure():
    """
    test the run function by capturing a frame after frame and process it.
    :return: void
    """
    dict_results = {}
    # video_capture = cv2.VideoCapture(config.CAM_SRC, cv2.CAP_DSHOW)
    video_capture = cv2.VideoCapture(config.CAM_SRC)
    success, frame = video_capture.read()
    hp = HeadPose()
    while success:
        hp.run(frame, dict_results)
        print(dict_results)
        success, frame = video_capture.read()
    video_capture.release()


def test_measurement_on_images(file_list):
    """
    test the headPose measurement by static labeled images and print the test results.
    :param file_list: list of images to run the measurement on them.
    :return: void.
    """
    test_details_list = []
    for idx, file in enumerate(file_list):
        dict_results = {}
        image = cv2.imread(file)
        HeadPose().run(image, dict_results)
        file_name = ntpath.basename(file)
        is_there_face = "True" in file_name
        test_details_list.append([file_name, is_there_face, dict_results["HeadPose"],
                                  is_there_face == dict_results["HeadPose"]])

    # print test results in a readable table format
    headers = ['File Name', 'Head Is Facing Screen', 'Measurement Result', 'Test Result']
    # print(tabulate(test_details_list, headers))


if __name__ == "__main__":
    file_list = glob.glob(r"..\TestImages\HeadPose\*.jpg")
    test_measurement_on_images(file_list)
    test_head_pose_measure()
