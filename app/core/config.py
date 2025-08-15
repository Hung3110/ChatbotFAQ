# app/core/config.py
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Tải các biến từ file .env vào môi trường
load_dotenv()

class Settings(BaseSettings):
    """
    Lớp này dùng để quản lý các cấu hình của ứng dụng.
    Pydantic sẽ tự động đọc các biến từ môi trường (environment variables)
    hoặc từ file .env để gán giá trị cho các thuộc tính.
    """
    PROJECT_NAME: str = "Chatbot FAQ Backend"
    API_V1_STR: str = "/api/v1"
    
    # Đọc GOOGLE_API_KEY từ môi trường, có thể là None
    GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")

    # Đọc DATABASE_URL từ môi trường (ví dụ: "sqlite:///./test.db")
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    
    # Thư mục để lưu các file được người dùng tải lên
    UPLOAD_DIR: str = "app/static/uploads"

    class Config:
        # Chỉ định file env để Pydantic đọc
        env_file = ".env"
        env_file_encoding = "utf-8"

# Tạo một instance của Settings để sử dụng trong toàn bộ ứng dụng
settings = Settings()