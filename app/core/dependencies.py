# app/dependencies.py
from fastapi import Depends, HTTPException
from app.repositories.chatbot_repository import ChatbotRepository
from app.services.chatbot_service import ChatbotService
from app.database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os
from app.core.config import settings

# --- GHI CHÚ TỔNG QUAN ---
# File này định nghĩa các "dependencies" cho hệ thống Dependency Injection của FastAPI.
# Dependency Injection là một cơ chế giúp chia sẻ các tài nguyên chung (như session database,
# các đối tượng service/repository) một cách hiệu quả và có tổ chức giữa các endpoint.
#
# LƯU Ý QUAN TRỌNG: Dựa trên file `chatbot.py` bạn cung cấp, các dependency này
# có vẻ không được sử dụng trong logic hiện tại. File `chatbot.py` đang khởi tạo
# `ChatbotService()` trực tiếp. Có thể đây là một cấu trúc cũ hoặc dành cho một luồng phát triển khác.

def get_chatbot_repository() -> ChatbotRepository:
    """
    Dependency này có nhiệm vụ tạo và trả về một instance của ChatbotRepository.
    FastAPI sẽ gọi hàm này mỗi khi một endpoint yêu cầu nó.
    """
    # Khởi tạo một đối tượng repository mới.
    repo = ChatbotRepository()
    
    # Đoạn code dưới đây có vẻ dùng để tải một tài liệu mẫu khi khởi tạo.
    # Điều này hữu ích cho việc demo hoặc kiểm thử nhanh.
    upload_dir = settings.UPLOAD_DIR
    sample_file = os.path.join(upload_dir, "policy.pdf")
    
    if os.path.exists(sample_file):
        # LƯU Ý: Phương thức `load_documents` không được định nghĩa trong file
        # `chatbot_repository.py` bạn đã cung cấp. Đây có thể là code cũ
        # hoặc tên phương thức không chính xác.
        repo.load_documents(sample_file)
        
    return repo


async def get_chatbot_service(
    # FastAPI sẽ tự động gọi các hàm dependency được truyền vào đây.
    # 1. Gọi `get_chatbot_repository` để lấy `repo`.
    repo: ChatbotRepository = Depends(get_chatbot_repository),
    # 2. Gọi `get_db` để lấy session database `db`.
    db: AsyncSession = Depends(get_db),
) -> ChatbotService:
    """
    Dependency này tạo ra một instance của ChatbotService.
    Nó phụ thuộc vào hai dependency khác: `get_chatbot_repository` và `get_db`.
    """
    # LƯU Ý: Dòng này khởi tạo ChatbotService bằng cách truyền vào một `repo`.
    # Điều này ngụ ý rằng class `ChatbotService` có một constructor dạng `__init__(self, repo)`.
    # Việc này khác với cách `ChatbotService` được khởi tạo trong file `chatbot.py`
    # (nơi nó được gọi không có tham số). Đây là một điểm không nhất quán cần xem xét.
    return ChatbotService(repo)