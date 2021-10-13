from Core.studentManager import StudentManager
from WarningSystem import voiceSystem as vs
from WarningSystem import flickerSystem as fs
from WarningSystem import emailWarning as ew
import threading


class RunSystem:

    def __init__(self, indices_dict):
        """
        initialize the indices & the processes that are related
        to the warning system.
        :param indices_dict: dictionary of indices
        """
        self.__indices_dict = indices_dict
        self.__failed_in = []
        self.__student = StudentManager.get_student()
        self.__dict_threads = {
            'voice': threading.Thread(target=vs.VoiceSystem, args=(self.__failed_in, )),
            'flicker': threading.Thread(target=fs.FlickerSystem),
            'email': threading.Thread(target=ew.EmailWarning, args=(self.__failed_in, ))
        }
        self.__init_failed_indices()
        self.__run_warning_system()

    def __run_warning_system(self):
        """
        run the warning system in parallel.
        """
        # assign all processes and start each one of them
        if not self.__failed_in:
            return
        threads = []

        for key, thread in self.__dict_threads.items():
            if key == 'email':
                if 'ObjectDetection'.upper() in self.__failed_in or 'SoundCheck'.upper() in self.__failed_in:
                    thread.start()
                    threads.append(thread)
            else:
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

    def __init_failed_indices(self):
        """
        initialize the indices that the student failed in.
        """
        for key, val in self.__indices_dict.items():
            if not val:
                self.__failed_in.append(key.upper())


def for_tests_only():
    """
    this function is used only for tests.
    """
    indices_dict = {
        'FaceDetector': True, 'ObjectDetector': False, 'SleepDetector': True,
        'OnTop': True, 'HeadPose': True, 'SoundCheck': False
    }
    RunSystem(indices_dict)


if __name__ == '__main__':
    StudentManager.get_student("333")
    for_tests_only()

