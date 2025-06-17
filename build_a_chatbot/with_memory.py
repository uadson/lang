from config import model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
import uuid

# Define um novo grafo
workflow = StateGraph(state_schema=MessagesState)


# Define a função que chamará o modelo
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}


# Define um nó singular no grafo
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Adiciona memória
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": str(uuid.uuid4())}}

query = "Olá! Eu sou o Bob"

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()  # Saída contendo todas as mensagens

query = "Qual é o meu nome?"

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()  # Saída contendo todas as mensagens
