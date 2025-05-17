from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]


class DocumentUploadResponse(BaseModel):
    message: str
    filename: str
