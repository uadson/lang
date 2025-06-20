from config import model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
    trim_messages,
    AIMessage,
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.graph.message import add_messages
from typing import Sequence
from typing_extensions import Annotated, TypedDict

import uuid


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str


# Prompt
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um assistente prestativo. Responda a todas as perguntas com o máximo de sua capacidade em {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Gerênciamento do histórico de conversação
trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

messages = [
    SystemMessage(content="Você é um assistente prestativo"),
    HumanMessage(content="Olá! Eu sou o Joe"),
    AIMessage(content="Olá Joe! Como posso ajudar?"),
    HumanMessage(content="Eu gosto de programar em Python."),
    AIMessage(content="Que legal!"),
    HumanMessage(content="Qual é a raiz quadrada de 49?"),
    AIMessage(content="A raiz quadrada de 49 é 7."),
    HumanMessage(content="Obrigado!"),
    AIMessage(content="De nada!"),
    HumanMessage(content="Isto foi legal"),
    AIMessage(content="Que bom!"),
]

trimmer.invoke(messages)

# Define um novo grafo
workflow = StateGraph(state_schema=State)


# Define a função que chamará o modelo
def call_model(state: State):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke(
        {"messages": trimmed_messages, "language": state["language"]},
    )
    response = model.invoke(prompt)
    return {"messages": response}


# Define um nó singular no grafo
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Adiciona memória
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": thread_id}}
query = "Qual é o meu nome?"
language = "espanhol"

input_messages = messages + [HumanMessage(query)]
output = app.invoke({"messages": input_messages, "language": language}, config)
output["messages"][-1].pretty_print()  # Saída contendo todas as mensagens

thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": thread_id}}
query = "Qual foi o problema de matemática que perguntei?"
language = "espanhol"

input_messages = messages + [HumanMessage(query)]
output = app.invoke({"messages": input_messages, "language": language}, config)
output["messages"][-1].pretty_print()  # Saída contendo todas as mensagens
