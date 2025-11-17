from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str


class TokenPair(BaseModel):
    access: str
    refresh: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str
