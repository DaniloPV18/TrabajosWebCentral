import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_PARAMS = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "port": os.getenv("DB_PORT")
    }
    TZ = os.getenv("APP_TIMEZONE", "America/Guayaquil")

    LOGS_SERVICE_URL = os.getenv("LOGS_SERVICE_URL")
    LOGS_TIMEOUT = int(os.getenv("LOGS_TIMEOUT"),5)