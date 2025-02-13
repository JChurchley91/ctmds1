import typer
import importlib
import datetime

from typing_extensions import Annotated
from db.tables import Strategies, CountryCodes, Granularity, Commodity
from db.db_utils import (
    create_duckdb_db,
    return_duckdb_conn,
    create_config_schema,
    create_config_tables,
)
from utils.timer import log_generation_time

app = typer.Typer()


def initialise_database(db_name: str = "price_data.db") -> None:
    """
    Initialise the DuckDB database and create the config schema and tables.
    Note that tbe tables are overwritten each time this function is called.
    :param db_name: the name of the database to initialise.

    :return: None
    """
    try:
        create_duckdb_db(db_name)
        conn = return_duckdb_conn(db_name)
        create_config_schema(conn)
        create_config_tables(conn)
        return None
    except Exception as error:
        typer.echo(f"Error initialising database: {error}. Program will exit.")
        raise typer.Exit(code=1)


def import_strategy_module(strategy_name: str) -> importlib:
    """
    Import the strategy module based on the strategy name.

    :param strategy_name:
    :return: importlib
    """
    try:
        return importlib.import_module(f"strategies.{strategy_name}")
    except ImportError as error:
        typer.echo(f"Error importing strategy: {error}. Program will exit.")
        raise typer.Exit(code=1)


@app.command()
def generate_random_numbers(
    strategy_name: Annotated[
        Strategies,
        typer.Option(help="The strategy to use when generating random numbers"),
    ],
    number_count: Annotated[
        int, typer.Option(help="The number of random numbers to be generated")
    ],
) -> None:
    """
    Generate random numbers using the specified strategy.

    :param strategy_name: the strategy to use when generating random numbers
    :param number_count: the number of random numbers to be generated
    :return: None
    """
    try:
        strategy_module = import_strategy_module(strategy_name)
        start_time = datetime.datetime.now()
        strategy_module.generate_random_numbers(number_count)
        finish_time = datetime.datetime.now()
        time_difference = log_generation_time(start_time, finish_time)
        typer.echo(f"{number_count} numbers generated in {time_difference} seconds.")

    except Exception as error:
        typer.echo(f"Error generating random numbers: {error}. Program will exit.")
        raise typer.Exit(code=1)


@app.command()
def model_prices(
    for_date: Annotated[
        datetime.datetime, typer.Option(help="The date in which to return prices for")
    ],
    country_code: Annotated[
        CountryCodes,
        typer.Option(help="The country code of the country to return prices for"),
    ],
    granularity: Annotated[
        Granularity, typer.Option(help="The granularity of the prices to be returned")
    ],
    commodity: Annotated[
        Commodity, typer.Option(help="The commodity to return prices for")
    ],
) -> None:
    """
    Return prices for the specified date, country code, and granularity.

    :param for_date: the date to model prices for
    :param country_code: the country code of the country to model prices for
    :param granularity: the granularity of the prices
    :param commodity: the commodity to model prices for
    :return: None
    """
    strategy_module = import_strategy_module("price_generator")
    prices = strategy_module.generate_prices(
        for_date, country_code, granularity, commodity
    )

    typer.echo(
        f"{commodity.value} price data for {for_date.date()} in {country_code.value} ({granularity.value}):"
    )

    for index, price in enumerate(prices):
        if granularity == "h":
            time = for_date.replace(hour=index, minute=0, second=0, microsecond=0)
            typer.echo(f"{time.time()} - {price}")
        if granularity == "hh":
            time = for_date.replace(
                hour=index // 2,
                minute=(index % 2) * 30,
                second=0,
                microsecond=0,
            )
            typer.echo(f"{time.time()} - {price}")


if __name__ == "__main__":
    initialise_database()
    app()
