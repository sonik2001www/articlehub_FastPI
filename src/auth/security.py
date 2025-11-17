from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from src.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _create_token(subject: dict, expires_delta: timedelta) -> str:
    to_encode = subject.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def create_access_token(user_id: str, email: str) -> str:
    return _create_token({"sub": user_id, "email": email, "type": "access"},

                         timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(user_id: str, email: str) -> str:
    return _create_token({"sub": user_id, "email": email, "type": "refresh"},
                         timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
