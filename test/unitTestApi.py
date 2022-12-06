import sys
import os
import logging
import logging.config
from shutil import rmtree
from pathlib import Path
<<<<<<< HEAD
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
=======
import pandas as pd
from pandas import ExcelWriter
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
>>>>>>> main
from fastapi.testclient import TestClient
from api.apiMain import app

# Path level
root = Path.cwd().parent
root = f'{root}/config_logs.conf'

# open file config
logging.config.fileConfig(root)
logger = logging.getLogger('test')
logger.info('beginning tests')

# Call testclient fastapi to make requests
client = TestClient(app)


def test_read_files():
    """Test if endpoint read csv processed files
    """
    name_files = ["customers.csv",
                  "target_customers.csv",
                  "transactions.csv",
                  "products.csv"]

    # If directory exists remove it and create new one to will be test
    if (Path(__file__).parent.parent / "outputs").exists():
        rmtree(Path(__file__).parent.parent / "outputs")
    else:
        os.mkdir(Path(__file__).parent.parent / "outputs")

    # Create mock files with some content to will be used by endpoint
    # to return them
    for name in name_files:
        with open(
                Path(__file__).parent.parent / f"outputs/{name}", "w") as file:
            file.write("Primera línea")
            file.close()

    response = client.get('/dataset/get_data')

    assert response.status_code == 200, logger.warning(
        'Test Status_code -> Failure')
    assert response.content != None, logger.warning(
        'Test content not empty ->  Failure')

    logger.info('Test read files -> Successfully Completed')


def test_read_files_not_found():
    """Test if the folder is empty
    """
    path = Path(__file__).parent.parent / "outputs"

    for file in path.iterdir():
        os.remove(file)

    response = client.get('/dataset/get_data')

    rmtree(path)

    dict_response = response.json()

    assert response.status_code == 404, logger.warning(
        'Test status code ->  Failure')
    assert dict_response['detail'] == 'File not found', logger.warning(
        'Test file not found ->  Failure')
    
    logger.info('Test read file not found -> successfully completed')


def test_upload_files():
    """Test upload file. Verify status code of request and validation path
    into json response object
    """
    # Create excel file with a litle dataframe for the upload tests
    df = pd.DataFrame({'Id': [1, 3, 2, 4],
                   'Nombre': ['Juan', 'Eva', 'María', 'Pablo'],
                   'Apellido': ['Méndez', 'López', 'Tito', 'Hernández']})
    df = df[['Id', 'Nombre', 'Apellido']]
    writer = ExcelWriter('test.xlsx')
    df.to_excel(writer, 'Hoja de datos', index=False)
    writer.save()
    writer.close()
    
    path_file = "test.xlsx" 

    # Read file as a binary
    with open(path_file, "rb") as file_upload:
        file = file_upload.read()

        response = client.post(
                "/dataset/upload",
                # Extract file name and save it throw the endpoint
                files={"file": (f"{file_upload.name.split('/')[-1]}",
                                file,
                                "multipart/form-data")}
                )
        file_upload.close()

        # Check if status code of reuqest is 200 ok,
        # and json include True into path key saved
        assert response.status_code == 200, logger.warning(
            'Test status code ->  Failure')
        assert response.json()['saved'] is True, logger.warning(
            'Test save is TRUE ->  Failure')

        logger.info('Test upload files -> Successfully Completed')

    # Delete folder that contain datasets when the test has finished
    rmtree("../datasets")
    os.remove("test.xlsx")


def test_upload_empty_file():
    """Test if uploaded file is empty. Verify status code
    of request and validation path into json response object
    """
    # Create generic empty file to test
    with open("ds_datas.xlsx", "w") as file:
        file.write("")
        file.close()

    # Indicate psth of some file that you would like to upload to test
    path_file = "ds_datas.xlsx"

    # Read file as a binary
    with open(path_file, "rb") as file_upload:
        file = file_upload.read()

        response = client.post(
                "/dataset/upload",
                # Extract file name and save it throw the endpoint
                files={"file": (f"{file_upload.name.split('/')[-1]}",
                                file,
                                "multipart/form-data")}
                )
        file_upload.close()

        # Check if status code of reuqest is 404 not found,
        # and json include string 'File not found' into path key detail
<<<<<<< HEAD
        assert response.status_code == 404, logger.warning(
            'Test status code ->  Failure')
        assert response.json()['detail'] == 'File not found', logger.warning(
            'Test file not found ->  Failure')

        logger.info('Test upload empty file -> Successfully Completed')
=======
        assert response.status_code == 404
        assert response.json()['detail'] == 'File not found'

    os.remove("ds_datas.xlsx")
>>>>>>> main
