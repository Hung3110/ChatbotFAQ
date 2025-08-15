# chatbot_repository.py
# LƯU Ý: File này có vẻ là một phiên bản cũ hơn hoặc một thử nghiệm,
# sử dụng LangChain và FAISS. Logic hiện tại trong `chatbot_service.py`
# đang sử dụng LlamaIndex.

from langchain_community.vectorstores import FAISS
from app.utils.document_loader import DocumentLoader # (File này không được cung cấp)
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import urllib.parse # Thư viện để mã hóa tên file

class ChatbotRepository:
    def __init__(self):
        # Khởi tạo model embedding của Google thông qua LangChain
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        # Thư mục để lưu các index của FAISS
        self.vector_store_dir = "faiss_indexes"
        os.makedirs(self.vector_store_dir, exist_ok=True)

    def create_index_for_file(self, file_path: str):
        """Tạo index bằng LangChain và FAISS."""
        try:
            # Tải và chia nhỏ tài liệu
            chunks = DocumentLoader.load_and_split(file_path)
            if not chunks:
                print(f"Không có nội dung nào được trích xuất từ {file_path}")
                return
            
            # Lấy nội dung text từ các chunks
            texts = [chunk.page_content for chunk in chunks]
            # Tạo vector store FAISS từ các đoạn text và model embedding
            vector_store = FAISS.from_texts(texts, self.embeddings)
            
            file_name = os.path.basename(file_path)
            # Mã hóa tên file để tạo tên thư mục an toàn
            safe_dir_name = urllib.parse.quote_plus(file_name)
            index_path = os.path.join(self.vector_store_dir, safe_dir_name)

            # Lưu index FAISS vào đĩa
            vector_store.save_local(index_path)
            print(f"Đã tạo và lưu index cho {file_name} tại {index_path}")
            
        except Exception as e:
            print(f"Lỗi khi tạo index cho file {file_path}: {e}")

    def search(self, query: str, document_name: str, k: int = 3) -> list[str]:
        """Tìm kiếm các đoạn văn bản tương đồng trong index FAISS."""
        # Lấy đường dẫn index từ tên tài liệu
        safe_dir_name = urllib.parse.quote_plus(document_name)
        index_path = os.path.join(self.vector_store_dir, safe_dir_name)
        
        if not os.path.exists(index_path):
            raise ValueError(f"Không tìm thấy cơ sở kiến thức cho tài liệu: {document_name}. Vui lòng upload lại.")
        
        # Tải lại index FAISS từ đĩa
        vector_store = FAISS.load_local(
            index_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True # Cần thiết cho việc tải index FAISS
        )
        
        # Thực hiện tìm kiếm tương đồng
        results = vector_store.similarity_search(query, k=k)
        return [result.page_content for result in results]