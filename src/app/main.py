from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import chat, bookings
from app.core.redis_memory import RedisMemory

def create_app() -> FastAPI:
    app = FastAPI(title="Conversational RAG API")

    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
    app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        app.state.memory = RedisMemory(redis_url)

    @app.on_event("shutdown")
    async def shutdown():
        await app.state.memory.close()

    return app

app = create_app()
