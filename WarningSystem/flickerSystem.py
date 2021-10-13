import time
import config
import screen_brightness_control as sbc


class FlickerSystem:

    def __init__(self):
        """
        init time interval & run the system
        """
        self.__interval = 0.10
        self.__run_flicker_system()

    def __run_flicker_system(self):
        """
        run the system for about ten seconds
        """
        start = time.time()
        while self.__interval > 0:
            # Fade the brightness from 100% to 0% with time intervals of 0.01 seconds.
            sbc.fade_brightness(0, start=100, interval=0.01, blocking=True)
            # Increase the brightness from 0% to 100% with time intervals of 0.01 seconds.
            sbc.fade_brightness(100, start=0, interval=0.01, blocking=True)
            self.__interval -= 0.10
        sbc.set_brightness(99)
        end = time.time()
        if config.DEBUG:
            print('Flicker System interpolation took {:.2f} seconds'.format(end - start))


def for_tests_only():
    """
    A test func to this page only.
    """
    FlickerSystem()


if __name__ == '__main__':
    for_tests_only()

