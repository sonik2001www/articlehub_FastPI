from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status

from src.articles.schemas import ArticleCreate, ArticleOut, ArticleUpdate
from src.articles.service import ArticlesService
from src.articles.dependencies import get_articles_service
from src.users.security import get_current_user_id

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.post("/", response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
async def create_article(
    payload: ArticleCreate,
    uid: str = Depends(get_current_user_id),
    svc: ArticlesService = Depends(get_articles_service),
):
    return await svc.create(uid, payload.title, payload.content, payload.tags)


@router.get("/", response_model=List[ArticleOut])
async def list_articles(
    search: Optional[str] = Query(None, alias="q"),
    tag: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    uid: str = Depends(get_current_user_id),
    svc: ArticlesService = Depends(get_articles_service),
):
    return await svc.list(author_id=uid, tag=tag, q=search, limit=limit, offset=offset)


@router.get("/{article_id}/", response_model=ArticleOut)
async def get_article(
    article_id: str,
    svc: ArticlesService = Depends(get_articles_service),
):
    return await svc.get(article_id)


@router.put("/{article_id}/", response_model=ArticleOut)
async def update_article(
    article_id: str,
    payload: ArticleUpdate,
    uid: str = Depends(get_current_user_id),
    svc: ArticlesService = Depends(get_articles_service),
):
    updates = payload.model_dump(exclude_none=True)
    return await svc.update(article_id, uid, updates)


@router.delete("/{article_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: str,
    uid: str = Depends(get_current_user_id),
    svc: ArticlesService = Depends(get_articles_service),
):
    await svc.delete(article_id, uid)
    return


@router.post("/{article_id}/analyze/", status_code=status.HTTP_202_ACCEPTED)
async def analyze_article_endpoint(
    article_id: str,
    uid: str = Depends(get_current_user_id),
    svc: ArticlesService = Depends(get_articles_service),
):
    return await svc.analyze(article_id, uid)

