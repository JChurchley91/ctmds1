import polars

from utils.logger import get_logger
from fastapi import FastAPI, HTTPException
from models.requests import GeneratePricesRequest
from models.responses import GeneratePricesResponse
from modelling.prices import model_daily_prices, build_daily_prices_df
from datetime import datetime
from db.utils import (
    create_duckdb_db,
    return_duckdb_conn,
    create_schemas,
    create_config_tables,
    select_duckdb_table,
    create_or_append_table_from_df,
)


def initialise_database(fast_api_app, db_name="price_data.db") -> None:  # noqa: F841
    """
    Initialise the database and set the FastAPI title.

    :param db_name: the name of the database to initialise.
    :param fast_api_app: The FastAPI instance
    :return: None
    """
    try:
        create_duckdb_db(db_name)
        conn = return_duckdb_conn(db_name)
        create_schemas(conn)
        create_config_tables(conn)
        logger.info(f"Database initialised - {db_name}")
        yield
        conn.close()
    except Exception as error:
        logger.error(f"Error initialising database - {error}")
        raise HTTPException(status_code=500, detail=str(error))


def get_historic_daily_price(
    for_date: datetime, country_code: str, granularity: str, commodity: str
) -> polars.DataFrame:
    """
    Check if a daily price entry exists in the daily_prices table.

    :param for_date: the date to check for
    :param country_code: the country code to check for
    :param granularity: the granularity to check for
    :param commodity: the commodity to check for
    :return: bool
    """
    conn = return_duckdb_conn("price_data.db")
    df = select_duckdb_table(conn, "prices", "daily_prices")
    df = df.filter(
        date=for_date,
        country_code=country_code,
        granularity=granularity,
        commodity=commodity,
    )
    return df if not df.is_empty() else polars.DataFrame()


logger = get_logger("daily-prices")
app = FastAPI(title="Price Data API", lifespan=initialise_database)


@app.post("/model-prices")
@logger.catch
def model_prices(request: GeneratePricesRequest) -> GeneratePricesResponse:
    """
    Return hourly prices for the specified date and country code.
    Maps the country_code param to COUNTRY_CODE_PRICES dictionary to return a base price.
    Uses the base price as a starting point to generate hourly prices for the specified date.
    Uses the seasonality factor and peak hours to adjust the prices accordingly.

    :param request: request containing the date, country code, granularity, and commodity
    :return: response containing the date, country code, granularity, commodity, and prices
    """
    logger.info(f"request: {request}")

    historic_price = get_historic_daily_price(
        request.for_date,
        request.country_code,
        request.granularity,
        request.commodity,
    )

    if not historic_price.is_empty():
        logger.info("historic_prices exist: returning historic prices")
        prices = historic_price.select("prices").to_series().to_list()[0]
        response = GeneratePricesResponse(
            commodity=request.commodity,
            date=request.for_date,
            country_code=request.country_code,
            granularity=request.granularity,
            prices=prices,
        )
    else:
        logger.info("historic_price does not exist - modelling price")
        prices = model_daily_prices(
            request.for_date,
            request.country_code,
            request.granularity,
            request.commodity,
        )
        response = GeneratePricesResponse(
            commodity=request.commodity,
            date=request.for_date,
            country_code=request.country_code,
            granularity=request.granularity,
            prices=prices.tolist(),
        )
        daily_price = build_daily_prices_df(response)
        logger.info("saving daily prices to database")
        conn = return_duckdb_conn("price_data.db")
        create_or_append_table_from_df(
            daily_price, "append", "prices", "daily_prices", conn
        )

    logger.info(f"response: {response}")
    return response.model_dump()
