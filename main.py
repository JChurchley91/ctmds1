import typer
import importlib
import datetime

from typing_extensions import Annotated
from utils.timer import log_generation_time
from utils.validations import (
    validate_strategy,
    validate_country_code,
    validate_granularity,
    validate_for_date,
)

app = typer.Typer()


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
        str, typer.Option(help="The strategy to use when generating random numbers")
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

    if validate_strategy(strategy_name):
        try:
            strategy_module = import_strategy_module(strategy_name)
            start_time = datetime.datetime.now()
            strategy_module.generate_random_numbers(number_count)
            finish_time = datetime.datetime.now()
            time_difference = log_generation_time(start_time, finish_time)
            typer.echo(
                f"{number_count} numbers generated in {time_difference} seconds."
            )

        except Exception as error:
            typer.echo(f"Error generating random numbers: {error}. Program will exit.")
            raise typer.Exit(code=1)


@app.command()
def model_prices(
    for_date: Annotated[
        datetime.datetime, typer.Option(help="The date in which to return prices for")
    ],
    country_code: Annotated[
        str, typer.Option(help="The country code of the country to return prices for")
    ],
    granularity: Annotated[str, typer.Option(help="The granularity of the prices")],
) -> None:
    """
    Return prices for the specified date, country code, and granularity.

    :param for_date: the date to model prices for
    :param country_code: the country code of the country to model prices for
    :param granularity: the granularity of the prices
    :return: None
    """
    if (
        validate_for_date(for_date)
        and validate_country_code(country_code)
        and validate_granularity(granularity)
    ):
        try:
            strategy_module = import_strategy_module("price_generator")
            prices = strategy_module.generate_prices(
                for_date, country_code, granularity
            )
            typer.echo(f"Prices for {for_date} in {country_code} ({granularity}):")
            for index, price in enumerate(prices):
                typer.echo(f"Observation {index + 1}: {price}")

        except Exception as error:
            typer.echo(f"Error modeling prices: {error}. Program will exit.")
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
