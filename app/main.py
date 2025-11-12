from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers.auth_router import router as auth_router
from app.api.routers.articles_router import router as articles_router
from app.api.error_handlers import setup_error_handlers
from app.api.routers.tasks_router import router as tasks_router

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_error_handlers(app)

app.include_router(auth_router)
app.include_router(articles_router)
app.include_router(tasks_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
