from typing import Optional
from bson import ObjectId
from src.common.constants import USERS_COL


class UsersRepo:
    def __init__(self, db):
        self.col = db[USERS_COL]

    async def get_by_email(self, email: str) -> Optional[dict]:
        return await self.col.find_one({"email": email})

    async def get_by_id(self, uid: str) -> Optional[dict]:
        return await self.col.find_one({"_id": ObjectId(uid)})

    async def create(self, email: str, password_hash: str, name: str) -> str:
        res = await self.col.insert_one({"email": email, "password": password_hash, "name": name})
        return str(res.inserted_id)
