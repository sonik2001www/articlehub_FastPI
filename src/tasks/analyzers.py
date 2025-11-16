from src.tasks.worker import analyze_article


class CeleryAnalyzer:
    async def enqueue(self, article_id: str) -> str:
        res = analyze_article.delay(article_id)
        return res.id
