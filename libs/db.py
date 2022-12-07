'''
Here we will create the engine variable that will connect to the database
engine, the session variable to be able to perform operations on the tables,
and the variable Base which is inherited to create in the model the classes
that make references to the references to the different tables in the model.
'''
import logging
import logging.config
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from libs.config import settings

# Sqlalchemy
# engine is created to be called as modules from other scripts
default_engine = create_engine(settings.DATABASE_URL)
# base is created to be called as modules from other scripts
Base = declarative_base()

# Logging
# Path level
root = Path.cwd().parent
root = f'{root}/config_logs.conf'
# open file config
logging.config.fileConfig(root)
logger = logging.getLogger('DB')


# Class to add functionality
class CommonActions:
    '''
    This class groups actions or tasks in common
    for the different scripts or classes.
    '''
    def truncate_tables(
        tables: list,
        engine=default_engine
    ) -> None | Exception:
        """
        This methods performs a truncate to the tables.

        Args:
            engine (Engine, optional): Database connection engine.
                Defaults to default_engine.

        Returns:
            None | Exception: captured exception if any,
                or None otherwise.
        """
        # Iterate table names list and build the truncate query
        query = "TRUNCATE TABLE "
        for idx, table_name in enumerate(tables):
            query += table_name
            if idx < len(tables) - 1:
                query += ", "
        # Catch and return possible exceptions
        try:
            engine.execute(query)
        except Exception as exc:
            logger.error(f'Truncate tables failed. {exc}')
            return exc
        else:
            logger.info(f"Truncated Tables successfully: '{query}'")
            return None

    def execute_query(
        table: str,
        columns=None,
        filters=None,
        engine=default_engine
    ) -> list | Exception:
        """
        Builds a simple query with given parameters,
        executes it and return the results.

        Args:
            table (str): table name
            columns (list): a list with column names. Defaults to None.
            filters (str, optional): filters to apply
                (WHERE clause without the WHERE keyword). Defaults to None.
            engine (Engine, optional): Database connection engine.
                Defaults to default_engine.

        Returns:
            list | Exception: a list of returned rows,
                or captured exception if any.
        """
        # Builds the query with given parameters
        # SELECT
        query = "SELECT "
        if columns:
            for idx, col in enumerate(columns):
                query += col
                if idx < len(columns) - 1:
                    query += ', '
        else:
            query += "* "
        # FROM
        query += f"FROM {table}"
        # WHERE
        if filters:
            query += f" WHERE {filters}"
        query += ";"

        # Try to execute it, catching possible exceptions
        try:
            result = engine.execute(query)
        except Exception as exc:
            logger.error(f'Failed to execute query:{query}. Exception: {exc}')
            return exc
        else:
            # If executed successfully, return fetched rows
            logger.info(f'Query executed successfully: {query}')
            return result.fetchall()
