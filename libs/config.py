import os
from dotenv import load_dotenv
from pathlib import Path

# The first thing we have to do is to locate where our .env
# What this does is to go back one folder where the .env file is located.
env_path = Path('.') / '.env'
# We load the .env file through env_path
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME:str = "PROYECTO-FAST-API"
    PROJECT_VERSION:str = "1.0"
    POSTGRES_USER:str = os.getenv('POSTGRES_USER')
    POSTGRES_DB:str = os.getenv('POSTGRES_DB')
    POSTGRES_PASSWORD:str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER:str = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT:str = os.getenv('POSTGRES_PORT')
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()