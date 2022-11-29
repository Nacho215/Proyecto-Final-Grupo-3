import pandas as pd 
import logging 


DATASET_PATH = '../datasets/KPMG_VI_New_raw_data_update_final.xlsx'

def extract(dataset:str):
    
    df_transactions = pd.read_excel(dataset, "Transactions", skiprows=[0])
    df_customers = pd.read_excel(dataset, "NewCustomerList", skiprows=[0])
    df_demographic = pd.read_excel(dataset, "CustomerDemographic")
    df_address = pd.read_excel(dataset, "CustomerAddress", skiprows=[0])

    return df_transactions, df_customers, df_demographic, df_address


def transform_transactions(df_transactions):
    pass


def transform_customers(df_customers):
    pass


def transform_demographic(df_demographic):
    pass


def transform_address(df_address):
    pass


def load(df_transactions,df_customers,df_demographic,df_address):
    pass


def main():
    try:
        df_list = extract(DATASET_PATH)
        
        df_transform_transactions = transform_transactions(df_list[0])
        df_transform_customers = transform_customers(df_list[1])
        df_transform_demographic = transform_demographic(df_list[2])
        df_transform_address = transform_address(df_list[3])
        
        load(
            df_transform_transactions,
            df_transform_customers,
            df_transform_demographic, 
            df_transform_address
        )

    except Exception as e:
        print(e)
    

if __name__ == '__main__':
    main()
    
