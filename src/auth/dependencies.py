from fastapi import Depends

from src.db.mongo import get_db
from src.users.repository import UsersRepo
from src.common.mailers import CeleryMailer  # див. нижче
from src.auth.service import AuthService


def get_auth_service(db=Depends(get_db)) -> AuthService:
    """
    Creates an AuthService instance with all dependencies.
    """
    return AuthService(UsersRepo(db), CeleryMailer())
