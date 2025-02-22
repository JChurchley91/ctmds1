# Price Data API

## Overview

The Price Data API is a FastAPI-based application that provides endpoints for modeling and retrieving daily prices for various commodities. The application uses DuckDB for data storage and Loguru for logging.

## Features

- Model daily prices for specified dates, country codes, granularities, and commodities.
- Retrieve historic daily prices from the database.
- Automatically save modeled prices to the database if they do not already exist.

## Requirements

- Python 3.11
- Docker
- GitHub Actions

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/jchurchley91/ctmds1.git
    cd ctmds1
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the FastAPI application:
    ```sh
    uvicorn main:app --reload
    ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints

- **POST /model-prices**: Model and retrieve daily prices for the specified date, country code, granularity, and commodity.

## Logging

Logs are stored in the `logs` directory with a filename format of `daily-prices-YYYY-MM-DD.log`. Logs are rotated and retained for 1 hour.

## Database

The application uses DuckDB for data storage. The database is initialized with the following steps:
- Create the database file.
- Create necessary schemas and configuration tables.

## GitHub Actions

### Workflows

- **run_tests.yml**: Runs tests on every push.
- **build_and_publish.yml**: Builds and publishes the Docker image to GitHub Container Registry on push to the `master` branch.

### Example Workflow Configuration

#### run_tests.yml

```yaml
name: run tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: pytest
