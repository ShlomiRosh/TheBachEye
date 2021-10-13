import config
from Services import healthChecksService as hcs
import sys
from EmailMessagingSystem import emailSystem as es


class HealthCheckPageController:

    def __init__(self):
        """
        init function for the status of the program and the health list.
        """
        self.__ready = True
        self.__health_list = health_list_tests() if config.DEBUG else hcs.run_health_checks()
        self.__health_dict = {}

    def get_health_map(self):
        """
        create a health map from the health list.
        :return: self.health_dict: health map for each component what is status
        """
        for i in range(len(self.__health_list)):
            val = self.__health_list[i]
            try:
                key = list(val.keys())[0].split('is_')[1].replace('_', ' ').upper()
            except:
                key = list(val.keys())[0].replace('_', ' ').upper()
            val = list(val.values())[0]
            self.__health_dict.update({key: val})
            print(val, key) if config.DEBUG else None
        return self.__health_dict

    def is_ready(self):
        """
        check if all health components are ready to run.
        :return: self.ready: a boolean indicating if the process is ready or not
        """
        for key, val in self.__health_dict.items():
            if not val:
                self.__ready = False
        return self.__ready


def send_email(message):
    """
    send us en email from the student if he failed in health
    checks and want to connect us.
    :param message: the message from the student
    """
    subject = 'Mail from student'
    msg = """\
                Student failed in our health check
                and send us the following email:

                """ + message + """

                -------------------------------

            Student To TheBackEye Team.
            """
    es.EmailSystem().send_email(subject, msg, config.EMAIL['EMAIL'])


def close_application():
    """
    if the student failed in health checks close the program.
    """
    # TODO - check for other things to be done and close
    sys.exit()


def health_list_tests():
    """
    function for tests.
    :return: a list that mimics the operation of the service get health.
    """
    return [{'is_zoom_installed': True}, {'is_manycam_installed': True},
            {'is_manycam_running': True}, {'is_alive': True}, {'camera_source': True},
            {'is_sound_ok': True}]


if __name__ == '__main__':
    x = HealthCheckPageController()
    x.get_health_map()
    print(x.is_ready())
