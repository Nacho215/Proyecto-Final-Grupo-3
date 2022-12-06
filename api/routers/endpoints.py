import logging
import logging.config
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from repository import functionality

# second level
root = Path.cwd().parent
root = f'{root}/config_logs.conf'
# print(f'Endopoint{root}')
# open file config
logging.config.fileConfig(root)
logger = logging.getLogger('api')

# Define router with sets
router = APIRouter(
    prefix="/dataset",
    tags=["DataSet"]
)


@router.post('/upload')
def upload_file(file: UploadFile = File(...)) -> UploadFile:
    """Endpoint that recive a file and upload to de local file system

    Args:
        file (UploadFile, optional): files to be uploaded via url of
        type csv, json or xlxs. Defaults to File(...).

    Returns:
        UploadFile: json file with information if the file
        was loaded or not in the system and path where was upload.
    """
    logger.info('Function Upload -> Return file Uploaded')
    return functionality.uploadFile(file)


@router.get('/get_data')
def getData() -> dict:
    """Endpoint that returns the paths of the
    processed csv files

    Returns:
        dict: dictionary with each of the paths found in the
        outputs folder with csvs
    """
    logger.info('Funtion GetData -> Return path of file')
    return functionality.get_csv_url_files()
