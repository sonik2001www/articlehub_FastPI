from typing import Protocol, Optional

from src.tasks.worker import analyze_article


class Analyzer(Protocol):
    async def enqueue(self, article_id: str) -> Optional[str]:
        ...


class CeleryAnalyzer:
    """
    Adapter over Celery-task `analyze_article`.
    """

    async def enqueue(self, article_id: str) -> Optional[str]:
        result = analyze_article.delay(article_id)
        return str(result.id) if hasattr(result, "id") else None
