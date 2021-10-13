import config
from Services import loggerService as ls
import yagmail


class EmailSystem:

    def __init__(self):
        """
        init the email & password & port of the sender
        """
        self.__sender = config.EMAIL['EMAIL']
        self.__password = config.EMAIL['PASSWORD']
        # initializing the server connection
        self.__yag = yagmail.SMTP(user=self.__sender, password=self.__password)
        self.__success = False

    def send_email(self, subject, msg, recipient_email):
        """
        send the email to the recipient address.
        :param: msg: the msg to the recipient
        :param: recipient_email: the email address of the recipient
        :param: subject: the subject of the email
        :return: self.success: bool param to update if we succeed
        to send the email
        """
        try:
            # sending the email
            self.__yag.send(to=recipient_email, subject=subject, contents=msg)
            self.__success = True
            print("Email sent successfully!") if config.DEBUG else None
        except ValueError as v:
            ls.get_logger().error(str(v))
        except Exception as e:
            ls.get_logger().error(f'failed to send the email, due to: {str(e)}')
        return self.__success


def for_tests_only():
    """
    A test func to this page only.
    """
    x = EmailSystem()
    subject = 'Python Email Test'
    message = """\
    Subject: Python Email Test\n

    hi how are you.\n

    From Tests
    """
    x.send_email(subject, message, "rshalom8@gmail.com")


if __name__ == '__main__':
    for_tests_only()
