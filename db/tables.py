from enum import Enum

import polars


class CountryCodes(str, Enum):
    """
    Enum class for the different country codes available.
    """

    GB = "GB"
    FR = "FR"
    NL = "NL"
    DE = "DE"

    @classmethod
    def get_price(cls, country_code: str) -> int:
        """
        Return the base price for the specified country code.

        :param country_code: the country code to get the base price for
        :return: base price for specified country code
        """
        price_mapping = {
            "GB": 61,
            "FR": 58,
            "NL": 52,
            "DE": 57,
        }

        return price_mapping[country_code]

    @classmethod
    def return_as_df(cls) -> polars.DataFrame:
        """
        Return a Polars DataFrame containing the available country codes.

        :return: Polars DataFrame
        """
        data = {
            "country_code": [country_code.value for country_code in cls],
            "country_base_price": [
                cls.get_price(country_code.value) for country_code in cls
            ],
        }
        df = polars.DataFrame(data)
        return df


class Granularity(str, Enum):
    h = "h"
    hh = "hh"

    @classmethod
    def return_as_df(cls) -> polars.DataFrame:
        """
        Return a Polars DataFrame containing the available granularities.

        :return: Polars DataFrame
        """
        data = {"granularity": [granularity.value for granularity in cls]}
        return polars.DataFrame(data)


class Commodity(str, Enum):
    power = "power"
    natural_gas = "natural_gas"
    crude = "crude"

    @classmethod
    def return_as_df(cls) -> polars.DataFrame:
        """
        Return a Polars DataFrame containing the available commodities.

        :return: Polars DataFrame
        """
        data = {"commodity": [commodity.value for commodity in cls]}
        df = polars.DataFrame(data)
        return df
