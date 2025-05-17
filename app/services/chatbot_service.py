from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.repositories.chatbot_repository import ChatbotRepository
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database_models import QuestionHistory
from datetime import datetime


class ChatbotService:
    def __init__(self, repository: ChatbotRepository):
        self.repository = repository
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-4o-mini",
            temperature=0,
        )
        self.prompt = PromptTemplate(
            template="""Bạn là chatbot FAQ nội bộ doanh nghiệp. Trả lời câu hỏi bằng tiếng Việt, ngắn gọn, chính xác dựa trên thông tin sau. Nếu không tìm thấy thông tin, nói "Thông tin không có trong tài liệu."

            Thông tin: {context}
            Câu hỏi: {question}
            Trả lời: """,
            input_variables=["context", "question"],
        )

    async def get_answer(self, question: str, db: AsyncSession = None) -> dict:
        context = self.repository.search(question)
        if not context:
            result = {"answer": "Thông tin không có trong tài liệu", "sources": []}
        else:
            input_data = {"context": "\n".join(context), "question": question}
            answer = await self.llm.ainvoke(self.prompt.format(**input_data))
            result = {"answer": answer.content, "sources": context}

        # Lưu lịch sử (nếu có database)
        if db:
            history = QuestionHistory(question=question, answer=result["answer"])
            db.add(history)
            await db.commit()

        return result
