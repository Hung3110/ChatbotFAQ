from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.models.pydantic_models import (
    QuestionRequest,
    AnswerResponse,
    DocumentUploadResponse,
)
from app.services.chatbot_service import ChatbotService
from app.repositories.chatbot_repository import ChatbotRepository
from app.core.config import settings
from app.core.dependencies import (
    get_chatbot_service,
    get_chatbot_repository,
)
import os
import shutil

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest, service: ChatbotService = Depends(get_chatbot_service)
):
    return await service.get_answer(request.question)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    repo: ChatbotRepository = Depends(get_chatbot_repository),
):
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file PDF hoặc DOCX")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    repo.load_documents(file_path)
    return {"message": "Tài liệu đã được tải lên và xử lý", "filename": file.filename}
