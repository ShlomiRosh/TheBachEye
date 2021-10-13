import pyttsx3
import config
from Core.studentManager import StudentManager

FEMALE = 0
GENERAL_WARNING = 2


class VoiceSystem:

    def __init__(self, indices_list):
        """
        init indices & msgs & the model for text to speech msgs
        given the teacher an option to to give us unique messages for the student.
        :param indices_list: list of indices the student failed in
        """
        self.__indices_list = indices_list
        self.__indices_msgs = self.__init_indices_msgs() if config.TEACHER_MSGS is None else config.TEACHER_MSGS
        self.__msg = ''
        self.__general_msg = f'{StudentManager.get_student()["firstName"]} Please return to learning mode!.'
        # Object voice creation.
        self.__engine = pyttsx3.init()
        self.__init_msg()
        self.__set_voice()
        self.__debug_voice() if config.DEBUG else None
        self.__run_voice_system()

    @staticmethod
    def __init_indices_msgs():
        """
        create a dictionary of indices and their appropriate msgs if
        the student failed in those indices.
        :return: indices_msgs: a general msgs to the voice system.
        """
        indices_msgs = {
            'FACEDETECTOR': 'Our system suspects you are not in front of the screen.',
            'HEADPOSE': 'Our system notes that you are not looking at the screen.',
            'ONTOP': 'Our system detected that you are running non-lesson related apps.',
            'OBJECTDETECTION': 'Our system detected that you are dealing with distracting objects.',
            'SLEEPDETECTOR': 'Our system suspects you\'m asleep',
            'FACERECOGNITION': 'Our system suspects that you are not the person in front of the screen.',
            'MANY_FAILURES': 'Our system updates that you are completely out of learning mode.'
        }
        return indices_msgs

    def __init_msg(self):
        """
        initialize the messages into a one long string for the voice model.
        """
        if len(self.__indices_list) > GENERAL_WARNING:
            self.__msg = self.__indices_msgs['MANY_FAILURES']
            return
        for i in self.__indices_list:
            if i != 'SoundCheck'.upper():
                self.__msg += self.__indices_msgs[i] + ' '

    def __run_voice_system(self):
        """
        run the voice system & if in debug mode, record the voice system
        into a mp3 file.
        """
        self.__engine.say(self.__msg)
        self.__engine.say(self.__general_msg)
        self.__engine.runAndWait()
        if config.DEBUG:
            self.__engine.save_to_file(self.__msg + self.__general_msg, '.\\Mp3Files\\test.mp3')
            self.__engine.runAndWait()
        self.__engine.stop()

    def __debug_voice(self):
        """
        while in debug mode, print all the details about the
        voice model.
        """
        # RATE: getting details of current speaking rate.
        rate = self.__engine.getProperty('rate')
        # Printing current voice rate.
        print(rate)
        # VOLUME: getting details of the current volume level (maximum=1, minimum=0).
        volume = self.__engine.getProperty('volume')
        # Printing the current volume level.
        print(volume)
        # VOICE: getting details of the current voice (male=1, female=0).
        voice = self.__engine.getProperty('voice')
        # Printing the current voice.
        print(voice)

    def __set_voice(self):
        """
        set the voice model properties.
        """
        self.__engine.setProperty('rate', 180)
        self.__engine.setProperty('volume', 1)
        self.__engine.setProperty('voice', self.__engine.getProperty('voices')[not FEMALE].id)


def for_tests_only():
    """
    this function is used only for tests.
    """
    student_name = "David"
    indices_list = ['FACEDETECTOR', 'OBJECTDETECTOR', 'SLEEPDETECTOR']
    VoiceSystem(indices_list,student_name)
    indices_list = ['FACERECOGNITION', 'OBJECTDETECTOR']
    VoiceSystem(indices_list, student_name)


if __name__ == '__main__':
    for_tests_only()
