from fastapi import APIRouter, Depends, status

from src.users.schemas import UserOut
from src.users.service import UsersService
from src.users.dependencies import get_users_service
from src.users.security import get_current_user_id

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_profile(uid: str = Depends(get_current_user_id), svc: UsersService = Depends(get_users_service)):
    return await svc.get_profile(uid)
