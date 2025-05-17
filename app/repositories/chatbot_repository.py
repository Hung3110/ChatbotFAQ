from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
from app.utils.document_loader import DocumentLoader


class ChatbotRepository:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.vector_store = None

    def load_documents(self, file_path: str):
        chunks = DocumentLoader.load_and_split(file_path)
        texts = [chunk.page_content for chunk in chunks]
        self.vector_store = FAISS.from_texts(texts, self.embeddings)

    def search(self, query: str, k: int = 3) -> list[str]:
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        results = self.vector_store.similarity_search(query, k=k)
        return [result.page_content for result in results]
