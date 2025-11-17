from fastapi import Depends

from src.db.mongo import get_db
from src.users.repository import UsersRepo
from src.users.service import UsersService


def get_users_service(db=Depends(get_db)) -> UsersService:
    """
    Creates a UsersService with a repository.
    """
    return UsersService(UsersRepo(db))
