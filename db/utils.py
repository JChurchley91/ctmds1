import duckdb
import typer
import polars

from db.tables import CountryCodes, Granularity, Commodity, CountryEnergyMix

TABLES: dict = {
    "country_codes": CountryCodes.return_as_df(),
    "granularity": Granularity.return_as_df(),
    "commodity": Commodity.return_as_df(),
    "country_energy_mix": CountryEnergyMix.return_as_df(),
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


def create_schemas(conn: duckdb.DuckDBPyConnection) -> None:
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
        conn.execute(
            """
            CREATE SCHEMA IF NOT EXISTS prices;
            """
        )
        return None
    except Exception as error:
        typer.echo(f"Error creating schemas: {error}. Program will exit.")
        raise typer.Exit(code=1)


def check_table_exists(
    table_schema: str, table_name: str, conn: duckdb.DuckDBPyConnection
) -> bool:
    """
    Check if a table exists in a DuckDB database.

    :param table_schema: Schema name of table to check
    :param table_name: Table name to check
    :param conn: DuckDB connection to use
    :return: Boolean
    """
    return (
        True
        if conn.sql(
            f"SELECT 1 FROM information_schema.tables "
            f"WHERE table_schema = '{table_schema}' and table_name = '{table_name}'"
        )
        else False
    )


def create_or_append_table_from_df(
    df: polars.DataFrame,
    mode: str,
    schema_name: str,
    table_name: str,
    conn: duckdb.DuckDBPyConnection,
) -> None:
    """
    Create or append a table from a Polars DataFrame in a DuckDB database.
    Checks if the table exists before creating or appending.

    :param df: DataFrame to create or append the table from
    :param mode: Mode to use when creating the table (append or create)
    :param schema_name: Schema name of table to create or append into
    :param table_name: Table name to create or append into
    :param conn: DuckDB connection to use
    :return: None
    """
    if mode in ("append", "create"):
        try:
            df = df.with_columns(polars.Series("id", range(1, len(df) + 1)))
            df = df.select(["id"] + df.columns[:-1])
            conn.register("df", df)

            if mode == "append" and check_table_exists(schema_name, table_name, conn):
                conn.execute(f"INSERT INTO {schema_name}.{table_name} SELECT * FROM df")
            else:
                conn.execute(f"DROP TABLE IF EXISTS {schema_name}.{table_name}")
                conn.execute(
                    f"CREATE TABLE {schema_name}.{table_name} AS SELECT * FROM df"
                )

        except Exception as error:
            typer.echo(
                f"Error creating table from DataFrame: {error}. Program will exit."
            )
            raise typer.Exit(code=1)
    else:
        typer.echo(f"Invalid mode: {mode}. Program will exit.")
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
            create_or_append_table_from_df(df, "create", "config", table_name, conn)
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
