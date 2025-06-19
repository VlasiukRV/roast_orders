from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

WORK_DIR = os.getenv("WORK_DIR")
UVICORN_HOST = os.getenv("UVICORN_HOST")
UVICORN_PORT = int(os.getenv("UVICORN_PORT"))
