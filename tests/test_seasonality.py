from datetime import datetime
from utils.seasonality import (
    get_season,
    model_seasonality,
    model_peak_hours,
    model_off_peak_hours,
)


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
    assert (
        model_seasonality(
            "summer",
            "power",
        )
        == 1.5
    )
    assert model_seasonality("spring", "natural_gas") == 0.8
    assert model_seasonality("winter", "crude") == 1.5


def test_model_peak_hours():
    """
    Test the model_peak_hours function
    Assert that the function returns the correct peak hours for a given season and commodity.
    """
    assert model_peak_hours("summer", "power") == [
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
    ]
    assert model_peak_hours("winter", "natural_gas") == [
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
    ]
    assert model_peak_hours("autumn", "crude") == [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


def test_model_off_peak_hours():
    """
    Test the model_off_peak_hours function
    Assert that the function returns the correct off-peak hours for a given season and commodity.
    """
    summer_power_prices = model_off_peak_hours("summer", "power")

    for price in summer_power_prices:
        assert price not in [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    winter_natural_gas_prices = model_off_peak_hours("winter", "natural_gas")

    for price in winter_natural_gas_prices:
        assert price not in [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
