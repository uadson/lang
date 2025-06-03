from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from config import settings

settings.LANGSMITH_PROJECT
settings.LANGSMITH_API_KEY
settings.LANGSMITH_TRACING
settings.GOOGLE_API_KEY

# Usando modelo de linguagem
# Using Language Models

model = init_chat_model(
    str(settings.LLM_MODEL),
    model_provider="google-genai",
)

messages = [
    SystemMessage("Traduza o texto abaixo do Inglês para o Português do Brasil."),
    HumanMessage(
        """Note that ChatModels receive message objects as input and generate message objects as output. 
        In addition to text content, message objects convey conversational roles and hold important data, 
        such as tool calls and token usage counts."""
    ),
]

response = model.invoke(messages)

print(response)
print("-" * 100)
print(model.invoke("Hello"))
print("-" * 100)
print(model.invoke([{"role": "user", "content": "Hello"}]))
print("-" * 100)

## Streaming
for token in model.stream(messages):
    print(token.content, end="|")

print("-" * 100)

# Prompt Templates
"""
Vamos criar um modelo de prompt aqui. Ele receberá duas variáveis de usuário:

    language(idioma): O idioma para o qual o texto será traduzido.
    text(texto): O texto a ser traduzido.
    
Let's create a prompt template here. It will take in two user variables:

    language: The language to translate text into
    text: The text to translate
"""

system_template = "Traduza o texto abaixo do Inglês para o {language}."
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("human", "{text}")]
)

prompt = prompt_template.invoke({"language": "Português do Brasil", "text": "Hello"})

print(prompt)
print(prompt.to_messages())
print("-" * 100)

# Por fim, podemos invocar o modelo de bate-papo no prompt formatado:

response = model.invoke(prompt.to_messages())
print(response.content)
print("-" * 100)
