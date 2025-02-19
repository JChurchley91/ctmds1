from utils.logger import get_logger
from fastapi import FastAPI, HTTPException
from models.requests import GeneratePricesRequest
from models.responses import GeneratePricesResponse
from modelling.prices import model_daily_prices
from db.utils import (
    create_duckdb_db,
    return_duckdb_conn,
    create_config_schema,
    create_config_tables,
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
        create_config_schema(conn)
        create_config_tables(conn)
        yield
    except Exception as error:
        logger.error(f"Error initialising database - {error}")
        raise HTTPException(status_code=500, detail=str(error))


logger = get_logger("daily-prices")
app = FastAPI(title="Price Data API", lifespan=initialise_database)


@app.post("/model-prices")
@logger.catch
def model_prices(request: GeneratePricesRequest) -> dict:
    """
    Return hourly prices for the specified date and country code.
    Maps the country_code param to COUNTRY_CODE_PRICES dictionary to return a base price.
    Uses the base price as a starting point to generate hourly prices for the specified date.
    Uses the seasonality factor and peak hours to adjust the prices accordingly.

    :param request: request containing the date, country code, granularity, and commodity
    :return: dict of hourly prices
    """
    prices = model_daily_prices(
        logger,
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
    return response.model_dump()
