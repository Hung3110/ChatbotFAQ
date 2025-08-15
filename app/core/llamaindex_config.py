# app/core/llamaindex_config.py
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
import os

def configure_llamaindex():
    """
    Hàm này cấu hình các thành phần mặc định cho LlamaIndex.
    Nó sẽ được gọi một lần khi ứng dụng khởi động.
    Việc này đảm bảo mọi nơi trong code sử dụng LlamaIndex
    sẽ dùng chung một cấu hình LLM và model embedding.
    """
    # Cấu hình model ngôn ngữ lớn (LLM) sẽ được sử dụng để sinh câu trả lời
    Settings.llm = Gemini(
        model="models/gemini-1.5-flash", # Sử dụng model Flash của Gemini, tối ưu về tốc độ
        api_key=os.getenv("GOOGLE_API_KEY"), # Lấy API key từ biến môi trường
        temperature=0.1 # Giảm nhiệt độ để câu trả lời nhất quán và bám sát tài liệu hơn
    )
    # Cấu hình model embedding sẽ được sử dụng để tạo vector từ văn bản
    Settings.embed_model = GeminiEmbedding(
        model="models/embedding-001", # Model embedding của Google
        api_key=os.getenv("GOOGLE_API_KEY")
    )