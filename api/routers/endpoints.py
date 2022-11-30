from fastapi import APIRouter, UploadFile, File
from repository import functionality

# Define router with sets
router = APIRouter(
    prefix="/dataset",
    tags=["DataSet"]
)


@router.post('/upload')
def upload_file(file: UploadFile = File(...)) -> UploadFile:
    """Endpoint in charge of receiving a file and processing
    the file upload to the system

    Args:
        file (UploadFile, optional): files to be uploaded via url of
        type csv, json or xlxs. Defaults to File(...).

    Returns:
        UploadFile: json file with information if the file
        was loaded or not in the system.
    """
    return functionality.uploadFile(file)


@router.get('/get_data')
def getData() -> dict:
    """Endpoint that returns the paths of the
    processed csv files

    Returns:
        dict: dictionary with each of the paths found in the
        outputs folder with csvs
    """
    return functionality.get_csv_url_files()
