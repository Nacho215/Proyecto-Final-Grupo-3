'''
This module contains the unit tests corresponding to the src.main module:

    1 - functions covered by the tests
    2 - download_dataset_from_s3
    3 - extract
    4 - transform_target_customers
    5 - transform_customers


'''
import sys
sys.path.append('')
import pandas as pd
from src.main import S3_KEY, S3_SECRET, S3_BUCKET, S3_DATASET_PATH, DATASET_PATH, DATASET_DIR
from src.main import download_dataset_from_s3, extract, transform_transactions, transform_target_customers, transform_customers
import botocore
import pytest


# --------- START TEST download_dataset_from_s3 function --------

@pytest.mark.parametrize('s3_key, s3_secret, s3_bucket, s3_dataset_path,dataset_path, dataset_dir, expected_exception', [
    # key and secret incorrect
    ('AZUasdHWTZ2MDHCZHO6', 'IAZasdUasdHWTZ2MDHCZHO6', S3_BUCKET,
     S3_DATASET_PATH, DATASET_PATH, DATASET_DIR, botocore.exceptions.ClientError),

    (S3_KEY, S3_SECRET, 'BUCKET_NO_EXIST', S3_DATASET_PATH,
     DATASET_PATH, DATASET_DIR, botocore.exceptions.ClientError),

    (S3_KEY, S3_SECRET, S3_BUCKET, 'outputs/file_no_exist.xlsx',
     DATASET_PATH, DATASET_DIR, botocore.exceptions.ClientError),

    (S3_KEY, S3_SECRET, S3_BUCKET, S3_DATASET_PATH,
     'folder_no_exist/file_no_exist.xlsx', DATASET_DIR, FileNotFoundError),

]
)
def test_download_dataset_from_s3(s3_key, s3_secret, s3_bucket, s3_dataset_path, dataset_path, dataset_dir, expected_exception):
    assert type(download_dataset_from_s3(
            s3_key, s3_secret, s3_bucket, s3_dataset_path, dataset_path, dataset_dir)) == expected_exception

def test_download_dataset_from_s3_success():
    assert download_dataset_from_s3(S3_KEY, S3_SECRET, S3_BUCKET, S3_DATASET_PATH, DATASET_PATH, DATASET_DIR) == True

# --------- END TEST download_dataset_from_s3 function ---------


# global dataframes are created with the necessary content for use in subsequent tests

df_transactions, df_target_customers, \
   df_demographic, df_address = extract(DATASET_PATH)


# --------- START TEST extract function ---------
@pytest.mark.parametrize('dataset, expected_exception',
                         [
                             ('', FileNotFoundError),
                             ('./outputs/dataset_not_exist.xlsx',
                                 FileNotFoundError),
                         ]
                         )
def test_extract(dataset, expected_exception):
    assert expected_exception ==  type(extract(dataset))



@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_extract_success():
    assert type(extract(DATASET_PATH)) == tuple


# --------- END TEST extract function ---------


# --------- START TEST transform_transactions function ---------

@pytest.mark.parametrize('df_transactions, expected_exception',
                         [
                             (pd.DataFrame(), KeyError),
                             (pd.DataFrame({'name': ['ricardo', 'nacho'], 'last_name': [
                                 'apellido1', 'apellido2']}), KeyError),
                         ]
                         )
def test_transform_transactions(df_transactions, expected_exception):
    assert expected_exception == type(transform_transactions(df_transactions))


def test_transform_transactions_success():
    assert type(transform_transactions(df_transactions)) == tuple

# --------- END TEST transform_transactions function ---------


# --------- START TEST transform_target_customers function ---------

@pytest.mark.parametrize('df_target_customers, expected_exception',
                         [
                             (pd.DataFrame(), KeyError),
                             (pd.DataFrame({'name': ['ricardo', 'nacho'], 'last_name': [
                                 'apellido1', 'apellido2']}), KeyError),
                         ]
                         )
def test_transform_target_customers(df_target_customers, expected_exception):
    assert expected_exception == type(transform_target_customers(df_target_customers))


def test_transform_target_customers_success():
    assert type(transform_target_customers(
        df_target_customers)) == pd.DataFrame


 #--------- END TEST transform_target_customers function ---------


# --------- START TEST transform_customers function ---------

@pytest.mark.parametrize('df_address, df_demographic, expected_exception',
                         [
                             (pd.DataFrame(), pd.DataFrame(), KeyError),
                             (pd.DataFrame({'name': ['ricardo', 'nacho'], 'last_name': ['apellido1', 'apellido2']}),
                                 pd.DataFrame({'name': ['ricardo', 'nacho'], 'last_name': [
                                              'apellido1', 'apellido2']}), KeyError),
                         ]
                         )
def test_transform_customers(df_address, df_demographic, expected_exception):
    assert expected_exception == type(transform_customers(df_address, df_demographic))


def test_transform_customers_success():
    assert type(transform_customers(
        df_address, df_demographic)) == pd.DataFrame

# --------- END TEST transform_customers function ---------

