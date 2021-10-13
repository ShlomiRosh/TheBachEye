from Measurements import abstractMeasurement as am
from Services import loggerService as ls
from config import DESIRED_PROGRAM
import win32gui as w
import psutil
import win32process
import win32con
from win32api import GetSystemMetrics
from Core.lessonConfiguration import LessonConfiguration as lc
import time


# The volume that a program considered to be On Top.
DESIRED_SIZE = 77


class OnTop(am.AbstractMeasurement):

    def __init__(self, debug=False):
        """
        initialize the parent class and size screen.
        """
        am.AbstractMeasurement.__init__(self)
        self.__screen_width = GetSystemMetrics(0)
        self.__screen_height = GetSystemMetrics(1)
        # If it True: If the desired program is not ON TOP, it will be.
        # If it False: Report only.
        if debug:
            self.is_active = True
        else:
            self.is_active = lc.get_lesson()['isActive']

    def run(self, frame, dict_results):
        """
        report if DESIRED program on top. if no
        update the dict_results to false else true.
        :param frame: frame to process
        :param dict_results: a dictionary which the result will be put there
        """
        result = {repr(self): False}
        try:
            am.AbstractMeasurement.run(self, frame, dict_results)
            result[repr(self)] = self.__check_and_act()
        except Exception as e:
            ls.get_logger().error(
                f'Failed to identify which program on top, due to: {str(e)}')
            dict_results.update(result)
            return
        dict_results.update(result)

    def __check_and_act(self):
        """
        check which program is in the foreground, report it and
        follow the parameters [Should you close the other programs?].
        :return: true or false depend if program on top & in good size
        """
        # Check which program is on top.
        program_name = None
        is_on_top = False
        try:
            pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())
            program_name = psutil.Process(pid[-1]).name().lower()
        except Exception as e:
            ls.get_logger().error(
                f'Failed to identify process up front, due to: {str(e)}')
        if program_name == DESIRED_PROGRAM['EXPECTED_ON_TOP']:
            is_on_top = True
            if self.__is_in_good_size():
                return True
        # If we got here the student is not watching the desired program and we act
        # according to the settings.
        if self.is_active:
            self.__handle_active_teacher(is_on_top)
        return False

    def __is_in_good_size(self):
        """
        check if window size of the program is not smaller than the
        desired volume.
        :return:  true or false depend if program in good size
        """
        rect = w.GetWindowRect(w.GetForegroundWindow())
        x, y = rect[0], rect[1]
        width, height = rect[2] + x if x < 0 else rect[2] - x, rect[3] - y
        screen_volume = self.__screen_width * self.__screen_height
        foreground_window_volume = width * height
        accepted_percentage = ((100 - DESIRED_SIZE) * screen_volume) / 100
        if screen_volume - foreground_window_volume < accepted_percentage:
            return True
        return False

    @staticmethod
    def __handle_active_teacher(is_on_top):
        """
        if the window is small enlarge it. If this is not the correct
        window you'll bring the correct window.
        :param is_on_top: bool parm
        """
        try:
            hwnd = w.FindWindow(None, DESIRED_PROGRAM['HWND'])
            if is_on_top:
                w.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            else:
                w.CloseWindow(w.GetForegroundWindow())
                w.SetForegroundWindow(hwnd)
        except IOError as e:
            pass
            # ls.get_logger().error(
            #     f'Failed to force forward the desired program, due to: {str(e)}')

    def __repr__(self):
        """
        :return: the name of the measurement.
        """
        return 'OnTop'


def for_tests_only():
    """
    A test func to this page only.
    """
    dict = {}
    x = OnTop(True)
    while True:
        x.run(None, dict)
        print(dict[x.__repr__()])
        time.sleep(5)


if __name__ == '__main__':
    for_tests_only()
