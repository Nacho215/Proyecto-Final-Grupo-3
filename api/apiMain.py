from fastapi import FastAPI
import uvicorn
import logging
import logging.config
from pathlib import Path
from routers import endpoints

# Path level
root = Path.cwd().parent
root = f'{root}/config_logs.conf'
print(root)
# open file config
logging.config.fileConfig(root)
logger = logging.getLogger('api')

# Creat app and add routes (enpoints)
app = FastAPI()
app.include_router(endpoints.router)


if __name__ == "__main__":
    # Start uvicorn server, you can change port if you like
    logger.info('Starting FastApi')
    uvicorn.run("apiMain:app", port=8000, reload=True)
