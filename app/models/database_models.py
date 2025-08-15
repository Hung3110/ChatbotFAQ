# app/models/database_models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# declarative_base() là một factory function trả về một class cơ sở
# mà các class model của chúng ta sẽ kế thừa từ nó.
Base = declarative_base()


class QuestionHistory(Base):
    """
    Đây là một model ORM của SQLAlchemy.
    Nó định nghĩa cấu trúc của bảng 'question_history' trong cơ sở dữ liệu.
    Mỗi instance của class này tương ứng với một hàng trong bảng.
    """
    # Tên của bảng trong CSDL
    __tablename__ = "question_history"
    
    # Định nghĩa các cột trong bảng
    id = Column(Integer, primary_key=True, index=True) # Khóa chính, tự động tăng
    question = Column(String, nullable=False) # Cột lưu câu hỏi, không được rỗng
    answer = Column(String, nullable=False) # Cột lưu câu trả lời, không được rỗng
    created_at = Column(DateTime, default=datetime.utcnow) # Thời gian tạo, mặc định là thời gian hiện tại (UTC)