# app/services/chatbot_service.py
import os
import urllib.parse
from sqlalchemy.orm import Session

# Import các thành phần cần thiết từ LlamaIndex
from llama_index.core import (
    VectorStoreIndex,          # Để tạo và làm việc với index vector
    SimpleDirectoryReader,     # Để đọc tài liệu từ file/thư mục
    StorageContext,            # Để quản lý ngữ cảnh lưu trữ (storage)
    load_index_from_storage,   # Để tải lại index đã được lưu
    PromptTemplate,            # Để tạo mẫu câu lệnh cho LLM
)
# Postprocessor để lọc các kết quả tìm kiếm dựa trên độ tương đồng
from llama_index.core.postprocessor import SimilarityPostprocessor

# Import model CSDL để lưu lịch sử chat
from app.models.database_models import QuestionHistory

# Thư mục để lưu trữ các index đã được tạo bởi LlamaIndex
INDEX_STORE_DIR = "llama_indexes"
os.makedirs(INDEX_STORE_DIR, exist_ok=True)

# --- PROMPT TEMPLATE TÙY CHỈNH ---
# Đây là một mẫu câu lệnh (prompt) để hướng dẫn AI cách trả lời.
# Nó giúp AI hiểu rõ vai trò và giới hạn của mình.
QA_TEMPLATE_STR = (
    "Bạn là một trợ lý AI hữu ích. Nhiệm vụ của bạn là trả lời câu hỏi về nội dung của một tài liệu của shop được cung cấp.\n"
    "Dưới đây là các thông tin được trích xuất từ tài liệu:\n"
    "---------------------\n"
    "{context_str}\n" # {context_str} sẽ được LlamaIndex điền vào bằng các đoạn văn bản liên quan
    "---------------------\n"
    "Dựa vào thông tin trên, hãy trả lời câu hỏi sau bằng tiếng Việt: {query_str}\n" # {query_str} là câu hỏi của người dùng
    "Nếu thông tin không có trong tài liệu hoặc không đủ để trả lời, hãy nói rằng: 'Tôi không tìm thấy thông tin này trong tài liệu.'\n"
    "Không được tự ý bịa đặt thông tin không có trong tài liệu.\n"
    "Trả lời: "
)
# Tạo đối tượng PromptTemplate từ chuỗi mẫu trên
QA_TEMPLATE = PromptTemplate(QA_TEMPLATE_STR)


class ChatbotService:

    def _get_index_path(self, document_name: str) -> str:
        """Hàm nội bộ: Tạo đường dẫn an toàn cho thư mục lưu index từ tên file."""
        # Mã hóa tên file để tránh các ký tự đặc biệt gây lỗi trên hệ thống file
        safe_dir_name = urllib.parse.quote_plus(document_name)
        return os.path.join(INDEX_STORE_DIR, safe_dir_name)

    def create_index_for_file(self, file_path: str):
        """Đọc một file, tạo và lưu trữ vector index cho file đó."""
        try:
            file_name = os.path.basename(file_path)
            index_path = self._get_index_path(file_name)

            # Sử dụng SimpleDirectoryReader để đọc nội dung từ file được chỉ định
            documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
            if not documents:
                print(f"Không có nội dung nào được trích xuất từ {file_name}")
                return

            # Tạo index vector từ các tài liệu đã đọc
            index = VectorStoreIndex.from_documents(documents)
            # Lưu index vào đĩa tại đường dẫn đã chỉ định để tái sử dụng sau này
            index.storage_context.persist(persist_dir=index_path)
            print(f"Đã tạo và lưu index cho {file_name} tại {index_path}")

        except Exception as e:
            print(f"Lỗi khi tạo index cho file {file_path}: {e}")
            raise # Ném lại lỗi để endpoint có thể xử lý

    def get_answer(self, question: str, document_name: str, db: Session = None) -> dict:
        """Tải index đã có và sử dụng Query Engine để trả lời câu hỏi."""
        index_path = self._get_index_path(document_name)
        if not os.path.exists(index_path):
            return {"answer": f"Không tìm thấy cơ sở kiến thức cho tài liệu: {document_name}. Vui lòng upload lại.", "sources": []}

        try:
            # Tạo ngữ cảnh lưu trữ từ thư mục chứa index
            storage_context = StorageContext.from_defaults(persist_dir=index_path)
            # Tải index từ storage
            index = load_index_from_storage(storage_context)
            
            # Tạo một query engine từ index
            query_engine = index.as_query_engine(
                similarity_top_k=5,  # Lấy top 5 kết quả tương đồng nhất
                # Lọc bỏ các kết quả có điểm tương đồng dưới 0.3
                node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.3)],
                # Sử dụng mẫu câu lệnh tùy chỉnh của chúng ta
                text_qa_template=QA_TEMPLATE
            )

            # Gửi câu hỏi đến query engine để nhận phản hồi
            response = query_engine.query(question)
            
            # Xử lý phản hồi: lấy câu trả lời và các nguồn (đoạn văn bản) đã được sử dụng
            answer = str(response) if response else "Tôi không tìm thấy thông tin này trong tài liệu."
            sources = [node.get_content() for node in response.source_nodes] if response and response.source_nodes else []
            result = {"answer": answer, "sources": sources}

        except Exception as e:
            print(f"Lỗi khi truy vấn: {e}")
            result = {"answer": "Đã xảy ra lỗi trong quá trình xử lý câu hỏi.", "sources": []}
        
        try:
            # Nếu có session database, lưu câu hỏi và câu trả lời vào lịch sử
            if db:
                history = QuestionHistory(question=question, answer=result["answer"])
                db.add(history)
                db.commit()
        except Exception as e:
            # Ghi lại lỗi nếu không lưu được vào CSDL, nhưng không làm ảnh hưởng đến câu trả lời trả về cho người dùng
            print(f"Lỗi khi lưu lịch sử: {e}")
            
        return result