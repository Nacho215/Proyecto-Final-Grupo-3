"""In this module we have two functions, one of which is responsible for
taking a file and placing it in the local directory and uploading it to
Amazon S3. This process is executed in two ways: if the local directory
exists, the file is saved there, and if not, the directory is created and
the file is saved there. In either case, the file is also uploaded to 
Amazon S3.

In the case of the second function, get_csv_url_files, it obtains the 
path of each of the files in the outputs folder on S3 and returns it in 
a JSON.

Raises:
    HTTPException: if upload file is empty
    HTTPException: if outputs directory is empty

Returns:
    _type_: JSONResponse
"""

from fastapi import UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from pathlib import Path
from shutil import rmtree
import os
import pandas as pd
import logging
import logging.config
import boto3
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from libs.config import settings
from boto3.s3.transfer import S3Transfer

S3_KEY = settings.S3_KEY
S3_SECRET = settings.S3_SECRET
S3_BUCKET = settings.S3_BUCKET
S3_FOLDER_SAVE_CSV_PATH = settings.S3_FOLDER_SAVE_CSV_PATH
S3_FOLDER_SAVE_CSV = settings.S3_FOLDER_SAVE_CSV

s3 = boto3.client('s3')

s3 = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)
# Get root project root
rootPath = Path(__file__).parent.parent.parent

# Path level level
root = Path.cwd().parent
root = f'{root}/config_logs.conf'

# open file config
logging.config.fileConfig(root)
logger = logging.getLogger(__name__)


def uploadFile_s3(file: UploadFile) -> JSONResponse:
    """Function that upload file to s3 service

    Args:
        file (UploadFile): file to upload

    Returns:
        JSONResponse: request info, 'saved':bool,'s3_path':str
    """
    s3.upload_fileobj(file.file, S3_BUCKET, f'datasets/{file.filename}')
    return JSONResponse(content={
                'saved': True,
                's3_path': f'datasets/{file.filename}'
            }, status_code=200)


def uploadFile(file: UploadFile) -> JSONResponse:
    """Function that loads the file with the information to be processed.
    Args:
        file (UploadFile): file type CSV,JSON or XLXS
    Returns:
        JSONResponse: {'saved':Boolean,'path':filepath uploaded}
    """
    try:
        # Ask if database folder had been creted if not create it and save file
        if Path(f"{rootPath}/datasets").exists():
            with open(f"{rootPath}/datasets/{file.filename}", 'wb') as myFile:
                # With second file name convert the first in bynary
                # and then read the binary
                content = file.file.read()
                myFile.write(content)

                # Select all content into file, then Verify if
                # don't have content into file
                # and back cursor to the start
                myFile.seek(0, os.SEEK_END)
                isempty = myFile.tell() == 0
                myFile.seek(0)

                if isempty:
                    myFile.close()
                    rmtree(Path(__file__).parent.parent.parent / "datasets")
                    # logger.error('Failed -> File empty')
                    raise HTTPException(
                                status_code=status.HTTP_404_NOT_FOUND,
                                detail="File empty"
                            )
                myFile.close()
                # logger.info('File successfuly created')            
            return JSONResponse(content={
                'saved': True,
                'local_path': f'{rootPath}/datasets/{file.filename}',
            }, status_code=200)
        else:
            os.mkdir(f'{rootPath}/datasets')
            with open(f"{rootPath}/datasets/{file.filename}", 'wb') as myFile:
                content = file.file.read()
                myFile.write(content)

                # Select all content into file, then Verify if
                # don't have content into file
                # and back cursor to the start
                myFile.seek(0, os.SEEK_END)
                isempty = myFile.tell() == 0
                myFile.seek(0)

                if isempty:
                    # Close file to can remove datasets folder if file is empty
                    myFile.close()
                    rmtree(Path(__file__).parent.parent.parent / "datasets")
                    # logger.error('Failed -> File empty')
                    raise HTTPException(
                                status_code=status.HTTP_404_NOT_FOUND,
                                detail="File empty"
                            )

                myFile.close()
                # logger.info('File successfuly created')
            return JSONResponse(content={
                'saved': True,
                'local_path': f'{rootPath}/datasets/{file.filename}',
            }, status_code=200)
    except FileNotFoundError:
        # logger.error(f'Error File not found {FileNotFoundError}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )


def get_csv_url_files() -> dict:
    """Function that obtains the paths of the processed csv files.

    Returns:
        dict: dictionary with the paths its keys range from strings
        numerical and start from '0'.
    """

    response = s3.list_objects(
            Bucket=S3_BUCKET,
            Prefix=S3_FOLDER_SAVE_CSV
            )

    dfUrlDict = {}
    # Loop which gets each of the paths from the address
    # stored in the output_dir variable
    for index, objeto in enumerate(response['Contents']):
        # Index 0 is output folder name and it is no necesary
        if index > 0:
            # Create dictionary with file name as key
            dfUrlDict[objeto['Key'].split('/')[-1]] = objeto['Key']

    if len(dfUrlDict) == 0:
        # logger.error('Failed - Files not found')
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
                )

    return dfUrlDict

def local_data() -> dict:
    """Function that obtains the paths of the processed csv files.
    Returns:
        dict: dictionary with the paths its keys range from strings
        numerical and start from '0'.
    """

    output_dir = f'{rootPath}/outputs'
    output_dir = Path(output_dir)
    dictData = {}
    # Loop which gets each of the paths from the address
    # stored in the output_dir variable
    for fichero in output_dir.iterdir():
        # Create dictionary with file name as key
        dictData[fichero.name.split('.')[0]] = f'{rootPath}/outputs/{fichero.name}'

    if len(dictData) == 0:
        logger.error('Failed - Files not found')
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
                )

    return dictData