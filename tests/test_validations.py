import sys
import os
import pytest
import typer
import datetime

from main import import_strategy_module

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.validations import (
    validate_strategy,
    validate_country_code,
    validate_granularity,
    validate_for_date,
)


def test_validate_strategy():
    """
    Test the validate_strategy function.
    Assert that the function returns True for valid strategies.
    Assert that the function raises a typer.Exit exception for invalid strategies.
    """
    assert validate_strategy("basic_generator") == True
    assert validate_strategy("numpy_generator") == True

    with pytest.raises(typer.Exit) as error:
        import_strategy_module("invalid_strategy")
        assert error.value.exit_code == 1


def test_validate_country_code():
    """
    Test the validate_country_code function.
    Assert that the function returns True for valid country codes.
    Assert that the function raises a typer.Exit exception for invalid country codes.
    """
    assert validate_country_code("GB") == True
    assert validate_country_code("FR") == True

    with pytest.raises(typer.Exit) as error:
        validate_country_code("invalid_country_code")
        assert error.value.exit_code == 1


def test_validate_granularity():
    """
    Test the validate_granularity function.
    Assert that the function returns True for valid granularities.
    Assert that the function raises a typer.Exit exception for invalid granularities.
    """
    assert validate_granularity("h") == True
    assert validate_granularity("hh") == True

    with pytest.raises(typer.Exit) as error:
        validate_granularity("invalid_granularity")
        assert error.value.exit_code == 1


def test_validate_for_date():
    """
    Test the validate_for_date function.
    Assert that the function returns True for valid dates.
    Assert that the function returns False for invalid dates.
    """
    assert validate_for_date(datetime.datetime.now()) == True

    with pytest.raises(typer.Exit) as error:
        validate_for_date("invalid_date")
        assert error.value.exit_code == 1
