from typing import List, Optional, Dict, Any

from src.articles.repository import ArticlesRepo
from src.articles.exceptions import (
    ArticleNotFoundError,
    ArticleForbiddenError,
)


class ArticlesService:
    def __init__(self, repo: ArticlesRepo, analyzer=None):
        self.repo = repo
        self.analyzer = analyzer

    # ---- mapper to DTO dictionary ----
    def _to_out(self, doc: dict) -> dict:
        return {
            "id": str(doc["_id"]),
            "title": doc.get("title", ""),
            "content": doc.get("content"),
            "tags": doc.get("tags", []),
            "author": str(doc.get("author")) if doc.get("author") else None,
            "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
            "analysis": doc.get("analysis"),
        }

    # ---- use-cases ----

    async def create(self, author_id: str, title: str, content: str, tags: list[str]) -> dict:
        aid = await self.repo.create(author_id, title, content, tags)
        doc = await self.repo.get_by_id(aid)
        if not doc:
            raise ArticleNotFoundError("Article was not created")
        return self._to_out(doc)

    async def list(
        self,
        *,
        author_id: Optional[str] = None,
        tag: Optional[str] = None,
        q: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        newest_first: bool = True,
    ) -> List[dict]:
        items, _total = await self.repo.list(
            author_id=author_id,
            tag=tag,
            q=q,
            limit=limit,
            offset=offset,
            newest_first=newest_first,
        )
        return [self._to_out(x) for x in items]

    async def get(self, article_id: str) -> dict:
        doc = await self.repo.get_by_id(article_id)
        if not doc:
            raise ArticleNotFoundError("Article not found")
        return self._to_out(doc)

    async def update(self, article_id: str, editor_id: str, updates: Dict[str, Any]) -> dict:
        doc = await self.repo.get_by_id(article_id)
        if not doc:
            raise ArticleNotFoundError("Article not found")
        if str(doc.get("author")) != editor_id:
            raise ArticleForbiddenError("Only author can update")

        ok = await self.repo.update(article_id, updates)
        if not ok:
            return self._to_out(doc)

        doc = await self.repo.get_by_id(article_id)
        if not doc:
            raise ArticleNotFoundError("Article not found after update")
        return self._to_out(doc)

    async def delete(self, article_id: str, requester_id: str) -> None:
        doc = await self.repo.get_by_id(article_id)
        if not doc:
            return
        if str(doc.get("author")) != requester_id:
            raise ArticleForbiddenError("Only author can delete")

        await self.repo.delete(article_id)

    async def analyze(self, article_id: str, requester_id: str) -> dict:
        doc = await self.repo.get_by_id(article_id)
        if not doc:
            raise ArticleNotFoundError("Article not found")

        if str(doc.get("author")) != requester_id:
            raise ArticleForbiddenError("Only author can analyze")

        task_id = await self.analyzer.enqueue(article_id) if self.analyzer else None
        return {"status": "scheduled", "task_id": task_id}
