
# main.py

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.http_router import app_router
from app.config import UVICORN_HOST, UVICORN_PORT

app = FastAPI(title="RoastOrder", version="1.0.1")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(app_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host = UVICORN_HOST, port = UVICORN_PORT, reload = True)