import logging

DEBUG = False
TIMEOUT = 5
CAM_SRC = 1

"""
enlist each action and its corresponding URL.
use: every page that use httpService.
"""
BASE_URL = "https://datamanagementapi20211003134521.azurewebsites.net/api/"
# BASE_URL ="https://localhost:44378/api/"
URLS = {
    'post_measures': BASE_URL + 'Measurement/',
    'post_stacked_measures': BASE_URL + 'Measurement/PostMeasurements',
    'post_logs': BASE_URL + 'Log/',
    'is_server_alive': BASE_URL + 'IsAlive/',
    'get_student': BASE_URL + 'Person/GetStudent/',
    'put_student': BASE_URL + 'Person/',
    'get_lesson': BASE_URL + 'Lesson/GetNextLesson/'
}

"""
enlist the log files keys and theirs physical path.
use: in loggerService and might be used to in each page that use loggerService 
"""
LOG_FILES = {
    'default': './Logs/back_eye.log'
}

"""
describe the several options for the log files configuration,
such as: mode, format, date foramt and log level.
use: in loggerService.
"""
LOG_OPTIONS = {
    'file_mode': 'a',
    'format': '%(asctime)s,%(msecs)d %(levelname)s %(message)s',
    'date_format': '%d/%m/%y %H:%M:%S',
    'level': logging.WARNING
}

"""
what program should be on top & what are window name.
use: in onTop.py
"""
DESIRED_PROGRAM = {
    'EXPECTED_ON_TOP': 'zoom.exe',
    'HWND': 'Zoom Meeting'
}

"""
all the data about the app.
use: in uiController.py
"""
APP = {
    'WIN_SIZE': '430x550+50+20',
    'TITLE': 'TheBackEye',
    'WIDTH': 430,
    'HEIGHT': 550,
    'FONT_OUTPUT': ("Ariel", 10),
    'FONT_MSG': ("Ariel", 10, "bold"),
    'FONT_HEALTH': ("Impact", 19, "bold", "underline")
}

"""
gui app object.
use: in uiController.py
"""
APPLICATION = None

"""
the name & id the student enter with to the app.
use: loginPage & probably in the warning system
"""
USER_DATA = {
    'USERNAME': '',
    'ID': ''
}

"""
enlist parameters that needed for head pose estimation.
use: in headPose measurement.
"""
HEAD_POSE = {
    'video_file': r'./Measurements/HeadPose/video/result.mp4',
    'snapshot_file': r'./Measurements/HeadPose/checkpoint/snapshot/checkpoint.pth.tar',
    'caffemodel': r'./Measurements/HeadPose/checkpoint/Widerface-RetinaFace.caffemodel',
    'deploy': r'./Measurements/HeadPose/checkpoint/deploy.prototxt',
    'range': {
        'yaw': (-10, 10),
        'pitch': (4, 20),
        'roll': (-30, 50)
    }
}

"""
what object we do not allow the student to mess with during lesson
we probably should receive this objects from the teacher.
use: in class ObjectDetector
"""
PROHIBITED_OBJECTS = ['CELL PHONE']

"""
teacher msgs for the student if the student fail in the
measurements.
use: in voice system
"""
TEACHER_MSGS = None

"""
email address & password that the system use to connect with the student
end send to him message.
use: in email system & email warning.
"""
EMAIL = {
    'EMAIL': "TheBackEyeApp@gmail.com",
    'PASSWORD': "thebackeye12345",
    'USER_EMAIL': "rshalom8@gmail.com"
}

"""
enlist the prerequisite programs that must be installed
before running the application.
use: in healthChecksService.
"""
PREREQUISITE_INSTALLATIONS = {
    'zoom': 'Zoom.exe',
    'manycam': 'ManyCam.exe'
}
"""
enlist the prerequisite processes that must be running
before running the application.
use: in healthChecksService.
"""
PREREQUISITE_PROCESSES = {
    'manycam': 'ManyCam.exe'
}

"""
specify the expected volume (in dB) for the sound check 
"""
SOUND_CHECK = {
    'min_volume': 0.34
}

"""
specify the interval seconds which every x seconds alert system will be called
"""
ALERT_SYSTEM = {
    'interval_seconds': 90
}

"""
specify the interval seconds which every x seconds measurements_interval will be calculate
"""
MEASUREMENT_INTERVAL = {
    'interval_seconds': 90
}

"""
specify the face recognition & objects detector threshold
[minimum value in order to protect user from false negatives]
"""
THRESHOLD_FR = 40
THRESHOLD_OD = 0.45
