Chatbot FAQ Nội bộ Doanh nghiệp
Hệ thống hỏi đáp nội bộ (Chatbot FAQ) giúp nhân viên doanh nghiệp truy cập thông tin từ tài liệu nội bộ (PDF/DOC) một cách nhanh chóng và chính xác. Chatbot sử dụng FastAPI, LangChain, và RAG (Retrieval-Augmented Generation) để xử lý tài liệu và trả lời câu hỏi, tích hợp giao diện demo qua Streamlit.
Mục tiêu

Tiết kiệm thời gian: Nhân viên tìm thông tin trong vài giây thay vì tìm kiếm thủ công.
Tăng năng suất: Giảm tải cho bộ phận hỗ trợ (nhân sự, IT).
Dễ triển khai: Cấu trúc chuyên nghiệp, dễ tích hợp với Slack/Teams.
Dễ demo: Giao diện Streamlit và Swagger UI giúp trình diễn trực quan.

Công nghệ

FastAPI: Framework API hiệu suất cao.
LangChain/RAG: Xử lý tài liệu và trả lời dựa trên nội dung.
OpenAI: Mô hình GPT-4o-mini cho câu trả lời tự nhiên.
FAISS: Lưu trữ vector để tìm kiếm nhanh.
SQLAlchemy/PostgreSQL: Lưu lịch sử câu hỏi (tùy chọn).
Streamlit: Giao diện demo.


Yêu cầu

Python: 3.8 trở lên
PostgreSQL: Database để lưu lịch sử (tùy chọn)
OpenAI API Key: Đăng ký tại OpenAI
Thư viện: Xem requirements.txt

Cài đặt

Clone repository:
git clone <repository-url>
cd chatbot_faq_project


Cài đặt thư viện:
pip install -r requirements.txt


Tạo file .env:
PROJECT_NAME=Chatbot FAQ Backend
API_V1_STR=/api/v1
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/faq_db
OPENAI_API_KEY=your-openai-api-key
UPLOAD_DIR=app/static/uploads


Cài đặt PostgreSQL:

Cài PostgreSQL và tạo database faq_db.
Cập nhật DATABASE_URL trong .env.



Chạy ứng dụng

Chạy FastAPI:
uvicorn app.main:app --reload

hoặc
python -m uvicorn app.main:app --reload


Truy cập http://localhost:8000/docs để xem Swagger UI và thử API.


Chạy giao diện Streamlit:
streamlit run streamlit_app.py


Truy cập http://localhost:8501 để dùng giao diện.



Cách demo

Chuẩn bị tài liệu:

Tạo file PDF/DOC (ví dụ: policy.pdf chứa chính sách nhân sự).
Lưu vào app/static/uploads/ hoặc tải qua Streamlit.


Trình diễn:

Mở Streamlit (http://localhost:8501).
Nhập OpenAI API Key.
Tải file policy.pdf.
Đặt câu hỏi: “Nhân viên được nghỉ bao nhiêu ngày phép mỗi năm?”
Kết quả: Chatbot trả lời (ví dụ: “12 ngày phép mỗi năm”) với nguồn tài liệu.


Thuyết phục doanh nghiệp:

Nhấn mạnh: “Chatbot trả lời chính xác, tiết kiệm thời gian, dễ tích hợp.”
Hiển thị Swagger UI (/docs) để chứng minh API chuyên nghiệp.
Đề xuất thử nghiệm trên một phòng ban nhỏ.



API Endpoints

POST /api/v1/chatbot/ask: Đặt câu hỏi.
Request: {"question": "Câu hỏi của bạn"}
Response: {"answer": "Câu trả lời", "sources": ["Nguồn tài liệu"]}


POST /api/v1/chatbot/upload: Tải tài liệu (PDF/DOC).
Request: Form-data với file PDF/DOC.
Response: {"message": "Tải thành công", "filename": "policy.pdf"}



Mở rộng

Bảo mật: Thêm authentication với fastapi-users.
Tích hợp: Kết nối với Slack/Teams qua webhook.
Hiệu suất: Dùng Chroma thay FAISS cho tài liệu lớn.
Lịch sử: Phân tích câu hỏi nhân viên từ database.

Đóng góp

Fork repository và tạo pull request.
Báo lỗi qua Issues.

Liên hệ

