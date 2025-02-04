# Random Number Generator

This project is a command-line application for generating random numbers using different strategies. It is built using Python and Typer.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To generate random numbers, use the `generate_random_numbers` command with the desired strategy and number count.

### Available Strategies

- `basic_generator`
- `numpy_generator`

### Command Syntax

```bash
python main.py generate-random-numbers <strategy_name> <number_count>
```

### Examples

Generate 10 random numbers using the basic_generator strategy:

```bash
python main.py generate-random-numbers basic_generator 10
```

Generate 20 random numbers using the numpy_generator strategy:

```bash
python main.py generate-random-numbers numpy_generator 20
```

### Testing

To run the tests, use the following command:

```bash
pytest
```

### Project Structure

The project has the following structure:

* main.py: The main application file containing the command-line interface and logic.
* strategies/: Directory containing the random number generation strategies.
    * strategies/basic_generator.py: A basic random number generator strategy.
    * strategies/numpy_generator.py: A random number generator strategy using NumPy.
* utils/timer.py: Utility functions for logging generation time.
* tests/: Directory containing test files.