from langchain_core.messages import HumanMessage, AIMessage
from config import model
from pprint import pprint as pp


# Sem histórico
human = HumanMessage(content="Hi! I'm Bob")
response = model.invoke([human])
pp(response)

# Com histórico
response = model.invoke(
    [
        HumanMessage(content="Olá! Eu sou o Bob"),
        AIMessage(content="Olá Bob! Como posso ajudar?"),
        HumanMessage(content="Qual é o meu nome?"),
    ]
)
pp(response)
