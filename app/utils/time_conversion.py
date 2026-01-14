from datetime import datetime



def _time_str(time_str):
    """
    Convert time to string format
    :param time_str:
    :return:
    """
    return datetime.strftime(time_str, "%Y-%m-%d %H:%M%S")


def _str_time(time_str):
    """
    Convert string to time format
    :param time_str:
    :return:
    """
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M%S")