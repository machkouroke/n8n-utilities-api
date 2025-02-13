from pymongo import MongoClient
from pymongo.database import Database

from config.settings import get_settings


async def get_db() -> Database:
    settings = get_settings()
    uri = f"mongodb+srv://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}" \
          f"@{settings.MONGO_URL}/?retryWrites=true&w=majority"
    return MongoClient(uri)[settings.DB_NAME]
