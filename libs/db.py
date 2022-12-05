'''
Here we will create the engine variable that will connect to the database
engine, the session variable to be able to perform operations on the tables,
and the variable Base which is inherited to create in the model the classes
that make references to the references to the different tables in the model.
'''
# import logging
# import logging.config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from libs.config import settings
import sys
sys.path.append('')

# Sqlalchemy
# engine is created to be called as modules from other scripts
engine = create_engine(settings.DATABASE_URL)
# session is created to be called as modules from other scripts
Session = sessionmaker(bind=engine)
session = Session()
# base is created to be called as modules from other scripts
Base = declarative_base()

# Logging
# Opening configuration file
# logging.config.fileConfig('./config_logs.conf')
# # Create logger
# logger = logging.getLogger('dbLogger')
# logger.info('probando dbLogger')


# Class to add functionality
class CommonActions:
    '''
    This class groups actions or tasks in common
    for the different scripts or classes.
    '''
    def truncate_tables(self) -> None:
        '''
        This methods performs a truncate
        to the tables
        '''
        tables = 'target_customers, transactions, current_customers,products'
        try:
            session.execute(f"TRUNCATE TABLE {tables}")
            session.commit()
            session.close()
        except Exception:
            # logger.error('Truncate Failed')
            raise ('Trancate Failed')
        else:
            print('Truncated Tables')
            # logger.info('Truncated Tables')

    def execute_query(table: str, columns=None, filters=None) -> list | None:
        """
        Builds a simple query with given parameters,
        executes it and return the results.

        Args:
            table (str): table name
            columns (list): a list with column names. Defaults to None.
            filters (str, optional): filters to apply
                (WHERE clause without the WHERE keyword). Defaults to None.

        Returns:
            list | None: a list of returned rows.
                None if failed to execute query.
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
        query += f" FROM {table}"
        # WHERE
        if filters:
            query += f" WHERE {filters}"
        query += ";"

        # Try to execute it, catching possible exceptions
        try:
            result = session.execute(query)
            session.commit()
            session.close()
        except Exception as e:
            # logger.error('f'Failed to execute query: {query}. Exception: {e}')
            print(f'Failed to execute query: {query}.\n{e}')
            return None
        else:
            # If executed successfully, return fetched rows
            # logger.info(f'Query executed successfully: {query}')
            print(f'Query executed successfully: {query}')
            return result.fetchall()
