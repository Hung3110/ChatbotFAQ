# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
# Import hàm cấu hình LlamaIndex từ module core
from app.core.llamaindex_config import configure_llamaindex
# Import router từ file chatbot trong thư mục endpoints
from app.api.v1.endpoints import chatbot

# Import thư viện để tải các biến môi trường từ file .env
from dotenv import load_dotenv

# >>> BƯỚC 1: THÊM IMPORT CHO CORS <<<
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() # Thực hiện tải biến môi trường

# asynccontextmanager và lifespan được dùng để quản lý các tác vụ
# cần thực hiện khi ứng dụng khởi động và kết thúc.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Code sẽ chạy một lần duy nhất lúc khởi động ứng dụng ---
    print("Ứng dụng đang khởi động...")
    # Gọi hàm để cấu hình các model LLM và Embedding cho toàn bộ ứng dụng
    configure_llamaindex()
    print("Đã cấu hình LlamaIndex xong!")
    
    # yield là điểm tạm dừng, code trong các endpoint sẽ chạy sau dòng này
    yield
    
    # --- Code sẽ chạy một lần duy nhất lúc tắt ứng dụng ---
    print("Ứng dụng đang tắt...")

# Khởi tạo đối tượng FastAPI và truyền vào hàm lifespan
# để quản lý vòng đời của ứng dụng.
app = FastAPI(
    title="Chatbot FAQ Backend",
    lifespan=lifespan
)

# >>> BƯỚC 2: THÊM CẤU HÌNH MIDDLEWARE CHO CORS <<<
# Danh sách các nguồn (trang web) được phép gọi đến API này
origins = [
    "http://localhost",
    "http://localhost:8080",  # Cổng mặc định của Spring Boot
    "http://127.0.0.1:8080",
    # Bạn có thể thêm các địa chỉ khác vào đây khi deploy
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Cho phép các nguồn đã liệt kê ở trên
    allow_credentials=True,
    allow_methods=["*"],          # Cho phép tất cả các phương thức: GET, POST, PUT, DELETE...
    allow_headers=["*"],          # Cho phép tất cả các loại header trong request
)
# >>> KẾT THÚC PHẦN THÊM MỚI <<<


# Thêm router của chatbot vào ứng dụng chính.
# Mọi endpoint trong chatbot.router sẽ có tiền tố /api/v1/chatbot
# và được nhóm vào tag "chatbot" trong giao diện Swagger/OpenAPI.
app.include_router(chatbot.router, prefix="/api/v1/chatbot", tags=["chatbot"])

# Endpoint gốc để kiểm tra xem API có hoạt động hay không.
@app.get("/")
def read_root():
    return {"message": "Welcome to the Chatbot API"}