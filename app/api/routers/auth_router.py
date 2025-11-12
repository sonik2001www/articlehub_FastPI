from fastapi import APIRouter, Depends, status
from app.schemas import UserCreate, UserOut, LoginIn, TokenPair
from app.db.mongo import get_db
from app.db.repositories.users_repo import UsersRepo
from app.services.auth_service import AuthService
from app.services.mailers import CeleryMailer
from app.deps import get_current_user_id

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_auth_service(db=Depends(get_db)) -> AuthService:
    return AuthService(UsersRepo(db), CeleryMailer())


@router.post("/register/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, svc: AuthService = Depends(get_auth_service)):
    return await svc.register(payload.email, payload.password, payload.name)


@router.post("/login/", response_model=TokenPair)
async def login(payload: LoginIn, svc: AuthService = Depends(get_auth_service)):
    return await svc.login(payload.email, payload.password)


@router.get("/profile/", response_model=UserOut)
async def profile(uid: str = Depends(get_current_user_id), svc: AuthService = Depends(get_auth_service)):
    return await svc.profile(uid)
