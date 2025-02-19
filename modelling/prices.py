import numpy as np
import polars
import datetime

from numpy import ndarray
from db.utils import return_duckdb_conn, select_duckdb_table
from modelling.seasonality import (
    get_hours_in_day,
    get_season,
    model_seasonality,
    model_peak_hours,
    model_off_peak_hours,
)


def get_base_price(country_code: str) -> int:
    """
    Select the base prices from config.country_codes table.
    Filter the base prices based on the country_code param.

    :return: dict
    """
    conn = return_duckdb_conn("price_data.db")
    df = select_duckdb_table(conn, "config", "country_codes")
    base_price = (
        df.filter(polars.col("country_code") == country_code)
        .select("country_base_price")
        .to_series()
        .to_list()[0]
    )
    return base_price


def model_daily_prices(
    for_date: datetime.datetime,
    country_code: str,
    granularity: str,
    commodity: str,
) -> np.ndarray[float]:
    """
    Return hourly prices for the specified date and country code.
    Maps the country_code param to COUNTRY_CODE_PRICES dictionary to return a base price.
    Uses the base price as a starting point to generate hourly prices for the specified date.
    Uses the seasonality factor and peak hours to adjust the prices accordingly.

    :param for_date: the date to return hourly prices for
    :param country_code: the country code of the country to return hourly prices for
    :param granularity: the granularity of the prices to be returned
    :param commodity: the commodity to return prices for
    :return: None
    """
    base_price = get_base_price(country_code)
    season = get_season(for_date)
    seasonality_factor = model_seasonality(season, commodity)
    peak_hours = model_peak_hours(season, commodity)
    off_peak_hours = model_off_peak_hours(season, commodity)
    hours_in_for_date = get_hours_in_day(for_date, "Europe/London")

    if granularity == "h":
        prices: ndarray = np.random.normal(
            loc=base_price * seasonality_factor, scale=5, size=hours_in_for_date
        )
        prices[peak_hours] += 20
        prices[off_peak_hours] -= 40
        prices = np.round(prices, 2)
        return prices

    if granularity == "hh":
        prices: ndarray = np.random.normal(
            loc=base_price, scale=5, size=(hours_in_for_date * 2)
        )
        prices[peak_hours] += 20
        prices[off_peak_hours] -= 40
        prices = np.round(prices, 2)
        return prices
    else:
        raise ValueError(f"Invalid granularity: {granularity}. Program will exit.")
