class ArticleError(Exception):
    """Basic error for article domain."""


class ArticleNotFoundError(ArticleError):
    """Article not found."""


class ArticleForbiddenError(ArticleError):
    """Not authorized to perform action on article (not author)."""
