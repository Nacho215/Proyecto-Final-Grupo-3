from fastapi import UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
import logging.config

# Get root project root
rootPath = Path(__file__).parent.parent.parent

print(f'{rootPath}/logs.conf')

# Logs config imports and logger set
logging.config.fileConfig(fname=f'{rootPath}/logs.conf',
                          disable_existing_loggers=False)

logger = logging.getLogger('loggerMain')


def uploadFile(file: UploadFile) -> JSONResponse:
    """Function that loads the file with the information to be processed.

    Args:
        file (UploadFile): file type CSV,JSON or XLXS

    Returns:
        JSONResponse: {'saved':Boolean,'path':filepath uploaded}
    """
    try:

        with open(f"{rootPath}/datasets/{file.filename}", 'wb') as myFile:
            # With second file name convert the first in bynary
            # and then read the binary
            content = file.file.read()
            myFile.write(content)
            myFile.close()
            logger.info('File created successfuly')
        return JSONResponse(content={
            'saved': True,
            'path': f'{rootPath}/{file.filename}'
        }, status_code=200)

    except FileNotFoundError:
        logger.error(f'Error File not found: {FileNotFoundError}')
        return JSONResponse(content={
            'saved': False
        }, status_code=404)


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
    for index, fichero in enumerate(output_dir.iterdir()):

        try:
            dfUrlDict[index] = f'{rootPath}/outputs/{fichero.name}'
        except Exception as e:
            logger.error(f'Error File not found: {e}')
            return JSONResponse(content={
                                'response': "File not found"
                                }, status_code=404)

    return dfUrlDict
