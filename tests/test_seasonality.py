import pytest

from datetime import datetime
from modelling.seasonality import get_season


@pytest.mark.order(6)
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
