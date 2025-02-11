from datetime import datetime
from utils.seasonality import get_season, model_seasonality


def test_get_season():
    """
    Test the get_season function
    Assert that the function returns the correct season for a given date.
    """
    date = datetime(2022, 3, 21)
    assert get_season(date) == "spring"

    date = datetime(2022, 6, 21)
    assert get_season(date) == "summer"

    date = datetime(2022, 9, 23)
    assert get_season(date) == "autumn"

    date = datetime(2022, 12, 21)
    assert get_season(date) == "winter"


def test_model_seasonality():
    """
    Test the model_seasonality function
    Assert that the function returns the correct seasonality factor for a given commodity and season.
    """
    assert model_seasonality("power", "summer") == 1.5
    assert model_seasonality("natural_gas", "spring") == 0.8
    assert model_seasonality("crude", "winter") == 1.5
