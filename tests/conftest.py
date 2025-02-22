import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.utils import (
    create_duckdb_db,
    return_duckdb_conn,
    create_schemas,
    create_config_tables,
)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """
    Fixture to set up the database.
    """
    create_duckdb_db("test.db")
    conn = return_duckdb_conn("test.db")
    create_schemas(conn)
    create_config_tables(conn)
    print("yest")
    yield conn


@pytest.fixture(scope="session", autouse=True)
def teardown_session():
    """
    Teardown function to delete the test.db file after tests are done.
    """
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")
