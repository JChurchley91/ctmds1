import pytz

from datetime import datetime, timedelta


def get_hours_in_day(date: datetime, timezone_str: str = "UTC") -> int:
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


def get_season(date: datetime) -> str:
    """
    Determine the season for a given date.

    :param date: The date to determine the season for
    :return: The season as a string ('spring', 'summer', 'autumn', 'winter')
    """
    year = date.year
    seasons = {
        "spring": (datetime(year, 3, 20), datetime(year, 6, 20)),
        "summer": (datetime(year, 6, 21), datetime(year, 9, 22)),
        "autumn": (datetime(year, 9, 23), datetime(year, 12, 20)),
        "winter": (datetime(year, 12, 21), datetime(year + 1, 3, 19)),
    }

    for season, (start, end) in seasons.items():
        if start <= date <= end:
            return season


def model_seasonality(season: str, commodity: str) -> float:
    """
    Model seasonality for a given commodity and season.

    :param commodity: The commodity to model seasonality for
    :param season: The season to model seasonality for
    :return: The seasonality factor
    """
    seasonality_factors = {
        "power": {
            "spring": 0.5,
            "summer": 1.5,
            "autumn": 0.5,
            "winter": 1.5,
        },
        "natural_gas": {
            "spring": 0.8,
            "summer": 0.5,
            "autumn": 1.0,
            "winter": 1.5,
        },
        "crude": {
            "spring": 0.8,
            "summer": 1.0,
            "autumn": 1.2,
            "winter": 1.5,
        },
    }

    return seasonality_factors[commodity][season]


def model_peak_hours(season: str, commodity: str) -> list[int]:
    """
    Model peak hours for a given date.

    :param season: The season to model peak hours for
    :param commodity: The commodity to model peak hours for

    :return: A list of peak hours
    """
    peak_hours = {
        "spring": {
            "power": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            "natural_gas": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "crude": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        },
        "summer": {
            "power": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "natural_gas": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            "crude": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        },
        "autumn": {
            "power": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            "natural_gas": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "crude": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        },
        "winter": {
            "power": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            "natural_gas": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "crude": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        },
    }

    return peak_hours[season][commodity]


def model_off_peak_hours(season: str, commodity: str) -> list[int]:
    """
    Model off-peak hours for a given date.

    :param season: The season to model off-peak hours for
    :param commodity: The commodity to model off-peak hours for
    :return: A list of off-peak hours
    """
    peak_hours = model_peak_hours(season, commodity)
    hours_in_day = 24
    off_peak_hours = [hour for hour in range(hours_in_day) if hour not in peak_hours]
    return off_peak_hours
