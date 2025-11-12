from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.errors import ConflictError, UnauthorizedError


def setup_error_handlers(app: FastAPI):
    app.add_exception_handler(ConflictError, lambda r, e: JSONResponse({"detail": str(e)}, status_code=409))
    app.add_exception_handler(UnauthorizedError, lambda r, e: JSONResponse({"detail": str(e)}, status_code=401))
