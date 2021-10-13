import os
from Core.studentManager import StudentManager as sm
from Core.lessonConfiguration import LessonConfiguration as lc


class LoginController:
    """
    This class is responsible for the page login.
    """
    def __init__(self, password, class_code):
        """
        Init variables.
        :param password: the student password
        :param class_code: the student class code
        """
        self.__password = password
        self.__class_code = class_code
        self.__msg = {'Class Code': '', 'Password': ''}

    def check_validation(self):
        """
        Check validation of student password & class_code.
        """
        if len(self.__class_code) == 0:
            self.__msg['Class Code'] += 'Class Code cannot be empty.\n'
        if len(self.__password) == 0:
            self.__msg['Password'] += 'Password cannot be empty.\n'
        if not all(ord(c) < 128 for c in self.__class_code):
            self.__msg['Class Code'] += 'Class Code not in ascii.\n'
        if not all(ord(c) < 128 for c in self.__password):
            self.__msg['Password'] += 'Password not in ascii.\n'
        return self.__msg

    def check_student_data_in_server(self):
        """
        check that the student password and class code exists in the server.
        :return: msg: a dictionary which tells us if the student data exists in server
        """
        msg = {'Class Code': '', 'Password': ''}
        password_res = sm.get_student(self.__password)
        if password_res is None:
            msg['Password'] = 'This Password dedent exists in our system, please try again.'
        code_res = lc.get_lesson(self.__class_code)
        if code_res is None:
            msg['Class Code'] = 'This Class Code dedent exists in our system, please try again.'
        return msg

    @staticmethod
    def page_to_jump():
        """
        Check if we already have email and pics for this student.
        """
        res = sm.get_student()
        if res['email'] == '':
            return 'ToValidation'
        else:
            # check if the student already has images
            files = os.listdir('Measurements/FaceRecognition/Images')
            if files == ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']:
                return 'ToSnapshot'
            else:
                return 'ToUpload'
