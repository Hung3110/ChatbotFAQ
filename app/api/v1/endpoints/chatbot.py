# app/api/v1/endpoints/chatbot.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.core.config import settings
# Import ChatbotService thay vì repository cũ
from app.services.chatbot_service import ChatbotService 
from app.core.llamaindex_config import configure_llamaindex
import os

# Khởi tạo một router mới cho các endpoint liên quan đến chatbot
router = APIRouter()

# Khởi tạo LlamaIndex settings một lần khi module này được load
# (Mặc dù đã có trong lifespan, để ở đây đảm bảo nó được cấu hình)
configure_llamaindex()

# Khởi tạo service một lần duy nhất để tái sử dụng trong các request
# Đây là mẫu Singleton Pattern, giúp tiết kiệm tài nguyên
chatbot_service = ChatbotService()

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """
    Endpoint để người dùng tải lên một file tài liệu (PDF, DOCX).
    File sẽ được lưu lại và sau đó được xử lý để tạo index.
    """
    # Lấy đường dẫn thư mục upload từ file cấu hình
    upload_dir = settings.UPLOAD_DIR
    # Tạo thư mục nếu nó chưa tồn tại
    os.makedirs(upload_dir, exist_ok=True)
    # Tạo đường dẫn đầy đủ đến file sẽ được lưu
    file_path = os.path.join(upload_dir, file.filename)
    try:
        # Mở file ở chế độ ghi nhị phân (wb) và lưu nội dung
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        # Sau khi lưu, gọi service để tạo vector index cho file này
        chatbot_service.create_index_for_file(file_path)

    except Exception as e:
        # Nếu có lỗi, trả về lỗi 500
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu hoặc xử lý file: {e}")
        
    return {"message": "Tải và xử lý tài liệu thành công", "filename": file.filename}


@router.post("/ask")
async def ask(
    request: Request,
    db: Session = Depends(get_db) # Dependency Injection để lấy session database
):
    """
    Endpoint để người dùng đặt câu hỏi về một tài liệu đã được tải lên.
    """
    # Lấy dữ liệu JSON từ body của request
    data = await request.json()
    question = data.get("question")
    document_name = data.get("document_name")

    # Kiểm tra xem các trường cần thiết có tồn tại không
    if not all([question, document_name]):
        raise HTTPException(status_code=400, detail="Thiếu 'question' hoặc 'document_name' trong request")
    
    # Gọi service để lấy câu trả lời, truyền vào câu hỏi, tên tài liệu, và session db
    result = chatbot_service.get_answer(question, document_name, db)
    return result