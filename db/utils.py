import duckdb
import typer
import polars

from db.tables import CountryCodes, Granularity, Commodity

TABLES: dict = {
    "country_codes": CountryCodes.return_as_df(),
    "granularity": Granularity.return_as_df(),
    "commodity": Commodity.return_as_df(),
}


def create_duckdb_db(db_name: str) -> bool | None:
    """
    Create a DuckDB database.

    :param db_name: Name of the database to be created
    :return: None
    """
    try:
        conn = duckdb.connect(db_name)
        conn.close()
        return True
    except Exception as error:
        typer.echo(f"Error creating DuckDB database: {error}. Program will exit.")
        raise typer.Exit(code=1)


def return_duckdb_conn(db_name: str) -> duckdb.DuckDBPyConnection:
    """
    Return a DuckDB connection.

    :param db_name: Name of the database to connect to
    :return: duckdb.DuckDBPyConnection
    """
    try:
        conn = duckdb.connect(db_name)
        return conn
    except Exception as error:
        typer.echo(f"Error connecting to DuckDB database: {error}. Program will exit.")
        raise typer.Exit(code=1)


def create_config_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Create the base config schema in the DuckDB database.

    :param conn: DuckDB connection to use
    :return: None
    """
    try:
        conn.execute(
            """
            CREATE SCHEMA IF NOT EXISTS config;
            """
        )
        return None
    except Exception as error:
        typer.echo(f"Error creating config schema: {error}. Program will exit.")
        raise typer.Exit(code=1)


def create_table_from_df(
    df: polars.DataFrame,
    schema_name: str,
    table_name: str,
    conn: duckdb.DuckDBPyConnection,
) -> None:
    """
    Create a table in a DuckDB database from a Polars DataFrame.
    Add an ID column to the DataFrame before creating the table.
    Tables are dropped and recreated if they already exist.

    :param df: Polars DataFrame to create a table from
    :param schema_name: Name of the schema to create the table in
    :param table_name: Name of the table to create
    :param conn: DuckDB connection to use
    :return: None
    """
    try:
        df = df.with_columns(polars.Series("id", [i + 1 for i in range(len(df))]))
        df = df.select(["id"] + df.columns[:-1])
        conn.register("df", df)
        conn.execute(f"DROP TABLE IF EXISTS {schema_name}.{table_name}")
        conn.execute(f"CREATE TABLE {schema_name}.{table_name} AS SELECT * FROM df")
    except Exception as error:
        typer.echo(f"Error creating table from DataFrame: {error}. Program will exit.")
        raise typer.Exit(code=1)


def create_config_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Create the base config tables in the DuckDB database.
    Uses the TABLES dictionary to create the tables.

    :param conn: DuckDB connection to use
    :return: None
    """
    try:
        for table_name, df in TABLES.items():
            create_table_from_df(df, "config", table_name, conn)
        return None
    except Exception as error:
        typer.echo(f"Error creating config tables: {error}. Program will exit.")
        raise typer.Exit(code=1)


def select_duckdb_table(
    conn: duckdb.DuckDBPyConnection, schema_name: str, table_name: str
) -> polars.DataFrame:
    """
    Select a table from a DuckDB database and return it as a Polars DataFrame.

    :param conn: DuckDB connection to use
    :param schema_name: Name of the schema to select the table from
    :param table_name: Name of the table to select
    :return: Polars DataFrame
    """
    try:
        df = duckdb.sql(
            connection=conn, query=f"SELECT * FROM {schema_name}.{table_name}"
        ).pl()
        return df
    except Exception as error:
        typer.echo(f"Error selecting table: {error}. Program will exit.")
        raise typer.Exit(code=1)


def create_daily_prices_table(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Create the daily_prices table in the DuckDB database.

    :return: None
    """
    pass
