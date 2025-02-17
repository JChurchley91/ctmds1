import importlib

from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from db.tables import Strategies, CountryCodes, Granularity, Commodity
from db.db_utils import (
    create_duckdb_db,
    return_duckdb_conn,
    create_config_schema,
    create_config_tables,
)


def import_strategy_module(strategy_name: str):
    try:
        return importlib.import_module(f"strategies.{strategy_name}")
    except ImportError as error:
        raise HTTPException(status_code=500, detail=str(error))


def lifespan(fast_api: FastAPI):
    fast_api.title = "Price Data API"
    initialise_database()
    yield


app = FastAPI(lifespan=lifespan)


class GeneratePricesRequest(BaseModel):
    for_date: datetime
    country_code: CountryCodes
    granularity: Granularity
    commodity: Commodity


def initialise_database(db_name: str = "price_data.db") -> None:
    try:
        create_duckdb_db(db_name)
        conn = return_duckdb_conn(db_name)
        create_config_schema(conn)
        create_config_tables(conn)
        print(f"{db_name} initialised - schema and tables created.")
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/generate-random-numbers")
def generate_random_numbers(strategy_name: Strategies, number_count: int):
    try:
        strategy_module = import_strategy_module(strategy_name.value)
        numbers = strategy_module.generate_random_numbers(number_count)
        return {"random numbers: ": numbers}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/model-prices")
def model_prices(request: GeneratePricesRequest):
    strategy_module = import_strategy_module("price_generator")
    prices = strategy_module.generate_prices(
        request.for_date,
        request.country_code,
        request.granularity,
        request.commodity,
    )
    return {
        "commodity": request.commodity.value,
        "date": request.for_date.date(),
        "country_code": request.country_code.value,
        "granularity": request.granularity.value,
        "prices": prices.tolist(),
    }
