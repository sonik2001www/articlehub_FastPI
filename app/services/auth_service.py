from app.db.repositories.users_repo import UsersRepo
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.errors import ConflictError, UnauthorizedError


class AuthService:
    def __init__(self, users_repo: UsersRepo, mailer):
        self.users = users_repo
        self.mailer = mailer

    async def register(self, email: str, password: str, name: str) -> dict:
        if await self.users.get_by_email(email):
            raise ConflictError("Email already registered")

        uid = await self.users.create(email, hash_password(password), name)

        await self.mailer.send_welcome(uid, email, name)
        return {"id": uid, "email": email, "name": name}

    async def login(self, email: str, password: str) -> dict:
        user = await self.users.get_by_email(email)
        if not user or not verify_password(password, user.get("password", "")):
            raise UnauthorizedError("Invalid credentials")

        uid = str(user["_id"])
        return {
            "access": create_access_token(uid, user["email"]),
            "refresh": create_refresh_token(uid, user["email"]),
        }

    async def profile(self, uid: str) -> dict:
        u = await self.users.get_by_id(uid)
        return {"id": str(u["_id"]), "email": u["email"], "name": u.get("name", "")}
