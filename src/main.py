import pandas as pd 

DATASET_PATH = '../datasets/KPMG_VI_New_raw_data_update_final.xlsx' #replace lib.conf.setting.DATASET_PATH


def extract(dataset:str):

    df_transactions = pd.read_excel(dataset, "Transactions", skiprows=[0])
    df_target_customers = pd.read_excel(dataset, "NewCustomerList", skiprows=[0])
    df_demographic = pd.read_excel(dataset, "CustomerDemographic")
    df_address = pd.read_excel(dataset, "CustomerAddress", skiprows=[0])

    return  df_transactions, df_target_customers, df_demographic, df_address
    

def transform_transactions(df_transactions:pd.DataFrame) -> pd.DataFrame:
    df_transactions.drop("product_id", axis=1, inplace=True)
    
    #Drop registers without product info (brand,
    #product_line, etc) because represents less than %1 of the dataset (197 from 20000).
    df_transactions = df_transactions[df_transactions['brand'].notna()]
    df_transactions[df_transactions["brand"].isna()]
    
    df_products = df_transactions[["transaction_id", "brand", "product_line", "product_class", "product_size"]]
    df_products = df_products.groupby(["brand", "product_line", "product_class", "product_size"]).size().reset_index()
    df_products.drop(0, axis=1, inplace=True)
    df_products.reset_index(inplace=True)
    df_products.rename(columns={"index" : "product_id"}, inplace=True)

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

    return df_transactions, df_products


def transform_target_customers(df_target_customers:pd.DataFrame):
    #We can drop "Unnamed", "Rank" and "Value" columns since they dont give us any useful information.
    df_target_customers = df_target_customers.iloc[:, :-7]
    df_target_customers.rename(columns = {'DOB':'birth_date'}, inplace = True)
    
    return df_target_customers


def transform_customers(df_address:pd.DataFrame, df_demographic:pd.DataFrame) -> pd.DataFrame:
    df_customers = df_demographic.merge(df_address, on='customer_id', how='inner')
    df_customers.rename(columns = {'DOB':'birth_date'}, inplace = True)
    return df_customers


def load(df_transactions:pd.DataFrame,
        df_customers:pd.DataFrame,
        df_demographic:pd.DataFrame,
        df_address:pd.DataFrame) -> pd.DataFrame:
    pass


def run():
    try:
        df_transactions, df_target_customers, df_demographic, df_address = extract(DATASET_PATH)

        df_end_transactions, df_end_product = transform_transactions(df_transactions)
        df_end_target_customers = transform_target_customers(df_target_customers)
        df_end_customers = transform_customers(df_address,df_demographic)
        
        #load()

    except Exception as e:
        print(e)
    

if __name__ == '__main__':
    run()
    
