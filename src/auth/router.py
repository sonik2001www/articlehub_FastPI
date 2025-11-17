from fastapi import APIRouter, Depends, status

from src.auth.schemas import UserCreate, LoginIn, UserOut, TokenPair
from src.auth.service import AuthService
from src.auth.dependencies import get_auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, svc: AuthService = Depends(get_auth_service)):
    return await svc.register(payload.email, payload.password, payload.name)


@router.post("/login/", response_model=TokenPair)
async def login(payload: LoginIn, svc: AuthService = Depends(get_auth_service)):
    return await svc.login(payload.email, payload.password)
