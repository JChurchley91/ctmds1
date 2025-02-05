import sys
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from strategies.price_generator import hours_in_day, generate_prices


def test_hours_in_day():
    """
    Test the hours_in_day function.
    Assert that 24 hours are returned for a specified date - 2025-29-03.
    Assert that 23 hours are returned for a specified date - 2025-30-03.
    """
    date_1 = datetime.datetime(2025, 3, 29, 0, 0, 0)
    date_2 = datetime.datetime(2025, 3, 30, 0, 0, 0)

    assert hours_in_day(date_1, "Europe/London") == 24
    assert hours_in_day(date_2, "Europe/London") == 23


def test_generate_prices():
    """
    Test the generate_prices function.
    Assert that prices are generated for a specified date, country code, and granularity.
    Assert that the number of prices returned is 24 for granularity 'h' and 48 for granularity 'hh'.
    """
    date = datetime.datetime(2025, 3, 29, 0, 0, 0)
    country_code = "GB"
    granularity = "h"

    assert generate_prices(date, country_code, granularity) is not None
    assert len(generate_prices(date, country_code, granularity)) == 24

    granularity = "hh"

    assert generate_prices(date, country_code, granularity) is not None
    assert len(generate_prices(date, country_code, granularity)) == 48
