from fastapi import FastAPI
import uvicorn
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),''))
from routers import endpoints

# Creat app and add routes (enpoints)
app = FastAPI()
app.include_router(endpoints.router)


if __name__ == "__main__":
    # Start uvicorn server, you can change port if you like
    uvicorn.run("apiMain:app", port=8000, reload=True)
