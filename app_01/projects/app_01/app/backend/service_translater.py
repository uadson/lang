from config import settings
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

API_KEY = settings.PROVIDER_API_KEY
MODEL = settings.LLM_MODEL
MODEL_PROVIDER = settings.MODEL_PROVIDER


class Translater:
    def __init__(self):
        self.llm_model = self.load_model()
        self.system_template = "You are a helpful assistant that translates from {input_language} to {output_language}."

    def load_model(self):
        model = init_chat_model(
            str(MODEL),
            model_provider=str(MODEL_PROVIDER),
        )

        return model

    def translate(self, text, input_language, output_language):
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.system_template), ("human", "{text}")]
        )
        prompt = prompt_template.invoke(
            {
                "input_language": input_language,
                "output_language": output_language,
                "text": text,
            }
        )
        response = self.llm_model.invoke(prompt.to_messages())
        return response.content


translater: Translater = Translater()
