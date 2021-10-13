import psutil
import cv2
import config
from Services import httpService, loggerService
from Measurements.soundCheck import SoundCheck as sc


def get_program(program):
    """
    get program details such as: name, status etc..
    :param program: program to get
    :return: instance of program details if the program is installed and None otherwise
    """
    for p in psutil.process_iter():
        try:
            if p.name().lower() == program.lower():
                return p
        except psutil.ZombieProcess:
            continue
        except psutil.NoSuchProcess:
            continue

    return None


def check_is_alive():
    """
    check if the server is alive and respond.
    :return: pair of test kind and True or False if the test was success or failure.
    """
    is_alive = httpService.head(config.URLS['is_server_alive'])
    loggerService.get_logger().info(f'is server alive = {is_alive}')
    return {'is_server_alive': is_alive}


def check_camera_source():
    """
    check if able to read from camera by the configured CAM_SRC, if was not able to read,
    try a range of numbers [0-10] and configure the new source if was success.
    :return: pair of test kind and True or False if the test was success or failure.
    """
    success_msg = 'read from camera source was success. source value = {cam_src}'
    failure_msg = 'read from camera source failed. source value = {cam_src}'
    res_key = 'camera_source'

    result = True

    # at first, try to read camera by CAM_SRC value
    capture_device = cv2.VideoCapture(config.CAM_SRC, cv2.CAP_DSHOW)
    ret, frame = capture_device.read()

    if not ret:
        # try each one of the values in range [0-10] until reading success
        for i in range(0, 11):
            capture_device = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            ret, frame = capture_device.read()
            if ret:
                # set CAM_SRC to be i from now on
                config.CAM_SRC = i
                break
        else:
            result = False
            loggerService.get_logger().fatal(failure_msg.format(cam_src=config.CAM_SRC))

    capture_device.release()
    cv2.destroyAllWindows()

    if result:
        loggerService.get_logger().info(success_msg.format(cam_src=config.CAM_SRC))

    return {res_key: result}


def check_if_program_installed(program_name):
    """
    check if a given program is install on the computer.
    :param program_name: the name if the program
    :return: True if the program installed and False otherwise.
    """
    try:
        if not config.PREREQUISITE_INSTALLATIONS[program_name]:
            raise ValueError(f"cannot find program: {program_name} in config")
        result = (get_program(config.PREREQUISITE_INSTALLATIONS[program_name]) is not None)
        loggerService.get_logger().info(f'is {program_name} installed = {result}')
    except ValueError as e:
        loggerService.get_logger().error(str(e))
        result = False
    except Exception as e:
        loggerService.get_logger().error(
            f'exception has occurred , due to: {str(e)}')
        result = False
    finally:
        return {f'is_{program_name}_installed': result}

def check_if_process_is_running(process_name):
    """
    check if a given process is currently running.
    :param process_name: the name of the process.
    :return: True if the process is running and False otherwise.
    """
    try:
        if not config.PREREQUISITE_INSTALLATIONS[process_name]:
            raise ValueError(f"cannot find process: {process_name} in config")
        p = get_program(config.PREREQUISITE_PROCESSES[process_name])
        loggerService.get_logger().info(f'{process_name} status: {p.status()}')
        result = (p.status() == 'running')
    except ValueError as e:
        loggerService.get_logger().error(str(e))
        result = False
    except Exception as e:
        loggerService.get_logger().error(
            f'exception has occurred , due to: {str(e)}')
        result = False
    finally:
        return {f'is_{process_name}_running': result}

def check_if_sound_is_ok():
    """
    check if a the sound is not on mute and the sound level at least in minimum level.
    :return: True if the sound is ok and False otherwise.
    """
    try:
        result = {}
        sound_check = sc()
        sound_check.run(None,result)
        is_sound_ok = result[repr(sound_check)]
        loggerService.get_logger().info(f'is sound ok: {is_sound_ok}')
    except ValueError as e:
        loggerService.get_logger().error(str(e))
        is_sound_ok = False
    except Exception as e:
        loggerService.get_logger().error(
            f'exception has occurred , due to: {str(e)}')
        is_sound_ok = False
    finally:
        return {f'is_sound_ok': is_sound_ok}




def run_health_checks():
    """
    run all the health checks needed for the application to run
    :return: list of pairs which the key is the health check name and value True or False
    depending the health check result.
    """
    health_checks = [check_is_alive, check_camera_source, check_if_sound_is_ok]
    results = []

    try:
        # iterate over prerequisite installations and check if each one of them is installed
        for key in config.PREREQUISITE_INSTALLATIONS.keys():
            results.append(check_if_program_installed(key))

        # iterate over prerequisite processes and check if each one of them is currently running
        for key in config.PREREQUISITE_PROCESSES.keys():
            results.append(check_if_process_is_running(key))

        # iterate over the health checks, call it and append its result to results array
        for health_check in health_checks:
            results.append(health_check())
    except Exception as e:
        loggerService.get_logger().error(f'run_health_checks - an error occurred: {str(e)}')

    return results


if __name__ == "__main__":
    print(run_health_checks())
