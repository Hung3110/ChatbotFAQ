from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Chatbot FAQ Backend"
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: str
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/faq_db"
    UPLOAD_DIR: str = "app/static/uploads"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
