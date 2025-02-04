import sys
import os
import pytest
import typer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import validate_strategy, import_strategy_module


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


def test_import_strategy_module():
    """
    Test the import_strategy_module function.
    Assert that the function returns the correct module for valid strategies.
    Assert that the function raises a typer.Exit exception for invalid strategies.
    """
    assert import_strategy_module("basic_generator") is not None
    assert import_strategy_module("numpy_generator") is not None

    with pytest.raises(typer.Exit) as error:
        import_strategy_module("invalid_strategy")
        assert error.value.exit_code == 1
