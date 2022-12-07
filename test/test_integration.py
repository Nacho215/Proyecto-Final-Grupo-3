from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
import pandas as pd
import pytest
import logging
import logging.config
from shutil import rmtree
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from libs.db import Base
from libs.config import settings
from src.main import extract
from src.main import transform_transactions
from src.main import transform_target_customers
from src.main import transform_customers
from src.main import load
from src.main import download_dataset_from_s3

# Loggings
# Path level
root = Path.cwd().parent
root = f'{root}/config_logs.conf'

# open file config
logging.config.fileConfig(root)
logger = logging.getLogger('TEST')
logger.info('Beginning integration tests!')

# Parameters to will be use into tests
S3_KEY = settings.S3_KEY
S3_SECRET = settings.S3_SECRET
S3_BUCKET = settings.S3_BUCKET
S3_DATASET_PATH = settings.S3_DATASET_PATH
DATASET_PATH = os.path.join(settings.DATASET_DIR, settings.S3_DATASET_NAME)
S3_CREDENTIALS = settings.S3_CREDENTIALS
S3_FOLDER_SAVE_CSV_PATH = settings.S3_FOLDER_SAVE_CSV_PATH
DATASET_DIR = settings.DATASET_DIR

# Create database, engine, session and tables into database
db_path = os.path.join(os.path.dirname(__file__), 'test.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
engine_test = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine_test)
Base.metadata.create_all(bind=engine_test)


@pytest.fixture
def dataframes_generate() -> pd.DataFrame:
    """Function that return dataframes to will be use into tests

    Returns:
        pd.DataFrame: Touple of dataframes downloaded and transformed
    """
    # If path not exist so create teporary folder to datasets
    if not (Path(__file__).parent.parent / "datasets").exists():
        os.mkdir(Path(__file__).parent.parent / "datasets")

    # Download dataset from aws s3 bucket
    download_dataset_from_s3(
        S3_KEY,
        S3_SECRET,
        S3_BUCKET,
        S3_DATASET_PATH,
        DATASET_PATH,
        DATASET_DIR
    )

    # Extract
    df_transactions, df_target_customers, \
        df_demographic, df_address = extract(DATASET_PATH)
    # Transform
    df_end_transactions, df_end_products = \
        transform_transactions(df_transactions)
    df_end_target_customers = \
        transform_target_customers(df_target_customers)
    df_end_customers = transform_customers(df_address, df_demographic)

    return df_end_transactions, df_end_products,\
        df_end_target_customers, df_end_customers


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_dataframe_load_database(dataframes_generate):
    """Test function that verify if tables was created into database with all
    records

    Args:
        dataframes_generate (pd.DataFrame): _description_
    """
    df_end_transactions, df_end_products,\
        df_end_target_customers, df_end_customers = dataframes_generate

    load(
        df_end_transactions,
        df_end_products,
        df_end_target_customers,
        df_end_customers,
        S3_FOLDER_SAVE_CSV_PATH,
        S3_CREDENTIALS,
        engine_test,
        testing=True
    )

    conn = engine_test.connect()

    # verifies if data has been uploaded to the database
    assert conn.execute(
        "SELECT COUNT(product_id) as number_reg FROM products")\
        .fetchall()[0][0] > 0, logger.warning(
            'Test Count rows is greater 0 -> Failed')

    assert conn.execute(
        "SELECT COUNT(customer_id) as number_reg FROM current_customers")\
        .fetchall()[0][0] > 0, logger.warning(
            'Test Count rows is greater 0 -> Failed')

    assert conn.execute(
        "SELECT COUNT(first_name) as number_reg FROM target_customers")\
        .fetchall()[0][0] > 0, logger.warning(
            'Test Count rows is greater 0 -> Failed')

    assert conn.execute(
        "SELECT COUNT(transaction_id) as number_reg FROM transactions")\
        .fetchall()[0][0] > 0, logger.warning(
            'Test Count rows is greater 0 -> Failed')

    conn.close()

    logger.info(
        'Test check count of rows is greater 0 -> Successfully Completed!')

    os.remove(os.path.join(os.path.dirname(__file__), 'test.db'))

    rmtree(Path(__file__).parent.parent / "datasets")


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_empty_dataframes_to_database(dataframes_generate):
    """Test if load function rise correct exception if
    I send an emmpty dataframe

    Args:
        dataframes_generate (pd.DataFrame): _description_
    """
    df_end_transactions, df_end_products,\
        df_end_target_customers, df_end_customers = dataframes_generate

    df_end_transactions = pd.DataFrame({})
    df_end_products = pd.DataFrame({})

    return_value = load(
                    df_end_transactions,
                    df_end_products,
                    df_end_target_customers,
                    df_end_customers,
                    S3_FOLDER_SAVE_CSV_PATH,
                    S3_CREDENTIALS,
                    engine_test,
                    testing=True
                )
    assert return_value == ValueError, logger.warning(
            'Test check if return ValueError -> Failed')

    logger.info(
        'Test rise correct exception -> Successfully Completed!')
