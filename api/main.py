from fastapi import FastAPI
import uvicorn
from routers import dml

app = FastAPI()
app.include_router(dml.router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
