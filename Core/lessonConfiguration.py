import config
from Services import httpService
import copy
from Core.studentManager import StudentManager

lesson_from_server = None


class LessonConfiguration:
    """
    This class manages the lesson configuration that come from remote.
    The configuration define a specific lesson's configuration.
    """

    @staticmethod
    def get_lesson(lesson_code=None):
        """
        Get specific lesson from remote
        :param lesson_code: the lesson's password
        :return: lesson details dictionary
        """
        global lesson_from_server
        if lesson_code:
            url = config.URLS['get_lesson'] + lesson_code
            student = StudentManager.get_student()
            if student:
                result = httpService.get(url,student['token'])
                if result:
                    lesson_from_server = result.json()

        return copy.deepcopy(lesson_from_server)


if __name__ == '__main__':
    lesson = LessonConfiguration.get_lesson("999")
    if lesson:
        print('got lesson from server: ', lesson)
