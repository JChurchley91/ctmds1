import datetime


def log_generation_time(
    start_time: datetime.datetime, finish_time: datetime.datetime
) -> datetime.timedelta | str:
    """
    Log the time it takes to generate random numbers.
    Receives a start time and a finish time and calculates the difference.

    :param start_time: Start time
    :param finish_time: Finish time
    :return: difference between finish and start time
    """
    try:
        time_difference: datetime.timedelta = finish_time - start_time

    except TypeError:
        return "please ensure both times are datetime objects"

    return time_difference
