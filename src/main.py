# Imports
import sys
sys.path.append('')

import pandas as pd
import warnings
import boto3
import os
from libs.config import settings
from libs.db import engine
from libs.db import CommonActions


# Set future warnings off
warnings.simplefilter(action='ignore', category=FutureWarning)


# Constants definition
S3_KEY = settings.S3_KEY
S3_SECRET = settings.S3_SECRET
S3_CREDENTIALS = settings.S3_CREDENTIALS
S3_BUCKET = settings.S3_BUCKET
S3_FOLDER_SAVE_CSV_PATH = settings.S3_FOLDER_SAVE_CSV_PATH
S3_DATASET_PATH = settings.S3_DATASET_PATH
DATASET_PATH = os.path.join(settings.DATASET_DIR, settings.S3_DATASET_NAME)
DATASET_DIR = settings.DATASET_DIR

def download_dataset_from_s3(
    s3_key: str, s3_secret: str,
    s3_bucket: str, s3_dataset_path: str,
    output_dataset_path: str,
    dataset_dir:str
    ) -> bool:
    """
    Download dataset from aws s3 bucket.

    Args:
        s3_key (str): aws key id
        s3_secret (str): aws secret
        s3_bucket (str): s3 bucket name
        s3_dataset_path (str): s3 dataset location
        output_dataset_path (str): local path to store downloaded dataset.
        dataset_dir (str): Directory where the data set is stored
    Returns:
        bool: True if downloaded dataset successfully.
            False otherwise.
    """
    try:
        # Download dataset from s3 to local_dataset_path
        client = boto3.client(
            's3',
            aws_access_key_id=s3_key,
            aws_secret_access_key=s3_secret
        )
        
        # create directory to save the dataset if it does not exist
        if not os.path.exists(dataset_dir):
            os.mkdir(dataset_dir)

        client.download_file(s3_bucket, s3_dataset_path, output_dataset_path)
    except Exception as e:
        print(f"Failed to download dataset from S3 bucket.\n {e}")
        return False
    else:
        return True


def extract(dataset: str) -> tuple:
    """
    Function that extracts data from dataset
    and convert it into a dataframe.

    Args:
        dataset (str): dataset location

    Returns:
        tuple: tuple containing the generated dataframes
    """
    try : 
        df_transactions = pd.read_excel(dataset, "Transactions", skiprows=[0])
        df_target_customers = pd.read_excel(
            dataset, "NewCustomerList", skiprows=[0])
        df_demographic = pd.read_excel(dataset, "CustomerDemographic")
        df_address = pd.read_excel(dataset, "CustomerAddress", skiprows=[0])
    except FileNotFoundError:
        print('error al abrir el dataset')
    except Exception as e :
        print(f'se produjo un error al extraer los dataframes del dataset {e}')

    return df_transactions, df_target_customers, df_demographic, df_address


def transform_transactions(df_transactions: pd.DataFrame) -> tuple:
    """
    Function that transforms transactions data.

    Args:
        df_transactions (pd.DataFrame): transactions DataFrame.

    Returns:
        tuple: tuple containing transactions and products DataFrames.
    """
    
    try : 
    # Drop product_id column because it's not reliable
        df_transactions.drop("product_id", axis=1, inplace=True)
        # Fix column types
        df_transactions["online_order"] = \
            df_transactions["online_order"].astype('bool')
        df_transactions["order_status"] = \
            df_transactions["order_status"].astype('category')
        df_transactions["online_order"] = \
            df_transactions["online_order"].astype('bool')
        # Drop registers without product info (brand, product_line, etc)
        # because represents less than %1 of the dataset (197 from 20000).
        df_transactions = df_transactions[df_transactions['brand'].notna()]

        # Extract product information into a new products DataFrame
        df_products = df_transactions[[
            "transaction_id",
            "brand",
            "product_line",
            "product_class",
            "product_size"
        ]]
        # Make products unique
        df_products = df_products.groupby([
            "brand",
            "product_line",
            "product_class",
            "product_size"
            ]).size().reset_index()
        # Create products id's
        df_products.drop(0, axis=1, inplace=True)
        df_products.reset_index(inplace=True)
        df_products.rename(columns={"index": "product_id"}, inplace=True)

        # Add product_id column to transactions DataFrame
        df_transactions = df_transactions.merge(
            df_products,
            how='left',
            on=["brand", "product_line", "product_class", "product_size"]
        )
        # Drop old product information from transactions DataFrame
        df_transactions.drop(
            ["brand", "product_line", "product_class", "product_size"],
            axis=1,
            inplace=True
        )

        # Drop transactions with not valid customer_id values
        index_drop = df_transactions.loc[
            df_transactions['customer_id'] > 4000
            ].index.tolist()
        df_transactions.drop(index=index_drop, inplace=True)
    except KeyError:
        print('existe un error en el dataset')
    except Exception as e :
        print(f'se produjo un error al procesar el dataset {e}')

    return df_transactions, df_products


