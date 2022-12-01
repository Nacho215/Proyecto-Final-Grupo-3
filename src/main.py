import sys
sys.path.append("..")

import pandas as pd
import os 
from sqlalchemy import create_engine
from libs.config import settings


DATASET_PATH = settings.DATASET_PATH
FOLDER_SAVE_CSV_PATH = settings.FOLDER_SAVE_CSV_PATH

engine = create_engine(settings.DATABASE_URL)

def extract(dataset: str) -> pd.DataFrame:
    """function to extract the data from the dataset
    and convert it into a dataframe

    Args:
        dataset (str): dataset location

    Returns:
        pd.DataFrame: list containing the generated dataframes
    """

    df_transactions = pd.read_excel(dataset, "Transactions", skiprows=[0])
    df_target_customers = pd.read_excel(
        dataset, "NewCustomerList", skiprows=[0])
    df_demographic = pd.read_excel(dataset, "CustomerDemographic")
    df_address = pd.read_excel(dataset, "CustomerAddress", skiprows=[0])

    return df_transactions, df_target_customers, df_demographic, df_address


def transform_transactions(df_transactions: pd.DataFrame) -> pd.DataFrame:
    """function to transform the data corresponding to the transactions

    Args:
        df_transactions (pd.DataFrame): dataset with transactions

    Returns:
        pd.DataFrame: dataframe df_transactions with
                      the transformations performed
    """

    df_transactions.drop("product_id", axis=1, inplace=True)

    df_transactions["online_order"] = df_transactions["online_order"].astype('bool')
    df_transactions["order_status"] = df_transactions["order_status"].astype('category')

    # Drop registers without product info (brand,
    # product_line, etc) because represents less than %1 of the dataset (197
    # from 20000).
    df_transactions = df_transactions[df_transactions['brand'].notna()]

    df_transactions["online_order"] = df_transactions["online_order"].astype('bool')

    df_products = df_transactions[["transaction_id",
                                   "brand",
                                   "product_line",
                                   "product_class",
                                   "product_size"]
                                ]

    df_products = df_products.groupby(["brand",
                                       "product_line",
                                       "product_class",
                                       "product_size"]
                                    ).size().reset_index()

    df_products.drop(0, axis=1, inplace=True)
    df_products.reset_index(inplace=True)
    df_products.rename(columns={"index": "product_id"}, inplace=True)

    df_transactions = df_transactions.merge(
        df_products,
        how='left',
        on=["brand", "product_line", "product_class", "product_size"]
    )

    df_transactions.drop(
        ["brand", "product_line", "product_class", "product_size"],
        axis=1,
        inplace=True
    )

    index_drop = df_transactions.loc[df_transactions['customer_id'] > 4000].index.tolist()
    df_transactions.drop(index=index_drop, inplace=True)
    df_transactions

    return df_transactions, df_products


def transform_target_customers(df_target_customers: pd.DataFrame) -> pd.DataFrame:
    """function to transform the data corresponding to the customer target

    Args:
        df_target_customers (pd.DataFrame): dataset with target customers

    Returns:
        pd.DataFrame: dataframe df_target_customers
                      with the transformations performed
    """

    # We can drop "Unnamed", "Rank" and "Value" columns since they dont give
    # us any useful information.
    df_target_customers = df_target_customers.iloc[:, :-7]

    df_target_customers.rename(columns={'DOB': 'birth_date'}, inplace=True)

    df_target_customers["gender"] = df_target_customers["gender"].astype('category')

    df_target_customers["owns_car"] = df_target_customers["owns_car"].astype('bool')

    return df_target_customers


def transform_customers(df_address: pd.DataFrame,
                        df_demographic: pd.DataFrame) -> pd.DataFrame:
    """function to transform the data corresponding to the customer

    Args:
        df_address (pd.DataFrame):  dataset with customer address
        df_demographic (pd.DataFrame): dataset with customer demographics

    Returns:
        pd.DataFrame: dataframe df_customers with the transformations performed
    """

    df_customers = df_demographic.merge(df_address, on='customer_id', how='left')

    df_customers.rename(columns={'DOB': 'birth_date'}, inplace=True)

    df_customers["gender"] = df_customers["gender"].astype('category')
    df_customers["owns_car"] = df_customers["owns_car"].astype('bool')

    return df_customers


def load(df_transactions: pd.DataFrame,
         df_product: pd.DataFrame,
         df_target_customers: pd.DataFrame,
         df_customers: pd.DataFrame):
    """function to load the data to the database and save the data in csv files

    Args:
        df_transactions (pd.DataFrame): dataset with transactions processed
        df_product (pd.DataFrame): dataset with processed products
        df_target_customers (pd.DataFrame): dataset with processed target customers
        df_customers (pd.DataFrame): dataset with processed customers
    """
    if os.path.exists(FOLDER_SAVE_CSV_PATH) == False:
        os.mkdir(FOLDER_SAVE_CSV_PATH)

    df_transactions.to_csv(f'{FOLDER_SAVE_CSV_PATH}/transactions.csv', index=False)
    df_product.to_csv(f'{FOLDER_SAVE_CSV_PATH}/products.csv', index=False)
    df_target_customers.to_csv(f'{FOLDER_SAVE_CSV_PATH}/target_customers.csv', index=False)
    df_customers.to_csv(f'{FOLDER_SAVE_CSV_PATH}/customers.csv', index=False)

    
    df_transactions.to_sql('transactions', engine, if_exists='append', index=False)
    df_product.to_sql('products', engine, if_exists='append', index=False) 
    df_target_customers.to_sql('target_customers', engine, if_exists='append', index=False)
    df_customers.to_sql('customers', engine, if_exists='append', index=False)


def run():
    """
        function to execute the extraction processes,
        data transformation and loading
    """

    try:
        df_transactions, df_target_customers, df_demographic, df_address = extract(DATASET_PATH)

        df_end_transactions, df_end_product = transform_transactions(df_transactions)
        df_end_target_customers = transform_target_customers(df_target_customers)
        df_end_customers = transform_customers(df_address, df_demographic)

        load(df_end_transactions,
            df_end_product,
            df_end_target_customers,
            df_end_customers
        )

    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()