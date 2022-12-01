# Imports
import sys
sys.path.append('')

import pandas as pd
from sqlalchemy import create_engine
import os
import warnings
from libs.config import settings

# Set future warnings off
warnings.simplefilter(action='ignore', category=FutureWarning)
# Constants definition
DATASET_PATH = settings.DATASET_PATH
FOLDER_SAVE_CSV_PATH = settings.FOLDER_SAVE_CSV_PATH
# Database engine
engine = create_engine(settings.DATABASE_URL)


def extract(dataset: str) -> tuple:
    """
    Function that extracts data from dataset
    and convert it into a dataframe.

    Args:
        dataset (str): dataset location

    Returns:
        tuple: tuple containing the generated dataframes
    """
    df_transactions = pd.read_excel(dataset, "Transactions", skiprows=[0])
    df_target_customers = pd.read_excel(
        dataset, "NewCustomerList", skiprows=[0])
    df_demographic = pd.read_excel(dataset, "CustomerDemographic")
    df_address = pd.read_excel(dataset, "CustomerAddress", skiprows=[0])

    return df_transactions, df_target_customers, df_demographic, df_address


def transform_transactions(df_transactions: pd.DataFrame) -> tuple:
    """
    Function that transforms transactions data.

    Args:
        df_transactions (pd.DataFrame): transactions DataFrame.

    Returns:
        tuple: tuple containing transactions and products DataFrames.
    """
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
    df_target_customers = df_target_customers.iloc[:, :-7]
    # Rename and fix column types
    df_target_customers.rename(columns={'DOB': 'birth_date'}, inplace=True)
    df_target_customers["gender"] = \
        df_target_customers["gender"].astype('category')
    df_target_customers["owns_car"] = \
        df_target_customers["owns_car"].astype('bool')

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

    return df_customers


def load(df_transactions: pd.DataFrame,
         df_products: pd.DataFrame,
         df_target_customers: pd.DataFrame,
         df_customers: pd.DataFrame,
         csv_path: str):
    """
    Function that loads data to the database and also saves it to csv files.

    Args:
        df_transactions (pd.DataFrame): processed transactions DataFrame.
        df_products (pd.DataFrame): processed products DataFrame.
        df_target_customers (pd.DataFrame):
            processed target customers DataFrame.
        df_customers (pd.DataFrame): processed customers DataFrame.
        csv_path (str): path where store the csv files.
    """
    # Creates directory if not exists
    if not os.path.exists(csv_path):
        os.mkdir(csv_path)
    # Saves .csv files
    df_transactions.to_csv(f'{csv_path}/transactions.csv', index=False)
    df_products.to_csv(f'{csv_path}/products.csv', index=False)
    df_target_customers.to_csv(f'{csv_path}/target_customers.csv', index=False)
    df_customers.to_csv(f'{csv_path}/customers.csv', index=False)

    # Truncate tables before load
    engine.execute(
        'TRUNCATE TABLE current_customers, products, transactions, target_customers;'
    )

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


def run():
    """
        Function that execute the entire ETL process.
    """
    # Try to run the ETL process, catching posible exceptions
    try:
        # Extract
        df_transactions, df_target_customers, \
            df_demographic, df_address = extract(DATASET_PATH)
        # Transform
        df_end_transactions, df_end_products = transform_transactions(df_transactions)
        df_end_target_customers = transform_target_customers(df_target_customers)
        df_end_customers = transform_customers(df_address, df_demographic)
        # Load
        load(
            df_end_transactions,
            df_end_products,
            df_end_target_customers,
            df_end_customers,
            FOLDER_SAVE_CSV_PATH
        )
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()
