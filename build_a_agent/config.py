from decouple import config
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch


class Settings:
    GOOGLE_API_KEY: str = config("GOOGLE_API_KEY")
    LANGSMITH_API_KEY: str = config("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: str = config("LANGSMITH_PROJECT")
    LANGSMITH_TRACING: bool = config("LANGSMITH_TRACING")
    LANGSMITH_ENDPOINT: str = config("LANGSMITH_ENDPOINT")
    LLM_MODEL: str = config("LLM_MODEL")
    TAVILY_API_KEY: str = config("TAVILY_API_KEY")
    LANGSMITH_PROJECT: str = config("LANGSMITH_PROJECT")


settings: Settings = Settings()

settings.LANGSMITH_PROJECT
settings.LANGSMITH_API_KEY
settings.LANGSMITH_TRACING
settings.LANGSMITH_ENDPOINT
settings.LANGSMITH_PROJECT
settings.GOOGLE_API_KEY
settings.TAVILY_API_KEY

model = init_chat_model(
    str(settings.LLM_MODEL),
    model_provider="google-genai",
)

# --- 1. Inicia modelo Gemini ---
llm = ChatGoogleGenerativeAI(
    model=settings.LLM_MODEL, google_api_key=settings.GOOGLE_API_KEY, temperature=0.7
)

# --- 2. Inicia o cliente tavily
tavily_client = TavilySearch(max_results=5, tavily_api_key=settings.TAVILY_API_KEY)
