from time import sleep

import config
from Measurements import abstractMeasurement as am
from Services import loggerService
from Core.lessonConfiguration import LessonConfiguration as lc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class SoundCheck(am.AbstractMeasurement):

    def __init__(self):
        """
        initialize the parent class and set up volume and lesson configuration.
        """
        am.AbstractMeasurement.__init__(self)
        self.volume = self.init_volume()
        self.min_sound_level = config.SOUND_CHECK['min_volume']
        self.is_active_lesson = True
        lesson = lc.get_lesson()
        if lesson:
            self.is_active_lesson = lesson['isActive']


    def init_volume(self):
        """
        initialize the volume object
        :return: the volume object
        """
        # get default audio device using PyCAW
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))

    def run(self, frame, dict_results):
        """
        run the sound check - check if the sound is on and loud enough to ear the lesson.
        :param frame: frame to process - not in use here just to follow interface structure.
        :param dict_results: a dictionary which the result will be put there
        :return: pair of key = 'sound_check', value = True if the computer's sound is on and loud and False otherwise.
            """
        try:
            run_result = {repr(self): True}

            # decide whether it is mute or not, mute is 1 for mute, 0 for not mute
            is_mute = self.volume.GetMute()

            # get the volume value, 0.0 means minimum, 1.0 means maximum
            current_volume = self.volume.GetMasterVolumeLevelScalar()
            if config.DEBUG:
                print("is mute: ",is_mute)
                print("current volume level: ",current_volume)

            if is_mute or current_volume < self.min_sound_level:
                run_result[repr(self)] = False
                # if it's an active lesson, then should open up the volume to expected level
                if self.is_active_lesson:
                    # if it's on mute - set mute to False
                    if is_mute:
                        self.volume.SetMute(False,None)

                    # if the volume is lower then expected - increase the volume to the expected level
                    if current_volume < self.min_sound_level:
                        self.volume.SetMasterVolumeLevelScalar(self.min_sound_level + 0.01, None)

                    if config.DEBUG:
                        print("volume is up. volume level: ", self.volume.GetMasterVolumeLevelScalar())

        except Exception as e:
            # write error to log file
            loggerService.get_logger().error(str(e))
        finally:
            dict_results.update(run_result)

    def __repr__(self):
        return 'SoundCheck'


if __name__ == "__main__":
    while True:
        dict_results = {}
        SoundCheck().run(None, dict_results)
        print(dict_results)
        sleep(5)
