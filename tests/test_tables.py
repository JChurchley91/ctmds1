import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.tables import CountryCodes, Granularity, Commodity


def test_country_codes():
    """
    Test the country codes enum.
    Assert that the CountryCodes Enum class returns a valid int for each country code.
    Assert that the enum also returns a Polars DataFrame containing the correct size df.
    :return: None
    """
    assert type(CountryCodes.get_price("GB")) == int
    assert type(CountryCodes.get_price("FR")) == int
    assert type(CountryCodes.get_price("NL")) == int
    assert type(CountryCodes.get_price("DE")) == int
    assert CountryCodes.return_as_df().shape[0] == 4


def test_granularity():
    """
    Test the granularity enum.
    Assert that the Granularity Enum class returns the correct granularities.
    Assert that the enum also returns a Polars DataFrame containing the correct size df.
    :return: None
    """
    assert Granularity.h == "h"
    assert Granularity.hh == "hh"
    assert Granularity.return_as_df().shape[0] == 2


def test_commodity():
    """
    Test the commodity enum.
    Assert that the Commodity Enum class returns the correct commodities.
    Assert that the enum also returns a Polars DataFrame containing the correct size df.
    :return: None
    """
    assert Commodity.power == "power"
    assert Commodity.natural_gas == "natural_gas"
    assert Commodity.crude == "crude"
    assert Commodity.return_as_df().shape[0] == 3
