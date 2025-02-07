from enum import Enum


class Strategies(str, Enum):
    """
    Enum class for the different strategies available to generate random numbers.
    """

    basic = "basic_generator"
    numpy = "numpy_generator"
    prices = "price_generator"


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


class Granularity(str, Enum):
    h = "h"
    hh = "hh"
