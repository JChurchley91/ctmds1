import numpy as np
import pytz

from datetime import datetime, timedelta
from numpy import ndarray
from options import CountryCodes
from utils.seasonality import (
    get_season,
    model_seasonality,
    model_peak_hours,
    model_off_peak_hours,
)


def hours_in_day(date: datetime, timezone_str: str = "UTC") -> int:
    """
    Return the number of hours in a day for the specified date and timezone.

    :param date: the date to calculate the number of hours in a day for
    :param timezone_str: the timezone to calculate the number of hours in a day for
    :return: an int representing the number of hours in a given day
    """
    tz = pytz.timezone(timezone_str)

    if isinstance(date, datetime):
        date = date.date()

    day_start = datetime(date.year, date.month, date.day)
    next_day = day_start + timedelta(days=1)

    day_start = tz.localize(day_start)
    day_start = tz.normalize(day_start)

    next_day = tz.localize(next_day)
    next_day = tz.normalize(next_day)

    difference = next_day - day_start
    hours = difference.total_seconds() / 3600

    return int(hours)


def generate_prices(
    for_date: datetime, country_code: str, granularity: str, commodity: str
) -> np.ndarray[float]:
    """
    Return hourly prices for the specified date and country code.
    Maps the country_code param to COUNTRY_CODE_PRICES dictionary to return a base price.
    Uses the base price as a starting point to generate hourly prices for the specified date.
    Uses the seasonality factor and peak hours to adjust the prices accordingly.

    :param for_date: the date to return hourly prices for
    :param country_code: the country code of the country to return hourly prices for
    :param granularity: the granularity of the prices to be returned
    :param commodity: the commodity to return prices for
    :return: None
    """

    base_price = CountryCodes.get_price(country_code)
    season = get_season(for_date)
    seasonality_factor = model_seasonality(season, commodity)
    peak_hours = model_peak_hours(season, commodity)
    off_peak_hours = model_off_peak_hours(season, commodity)
    hours_in_for_date = hours_in_day(for_date, "Europe/London")

    if granularity == "h":
        prices: ndarray = np.random.normal(
            loc=base_price * seasonality_factor, scale=5, size=hours_in_for_date
        )
        prices[peak_hours] += 20
        prices[off_peak_hours] -= 40
        return np.round(prices, 2)

    if granularity == "hh":
        prices: ndarray = np.random.normal(
            loc=base_price, scale=5, size=(hours_in_for_date * 2)
        )
        prices[peak_hours] += 20
        prices[off_peak_hours] -= 40
        return np.round(prices, 2)
    else:
        raise ValueError(f"Invalid granularity: {granularity}. Program will exit.")
