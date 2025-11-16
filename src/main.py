from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.auth.router import router as auth_router
from src.users.router import router as users_router
from src.articles.router import router as articles_router
from src.tasks.router import router as tasks_router
from src.common.error_handlers import setup_error_handlers


app = FastAPI(title=settings.APP_NAME)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- global error handlers ---
setup_error_handlers(app)

# --- routers ---
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(articles_router)
app.include_router(tasks_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
