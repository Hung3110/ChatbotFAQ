# app/database/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# In ra URL database để debug khi khởi động
print(f"[DEBUG] DATABASE_URL = {settings.DATABASE_URL}")

# Tạo một "engine" kết nối đến CSDL.
# Engine quản lý các kết nối (connections) đến CSDL.
# `echo=True` sẽ log tất cả các câu lệnh SQL được SQLAlchemy thực thi.
engine = create_engine(settings.DATABASE_URL, echo=True)

# Tạo một "Session factory". SessionLocal là một class.
# Mỗi instance của SessionLocal sẽ là một session (phiên làm việc) với CSDL.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Hàm này là một dependency cho FastAPI.
    Nó tạo ra một session CSDL mới cho mỗi request,
    yield session đó cho endpoint sử dụng, và sau đó đóng nó lại.
    Điều này đảm bảo session được quản lý đúng cách.
    """
    db = SessionLocal()
    try:
        yield db # Trả về session cho endpoint
    finally:
        db.close() # Đóng session sau khi request hoàn tất