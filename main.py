import typer
import importlib
import datetime

from utils.timer import log_generation_time

STRATEGIES = ["basic_generator", "numpy_generator"]
app = typer.Typer()


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
def generate_random_numbers(strategy_name: str, number_count: int) -> None:
    """
    Generate random numbers using the specified strategy.

    :param strategy_name:
    :param number_count:
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


if __name__ == "__main__":
    app()
