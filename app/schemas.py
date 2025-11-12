from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


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


class ArticleCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class ArticleAnalysis(BaseModel):
    word_count: int
    unique_tags: int


class ArticleOut(BaseModel):
    id: str
    title: str
    content: Optional[str] = None
    tags: List[str] = []
    author: str
    created_at: str
    analysis: Optional[ArticleAnalysis] = None
