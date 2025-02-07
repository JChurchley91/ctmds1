import random


def generate_random_numbers(count: int) -> list | str:
    """
    Generate a range of random numbers equal to the count param.
    Each number is a float between 0 and 100 rounded to 2 decimal places.
    Return the list of random numbers.

    :param count: Number of random numbers to generate
    :return: List of random numbers
    """
    random_numbers_list: list = []

    try:
        for x in range(count):
            random_number: float = round(random.uniform(0, 100), 2)
            random_numbers_list.append(random_number)

        return random_numbers_list

    except TypeError:
        return "please ensure the count is an integer"
