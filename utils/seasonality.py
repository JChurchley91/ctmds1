from datetime import datetime


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
