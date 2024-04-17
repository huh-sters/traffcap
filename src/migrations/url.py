import os
from dotenv import load_dotenv


load_dotenv()


def generate_db_url(migration: bool = False) -> str:
    """
    Trying to be as nice as possible but also trying to accomodate whatever
    persistent storage a user needs. This will be populated by environment
    variable.

    This configuration is for Alembic to run migrations. By default it uses
    the non async sqlite driver as that's what Alembic expects. The main
    traffcap application will use the async part of the driver.
    """
    db_config = {
        "driver": os.getenv('TRAFFCAP_DB_DRIVER', 'sqlite'),
        "user":  os.getenv('TRAFFCAP_DB_USER', ''),
        "password":  os.getenv('TRAFFCAP_DB_PASSWORD', ''),
        "host": os.getenv('TRAFFCAP_DB_HOST', ''),
        "name": os.getenv('TRAFFCAP_DB_NAME', 'traffcap.db'),
    }

    aio_handlers = {
        "sqlite": "sqlite+aiosqlite",  # Tested
        "mysql": "mysql+aiomysql",  # Tested
        "mssql": "mssql+pyodbc",  # TODO: AIO Test MS SQL+pyodbc
        "postgresql": "postgresql+asyncpg",  # TODO: AIO Test PostgreSQL + asyncpg
        "oracle": "oracle+cx_oracle_async"  # TODO: AIO Test Oracle + CX Oracle async
    }

    non_aio_handlers = {
        "sqlite": "sqlite",  # Tested
        "mysql": "mysql+pymysql",  # Tested
        "mssql": "mssql+pyodbc",  # TODO: Non-AIO Test MS SQL + pyodbc
        "postgresql": "postgresql+psycopg2",  # TODO: Non-AIO Test PostgreSQL + psycopg2
        "oracle": "oracle+cx_oracle"  # TODO: Non-AIO Test Oracle + CX Oracle
    }

    if migration:
        db_config["driver"] = non_aio_handlers[db_config["driver"]]
    else:
        db_config["driver"] = aio_handlers[db_config["driver"]]

    if db_config["driver"].startswith("sqlite"):
        # Treat SQLite differently
        return "{driver}:///{name}".format(**db_config)

    return "{driver}://{user}:{password}@{host}/{name}".format(**db_config)
