from datetime import datetime


def convert_datetime_to_iso(datetime_obj):
    """
    convert a given datetime object to string iso format
    :param datetime_obj: datetime object to convert
    :return: iso format (string) of the given datetime
    """
    if datetime_obj is None:
        return None
    return datetime_obj.isoformat() + 'Z'


def convert_iso_format_to_datetime(iso_format_str):
    """
    convert a given iso format string to datetime object
    :param iso_format_str: iso format in string to convert
    :return: datetime object represent the given iso format
    """
    if iso_format_str is None:
        return None
    return datetime.fromisoformat(iso_format_str.split('.')[0])


def compare_dates_by_time(date1, date2):
    """
    compare dates only by time regardless of the day, month, year
    :param date1: first date
    :param date2: second date
    :return: whether date1 is smaller than date2
    """
    return date2.hour > date1.hour or (date2.hour == date1.hour and date2.minute > date1.minute)\
           or (date2.hour == date1.hour and date2.minute == date1.minute and date2.second > date1.second)