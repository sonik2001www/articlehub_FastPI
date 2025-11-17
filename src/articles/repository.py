from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Tuple, List, Dict, Any

from bson import ObjectId

from src.common.constants import ARTICLES_COL


class ArticlesRepo:

    def __init__(self, db):
        self.col = db[ARTICLES_COL]

    async def ensure_indexes(self) -> None:
        await self.col.create_index([("author", 1)])
        await self.col.create_index([("created_at", -1)])
        await self.col.create_index([("tags", 1)])

        await self.col.create_index([("title", "text"), ("content", "text")])

    # ---- CRUD ----------------------------------------------------------------
    async def create(self, author_id: str, title: str, content: str, tags: List[str]) -> str:
        now = datetime.now(timezone.utc)
        doc = {
            "title": title,
            "content": content,
            "tags": tags or [],
            "author": ObjectId(author_id),
            "created_at": now,
            "updated_at": now,
        }
        res = await self.col.insert_one(doc)
        return str(res.inserted_id)

    async def get_by_id(self, article_id: str) -> Optional[dict]:
        return await self.col.find_one({"_id": ObjectId(article_id)})

    async def update(self, article_id: str, updates: Dict[str, Any]) -> bool:
        if not updates:
            return False
        updates["updated_at"] = datetime.now(timezone.utc)
        res = await self.col.update_one({"_id": ObjectId(article_id)}, {"$set": updates})
        return res.matched_count == 1

    async def delete(self, article_id: str) -> bool:
        res = await self.col.delete_one({"_id": ObjectId(article_id)})
        return res.deleted_count == 1

    async def list(
        self,
        *,
        author_id: Optional[str] = None,
        tag: Optional[str] = None,
        q: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        newest_first: bool = True,
        projection: Optional[Dict[str, int]] = None,
    ) -> Tuple[List[dict], int]:
        filt: Dict[str, Any] = {}
        if author_id:
            filt["author"] = ObjectId(author_id)
        if tag:
            filt["tags"] = tag
        if q:
            filt["$text"] = {"$search": q}

        sort = [("created_at", -1 if newest_first else 1)]
        cur = self.col.find(filt, projection=projection).sort(sort).skip(offset).limit(limit)
        items = [doc async for doc in cur]
        total = await self.col.count_documents(filt)
        return items, total

    async def set_analysis(self, article_id: str, analysis: dict) -> bool:
        res = await self.col.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {"analysis": analysis, "updated_at": datetime.now(timezone.utc)}},
        )
        return res.matched_count == 1