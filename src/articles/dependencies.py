from fastapi import Depends

from src.db.mongo import get_db
from src.articles.repository import ArticlesRepo
from src.articles.service import ArticlesService
from src.articles.analyzers import CeleryAnalyzer


def get_articles_service(db=Depends(get_db)) -> ArticlesService:
    """
    Compiles ArticlesService with repository and parser.
    """
    return ArticlesService(ArticlesRepo(db), analyzer=CeleryAnalyzer())