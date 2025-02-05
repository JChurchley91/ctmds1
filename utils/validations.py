import typer
import datetime

STRATEGIES: list = ["basic_generator", "numpy_generator", "price_generator"]
COUNTRY_CODE_PRICES: dict = {"GB": 61, "FR": 58, "NL": 52, "DE": 57}
GRANULARITY: list = ["h", "hh"]


def validate_strategy(strategy_name: str) -> bool:
    """
    Validate the strategy name.

    :param strategy_name:
    :return: bool
    """
    if strategy_name in STRATEGIES:
        return True
    else:
        typer.echo(f"Invalid strategy: {strategy_name}. Program will exit.")
        raise typer.Exit(code=1)


def validate_country_code(country_code: str) -> bool:
    """
    Validate the country code.

    :param country_code:
    :return: bool
    """
    if country_code in COUNTRY_CODE_PRICES.keys():
        return True
    else:
        typer.echo(f"Invalid country code: {country_code}. Program will exit.")
        raise typer.Exit(code=1)


def validate_granularity(granularity: str) -> bool:
    """
    Validate the granularity.

    :param granularity:
    :return: bool
    """
    if granularity in GRANULARITY:
        return True
    else:
        typer.echo(f"Invalid granularity: {granularity}. Program will exit.")
        raise typer.Exit(code=1)


def validate_for_date(for_date: datetime.datetime) -> bool:
    """
    Validate the for_date.
    Return True if for_date is a datetime object, otherwise return False.

    :param for_date:
    :return: bool
    """
    if isinstance(for_date, datetime.datetime):
        return True
    else:
        typer.echo(f"Invalid for_date: {for_date}. Program will exit.")
        raise typer.Exit(code=1)
