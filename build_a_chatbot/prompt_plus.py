from config import model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage
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
            "Você é um assistente prestativo. Responda a todas as perguntas com o máximo de sua capacidade em {language}",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Define um novo grafo
workflow = StateGraph(state_schema=State)


# Define a função que chamará o modelo
def call_model(state: State):
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": response}


# Define um nó singular no grafo
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Adiciona memória
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": str(uuid.uuid4())}}
query = "Olá! Eu sou o Jim"
language = "inglês"

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages, "language": language}, config)
output["messages"][-1].pretty_print()  # Saída contendo todas as mensagens

query = "Qual é o meu nome?"

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages, "language": language}, config)
output["messages"][-1].pretty_print()  # Saída contendo todas as mensagens
