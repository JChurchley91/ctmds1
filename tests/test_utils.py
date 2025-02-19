import sys
import os
import polars
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.utils import (
    create_duckdb_db,
    return_duckdb_conn,
    create_schemas,
    create_or_append_table_from_df,
    select_duckdb_table,
    check_table_exists,
    create_config_tables
)


@pytest.fixture(scope="session", autouse=True)
def teardown_session():
    """
    Teardown function to delete the test.db file after tests are done.
    """
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")


def test_create_duckdb_db():
    """
    Test the create_duckdb_db function.
    Assert that the function creates a DuckDB database.
    """
    conn = create_duckdb_db("test.db")
    assert conn is True


def test_return_duckdb_conn():
    """
    Test the return_duckdb_conn function.
    Assert that the function returns a DuckDB connection.
    """
    conn = return_duckdb_conn("test.db")
    assert conn is not None


def test_create_schemas():
    """
    Test the create_config_schema function.
    Select 1 if the config schema exists in the DuckDB database.
    Assert that the function creates the config schema in the DuckDB database.
    """
    conn = return_duckdb_conn("test.db")
    create_schemas(conn)
    schema_exists = conn.sql(
        "SELECT 1 FROM information_schema.schemata WHERE schema_name = 'config'"
    ).fetchone()
    assert schema_exists == (1,)


def test_create_or_append_table_from_df():
    """
    Test the create_table_from_df function.
    Create a Polars DataFrame with a single column.
    Create a table from the Polars DataFrame.
    Assert that the table is created in the DuckDB database.
    """
    conn = return_duckdb_conn("test.db")
    df = polars.DataFrame({"col1": [1, 2, 3]})
    create_or_append_table_from_df(df, "create", "config", "test_table", conn)
    table_exists = conn.sql(
        "SELECT 1 FROM information_schema.tables WHERE table_name = 'test_table'"
    ).fetchone()
    assert table_exists == (1,)


def test_select_duckdb_table():
    """
    Test the select_duckdb_table function.
    Create a Polars DataFrame with a single column.
    Create a table from the Polars DataFrame.
    Select all rows from the table.
    Assert that the function returns the correct number of rows.
    """
    conn = return_duckdb_conn("test.db")
    df = polars.DataFrame({"col1": [1, 2, 3]})
    create_or_append_table_from_df(df, "create", "config", "test_table", conn)
    selected_df = select_duckdb_table(conn, "config", "test_table")
    assert selected_df.shape[0] == 3

def test_check_table_exists():
    """
    Test the check_table_exists function.
    Create a table in the DuckDB database.
    Check if the table exists.
    Assert that the function returns True.
    """
    conn = return_duckdb_conn("test.db")
    conn.execute("CREATE TABLE test_table (col1 INT)")
    table_exists = check_table_exists("config", "test_table", conn)
    assert table_exists is True
    
def test_create_config_tables():
    """
    Test the create_config_tables function.
    Create a DuckDB connection.
    Create the config schema.
    Create the config tables.
    Assert that the tables are created in the DuckDB database.
    """
    conn = return_duckdb_conn("test.db")
    create_schemas(conn)
    create_config_tables(conn)
    table_exists = conn.sql(
        "SELECT 1 FROM information_schema.tables WHERE table_name = 'country_codes'"
    ).fetchone()
    assert table_exists == (1,)