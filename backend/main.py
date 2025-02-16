from fastapi import FastAPI

from backend.routers.user import user_router


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_URL: str
    LLMWHISPERER_API_KEY: str
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
app = FastAPI()

app.include_router(user_router)