def transform_target_customers(df_target_customers: pd.DataFrame) -> pd.DataFrame:
    """
    Function that transforms target customers data.

    Args:
        df_target_customers (pd.DataFrame): target customers DataFrame.

    Returns:
        pd.DataFrame: dataframe df_target_customers
                      with the transformations performed.
    """
    # Drop "Unnamed", "Rank" and "Value" columns
    # since they dont give us any useful information.
    try:
        df_target_customers = df_target_customers.iloc[:, :-7]
        # Rename and fix column types
        df_target_customers.rename(columns={'DOB': 'birth_date'}, inplace=True)
        df_target_customers["gender"] = \
            df_target_customers["gender"].astype('category')
        df_target_customers["owns_car"] = \
            df_target_customers["owns_car"].astype('bool')
    except KeyError:
        print('existe un error en el dataset')
    except Exception as error :
        print(f'se produjo un error al procesar el dataset {error}')

    return df_target_customers


def transform_customers(df_address: pd.DataFrame,
                        df_demographic: pd.DataFrame) -> pd.DataFrame:
    """
    Function that transforms customer data.

    Args:
        df_address (pd.DataFrame):  customer address DataFrame.
        df_demographic (pd.DataFrame): customer demographics DataFrame.

    Returns:
        pd.DataFrame: unified and normalized customers DataFrame.
    """
    try:
        # Left merge both DataFrames on 'customer_id'
        df_customers = df_demographic.merge(
            df_address,
            on='customer_id',
            how='left'
        )
        # Rename and fix column types
        df_customers.rename(columns={'DOB': 'birth_date'}, inplace=True)
        df_customers["gender"] = df_customers["gender"].astype('category')
        df_customers["owns_car"] = df_customers["owns_car"].astype('bool')
    except KeyError:
        print('existe un error en el dataset')
    except Exception as e :
        print(f'se produjo un error al procesar el dataset {e}')

    return df_customers


def load(df_transactions: pd.DataFrame,
         df_products: pd.DataFrame,
         df_target_customers: pd.DataFrame,
         df_customers: pd.DataFrame,
         s3_csv_save_path: str,
         s3_credentials: dict):
    """
    Function that loads data to the database and also saves it to csv files.

    Args:
        df_transactions (pd.DataFrame): processed transactions DataFrame.
        df_products (pd.DataFrame): processed products DataFrame.
        df_target_customers (pd.DataFrame):
            processed target customers DataFrame.
        df_customers (pd.DataFrame): processed customers DataFrame.
        s3_csv_save_path (str): path where store the csv files.
        s3_credentials (dict): aws s3 access credentials
    """
    try: 
        # Saves .csv files in aws s3 bucket
        df_transactions.to_csv(
            f'{s3_csv_save_path}/transactions.csv',
            index=False,
            storage_options=s3_credentials
        )
        df_products.to_csv(
            f'{s3_csv_save_path}/products.csv',
            index=False,
            storage_options=s3_credentials
        )
        df_target_customers.to_csv(
            f'{s3_csv_save_path}/target_customers.csv',
            index=False,
            storage_options=s3_credentials
        )
        df_customers.to_csv(
            f'{s3_csv_save_path}/customers.csv',
            index=False,
            storage_options=s3_credentials
        )

        # Truncate tables before load
        commonactions = CommonActions()
        commonactions.truncate_tables()

        # Load processed dataframes into database tables
        df_products.to_sql(
            'products',
            engine,
            if_exists='append',
            index=False
        )
        df_customers.to_sql(
            'current_customers',
            engine,
            if_exists='append',
            index=False
        )
        df_target_customers.to_sql(
            'target_customers',
            engine, if_exists='append',
            index=False
        )
        df_transactions.to_sql(
            'transactions',
            engine,
            if_exists='append',
            index=False
        )
    except Exception as e:
        print(f'se produjo el siguiente error al cargar los datos: {e}')

def run():
    """
        Function that executes the entire ETL process.
    """
    # Try to run the ETL process, catching posible exceptions
    try:
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
        # Load
        load(
            df_end_transactions,
            df_end_products,
            df_end_target_customers,
            df_end_customers,
            S3_FOLDER_SAVE_CSV_PATH,
            S3_CREDENTIALS
        )
    except Exception as e:
        print(f'ETL process failed. Error: {e}')


if __name__ == '__main__':
    run()
