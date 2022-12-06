import sys
import os
import logging
import logging.config
from shutil import rmtree
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
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
    print((Path(__file__).parent.parent / "outputs").exists())
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
    """Test empty folder
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

    # Indicate psth of some file that you would like to upload to test
    path_file = "D:/ds_salaries_upd.xlsx"

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

        # Check if status code of reuqest is 200 ok,
        # and json include True into path key saved
        assert response.status_code == 200, logger.warning(
            'Test status code ->  Failure')
        assert response.json()['saved'] is True, logger.warning(
            'Test save is TRUE ->  Failure')

        logger.info('Test upload files -> Successfully Completed')

        # Delete folder that contain datasets when the test has finished
        rmtree(f"../datasets")


def test_upload_empty_file():
    """Test if uploaded file is empty. Verify status code
    of request and validation path into json response object
    """

    # Indicate psth of some file that you would like to upload to test
    path_file = "C:/Users/ale/Downloads/texto.txt"

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

        # Check if status code of reuqest is 404 not found,
        # and json include string 'File not found' into path key detail
        assert response.status_code == 404, logger.warning(
            'Test status code ->  Failure')
        assert response.json()['detail'] == 'File not found', logger.warning(
            'Test file not found ->  Failure')

        logger.info('Test upload empty file -> Successfully Completed')
