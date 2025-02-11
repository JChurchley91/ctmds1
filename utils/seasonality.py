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

def model_seasonality(commodity: str, season: str) -> float:
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