import config
from Core.studentManager import StudentManager
from Services import httpService


class MeasurementsService:
    """
    Measurements Service which will be responsible for sending the measurements data
    to the server even if there were an connection problems,
    it will keep the data until connection is back
    """

    def __init__(self):
        self.measurements_stack = []

    def post_measurements(self, measurements):
        """
        post measurements to the server and handle connection problems.
        :param measurements: measurements to send to the server
        :return: void
        """
        token = StudentManager.get_student()["token"]
        has_success = httpService.post(config.URLS['post_measures'], measurements.get_measurement_dto(), token)
        # if has success it means the connection eith the server is on
        if has_success:
            # if there is measurements to send
            if len(self.measurements_stack) > 0:
                # send all the stacked measurements to the matching API
                has_success = httpService.post(config.URLS['post_stacked_measures'], self.measurements_stack, token)
                # if has success can empty the stack
                if has_success:
                    self.measurements_stack = []
        else:
            # there is no connection so save it for later trial
            self.measurements_stack.append(measurements.get_measurement_dto())
