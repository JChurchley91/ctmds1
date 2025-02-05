import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from strategies.basic_generator import generate_random_numbers


def test_generate_random_numbers():
    """
    Test the generate_random_numbers function.
    Assert that random numbers are generated using the specified strategy.
    Assert that the number of random numbers generated is equal to the specified number count.
    """
    number_count = 100
    numbers = generate_random_numbers(number_count)

    assert numbers is not None
    assert len(numbers) == number_count
