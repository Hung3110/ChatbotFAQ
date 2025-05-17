from fastapi import FastAPI
from app.api.v1.endpoints import chatbot
from app.core.config import settings
from app.database.db import engine
from app.models.database_models import Base

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(
    chatbot.router, prefix=f"{settings.API_V1_STR}/chatbot", tags=["chatbot"]
)


@app.on_event("startup")
async def startup_event():
    # Tạo bảng database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
