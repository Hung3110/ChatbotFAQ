from fastapi import Depends, HTTPException
from app.repositories.chatbot_repository import ChatbotRepository
from app.services.chatbot_service import ChatbotService
from app.database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os
from app.core.config import settings


def get_chatbot_repository() -> ChatbotRepository:
    repo = ChatbotRepository()
    # Tải tài liệu mẫu (thay bằng file thực tế trong demo)
    upload_dir = settings.UPLOAD_DIR
    sample_file = os.path.join(upload_dir, "policy.pdf")
    if os.path.exists(sample_file):
        repo.load_documents(sample_file)
    return repo


async def get_chatbot_service(
    repo: ChatbotRepository = Depends(get_chatbot_repository),
    db: AsyncSession = Depends(get_db),
) -> ChatbotService:
    return ChatbotService(repo)
