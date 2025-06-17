from decouple import config
from langchain.chat_models import init_chat_model


class Settings:
    GOOGLE_API_KEY: str = config("GOOGLE_API_KEY")
    LANGSMITH_API_KEY: str = config("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: str = config("LANGSMITH_PROJECT")
    LANGSMITH_TRACING: bool = config("LANGSMITH_TRACING")
    LLM_MODEL: str = config("LLM_MODEL")


settings: Settings = Settings()

settings.LANGSMITH_PROJECT
settings.LANGSMITH_API_KEY
settings.LANGSMITH_TRACING
settings.GOOGLE_API_KEY

model = init_chat_model(
    str(settings.LLM_MODEL),
    model_provider="google-genai",
)
