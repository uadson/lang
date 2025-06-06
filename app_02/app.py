from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from config import settings

settings.LANGSMITH_PROJECT
settings.LANGSMITH_API_KEY
settings.LANGSMITH_TRACING
settings.GOOGLE_API_KEY

model = init_chat_model(
    str(settings.LLM_MODEL),
    model_provider="google-genai",
)

human = HumanMessage(content="Hi! I'm Bob")
