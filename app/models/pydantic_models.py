# app/models/pydantic_models.py
from pydantic import BaseModel

# Các class này sử dụng Pydantic để định nghĩa "schema" (lược đồ dữ liệu)
# cho các request và response của API.
# FastAPI sẽ dùng chúng để:
# 1. Validate dữ liệu đầu vào.
# 2. Serialize dữ liệu đầu ra thành JSON.
# 3. Tự động tạo tài liệu API (Swagger/OpenAPI).

class QuestionRequest(BaseModel):
    """Schema cho body của request /ask."""
    question: str


class AnswerResponse(BaseModel):
    """Schema cho response của request /ask."""
    answer: str
    sources: list[str]


class DocumentUploadResponse(BaseModel):
    """Schema cho response của request /upload."""
    message: str
    filename: str