
# main.py

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from app.api import api_router
from app.config import UVICORN_HOST, UVICORN_PORT

app = FastAPI(title="RoastOrder", version="1.0.1", root_path="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host = UVICORN_HOST, port = UVICORN_PORT, reload = True)