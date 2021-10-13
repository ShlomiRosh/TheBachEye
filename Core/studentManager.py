import config
from Services import httpService
import copy

student_from_server = None


class StudentManager:
    """
    This class manages the student details that come from remote.
    Student object is describe the student's personal details.
    """

    @staticmethod
    def get_student(password=None):
        """
        Get specific student from remote
        :param password: the student's password
        :return: student details dictionary
        """
        global student_from_server
        if password:
            url = config.URLS['get_student']
            result = httpService.post(url,password, None)
            if result:
                student_from_server = result.json()

        return copy.deepcopy(student_from_server)

    @staticmethod
    def update_student(student_updated):
        """
        Update student in remote
        :param student_updated: student to update
        :return: updated student details dictionary
        """
        global student_from_server
        if student_updated:
            url = config.URLS['put_student']
            result = httpService.put(url, student_updated, student_from_server['token'])
            if result:
                student_from_server = result.json()

        return StudentManager.get_student()


if __name__ == '__main__':
    student = StudentManager.get_student("999")
    if student:
        print('got student from server: ', student)
        # change something in student details
        student['person']['firstName'] = student['person']['firstName'] + 'X'
        print('got student after update: ', StudentManager.update_student(student))
        print('get from server after update: ', StudentManager.get_student("999"))
