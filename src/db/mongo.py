from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from src.config import settings

_client: AsyncIOMotorClient | None = None
_sync_client: MongoClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URI)
    return _client


def get_sync_client() -> MongoClient:
    global _sync_client
    if _sync_client is None:
        _sync_client = MongoClient(settings.MONGO_URI)
    return _sync_client


async def get_db():
    client = get_client()
    db = client[settings.MONGO_DB]
    return db