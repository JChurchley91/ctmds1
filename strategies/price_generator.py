import numpy as np
from numpy import ndarray

COUNTRY_CODE_PRICES: dict = {"GB": 61, "FR": 58, "NL": 52, "DE": 57}


def generate_prices(country_code: str, granularity: str) -> None:
    """
    Return hourly prices for the specified date and country code.
    Maps the country_code param to COUNTRY_CODE_PRICES dictionary to return a base price.
    Uses the base price as a starting point to generate hourly prices for the specified date.

    :param country_code: the country code of the country to return hourly prices for
    :param granularity: the granularity of the prices to be returned
    :return: None
    """
    base_price = COUNTRY_CODE_PRICES[country_code]

    if granularity == "h":
        prices: ndarray = np.random.normal(loc=base_price, scale=5, size=24)
        return prices
    if granularity == "hh":
        prices: ndarray = np.random.normal(loc=base_price, scale=5, size=48)
        return prices
    else:
        raise ValueError(f"Invalid granularity: {granularity}. Program will exit.")
