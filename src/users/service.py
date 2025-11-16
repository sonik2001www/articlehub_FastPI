from src.users.repository import UsersRepo
from src.users.exceptions import UserNotFoundError


class UsersService:
    def __init__(self, users_repo: UsersRepo):
        self.users = users_repo

    async def get_profile(self, uid: str) -> dict:
        user = await self.users.get_by_id(uid)
        if not user:
            raise UserNotFoundError(f"User {uid} not found")

        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "name": user.get("name", ""),
        }
