from fastapi import UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path

rootPath = Path(__file__).parent.parent.parent


def uploadFile(file: UploadFile) -> JSONResponse:
    """_summary_

    Args:
        file (UploadFile): _description_

    Returns:
        JSONResponse: _description_
    """
    try:

        with open(f"{rootPath}/datasets/{file.filename}", 'wb') as myFile:
            # With second file name convert the first in bynary
            # and then read the binary
            content = file.file.read()
            myFile.write(content)
            myFile.close()
        return JSONResponse(content={
            'saved': True,
            'path': f'{rootPath}/{file.filename}'
        }, status_code=200)

    except FileNotFoundError:
        return JSONResponse(content={
            'saved': False
        }, status_code=404)

