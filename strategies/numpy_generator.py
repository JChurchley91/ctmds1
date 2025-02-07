import numpy as np


def generate_random_numbers(count: int) -> np.ndarray[float] | str:
    """
    Generate a range of random numbers equal to the count param.
    Each number is a float between 0 and 100 rounded to 2 decimal places.
    Return the list of random numbers.

    :param count: Number of random numbers to generate
    :return: List of random numbers
    """

    try:
        random_numbers: np.ndarray = np.random.uniform(0, 100, count)
        return np.round(random_numbers, 2)

    except TypeError:
        return "please ensure the count is an integer"
