# Imports
import os
from dotenv import load_dotenv

# Locate and load.env file
load_dotenv()


class Settings:
    """
    Class that contains all project settings.
    """
    PROJECT_NAME: str = "PROYECTO-FAST-API"
    PROJECT_VERSION: str = "1.0"
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT')
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" + \
        f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    DATASET_PATH: str = os.getenv('DATASET_PATH')
    FOLDER_SAVE_CSV_PATH = os.getenv('FOLDER_SAVE_CSV_PATH')


# Reference to class
settings = Settings()
