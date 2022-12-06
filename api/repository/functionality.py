from fastapi import UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from pathlib import Path
from shutil import rmtree
import os
import logging
import logging.config

# Get root project root
rootPath = Path(__file__).parent.parent.parent

# # Logs config imports and logger set
# logging.config.fileConfig(f"{rootPath}/config_logs.conf",
#                           disable_existing_loggers=False)

# logger = logging.getLogger('simpleLogger')
# Path level level
root = Path.cwd().parent
root = f'{root}/config_logs.conf'
print(root)
# open file config
logging.config.fileConfig(root)
logger = logging.getLogger('api')


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
                    raise HTTPException(
                                status_code=status.HTTP_404_NOT_FOUND,
                                detail="File not found"
                            )
                myFile.close()
                logger.info('File successfuly created')
            return JSONResponse(content={
                'saved': True,
                'path': f'{rootPath}/datasets/{file.filename}'
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
                    raise HTTPException(
                                status_code=status.HTTP_404_NOT_FOUND,
                                detail="File not found"
                            )
                            
                myFile.close()
                logger.info('File successfuly created')
            return JSONResponse(content={
                'saved': True,
                'path': f'{rootPath}/datasets/{file.filename}'
            }, status_code=200)

    except FileNotFoundError:        
        logger.error(f'Error File not found {FileNotFoundError}')
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

    output_dir = f'{rootPath}/outputs'
    output_dir = Path(output_dir)
    dfUrlDict = {}
    # Loop which gets each of the paths from the address
    # stored in the output_dir variable
    for fichero in output_dir.iterdir():
        # Create dictionary with file name as key
        dfUrlDict[fichero.name.split('.')[0]] = f'{rootPath}/outputs/{fichero.name}'            

    if len(dfUrlDict) == 0:
        logger.error('Error - Files not found')
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
                )

    return dfUrlDict
