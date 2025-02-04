import sys
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.timer import log_generation_time


def test_log_generation_time() -> None:
    """
    Test the log_generation_time function.
    Assert that the function returns the correct time difference.
    """
    start_time = datetime.datetime(2023, 1, 1, 12, 0, 0)
    finish_time = datetime.datetime(2023, 1, 1, 12, 0, 5)
    time_difference = log_generation_time(start_time, finish_time)
    assert time_difference == datetime.timedelta(seconds=5)
