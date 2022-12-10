"""
Adds a UI on top of a dataframe to let viewers filter columns

Args:
    df (pd.DataFrame): Original dataframe

Returns:
    pd.DataFrame: Filtered dataframe
"""
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
from pathlib import Path
import requests
import boto3
import pandas as pd
import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from libs.config import settings

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.sidebar.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))            
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            #get the max and min from the dataset
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            #once the user enters two dates, the dataset can be filtered
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            #convert other dtypes to string
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

# Aply singleton to set it in cache memory, in that way in futures requests will 
# not be neccesary download again the files
@st.experimental_singleton
def s3_csv_downloader():
    """Function that download files of s3 service only if didn't be downloaded

    Returns:
        bool: return True if in the path had been downloaded 
        csv in the other hand return False
    """
    S3_KEY = settings.S3_KEY
    S3_SECRET = settings.S3_SECRET
    S3_BUCKET = settings.S3_BUCKET

    dataset_local_path = Path(__file__).parent.parent/'outputs'

    client = boto3.client('s3')

    client = boto3.client(
        's3',
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET
    )

    dats = requests.get('http://127.0.0.1:8000/dataset/get_data')
    # Convert json object into python dict
    dats = dats.json()
    
    if not dataset_local_path.exists():
        os.mkdir(dataset_local_path)

    # Go throw paths of s3 and download all csv files
    for i in dats:
        dataset_s3_path = f'{dats[i]}'
        try:
            client.download_file(S3_BUCKET, dataset_s3_path, f"{dataset_local_path}/{i.split('/')[-1]}")            
        except Exception as ex:
            print(f"error - {ex}")

    count = 0
    for i in dataset_local_path.iterdir():
        count += 1

    if 0 < count <= 4:
        return True
    else:
        return False