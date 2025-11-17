from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.auth.exceptions import ConflictError, UnauthorizedError
from src.users.exceptions import UserNotFoundError
from src.articles.exceptions import (
    ArticleNotFoundError,
    ArticleForbiddenError,
    ArticleError,
)


def setup_error_handlers(app: FastAPI):
    """
    Register global handlers for domain errors.
    """

    # --- AUTH ---
    app.add_exception_handler(
        ConflictError,
        lambda r, e: JSONResponse({"detail": str(e)}, status_code=409),
    )

    app.add_exception_handler(
        UnauthorizedError,
        lambda r, e: JSONResponse({"detail": str(e)}, status_code=401),
    )

    # --- USERS ---
    app.add_exception_handler(
        UserNotFoundError,
        lambda r, e: JSONResponse({"detail": str(e)}, status_code=404),
    )

    # --- ARTICLES ---
    app.add_exception_handler(
        ArticleNotFoundError,
        lambda r, e: JSONResponse({"detail": str(e)}, status_code=404),
    )

    app.add_exception_handler(
        ArticleForbiddenError,
        lambda r, e: JSONResponse({"detail": str(e)}, status_code=403),
    )

    # fallback for all ArticleError
    app.add_exception_handler(
        ArticleError,
        lambda r, e: JSONResponse({"detail": str(e)}, status_code=400),
    )
