from config import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from typing import List, Literal, TypedDict


# --- 1. Definir o Estado do Grafo ---
# Um TypeDict para representar o estado da nossa aplicação.
# Um histórico de chat será a parte mutável do nosso estado.
class ChatState(TypedDict):
    chat_history: List[AIMessage | HumanMessage]
    input: str


# --- 2. Definir o prompt para o Chatbot ---
# ChatPromptTemplate estrutura a conversa, incluíndo o histórico do chat
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente de IA prestativo e amigável."),
        MessagesPlaceholder(
            variable_name="chat_history"
        ),  # Onde o histórico de mensagens será inserido.
        ("human", "{input}"),  # A nova entrada do usuário.
    ]
)


# --- 3. Definir o Nó 'chatbot' ---
# Este nó encapsula a lógica principal do chatbot.
# Ele recebe o estado atual, invoca o LLM e retorna a resposta e o histórico atualizado.
def chatbot_node(state: ChatState):
    print("--- Executando o nó 'chatbot' ---")
    chat_history = state.get("chat_history", [])
    user_input = state["input"]

    # Constrói a cadeia LangChain dentro do nó
    # Aqui não precisamos de RunnablePassthrough.assign para chat_history,
    # pois ele já está no estado e é passado diretamente para o prompt.
    chain = prompt | llm | StrOutputParser()

    # Invoca a cadeia com a entrada do usuário e o histórico de chat
    response_content = chain.invoke({"input": user_input, "chat_history": chat_history})

    # Adiciona a mensagem do usuário e a resposta da IA ao histórico
    # É crucial retornar o estado atualizado para a próxima iteração do grafo.
    updated_chat_history = chat_history + [
        HumanMessage(content=user_input),
        AIMessage(content=response_content),
    ]

    return {"chat_history": updated_chat_history, "input": user_input}


# --- 4. Construir o Grafo LangGraph ---
workflow = StateGraph(ChatState)

# Adiciona o nó 'chatbot' ao nosso grafo
workflow.add_node("chatbot", chatbot_node)

# Define o ponto de entrada do grafo
workflow.set_entry_point("chatbot")

# Define a transição: após executar o nó 'chatbot', sempre encerra (END) neste exemplo simples.
# Para agentes mais complexos, teríamos lógica condicional aqui.
workflow.add_edge("chatbot", END)

# Compila o grafo para uso
app = workflow.compile()

# --- 5. Função para interagir com o Chatbot ---
# Esta função agora interage com o aplicativo LangGraph.


def ask_chatbot_langgraph(
    user_input: str, chat_history: List[HumanMessage | AIMessage]
):
    # O estado inicial é criado com a entrada do usuário e o histórico existente.
    initial_state = {"input": user_input, "chat_history": chat_history}

    # Invoca o aplicativo LangGraph com o estado inicial
    # O output é uma lista de estados, pois um grafo pode ter múltiplos passos.
    # Para este grafo simples, esperamos apenas o estado final.
    final_state = app.invoke(initial_state)

    # Extrai o histórico de chat atualizado do estado final
    updated_chat_history = final_state["chat_history"]
    response = updated_chat_history[-1].content  # A última mensagem do AI é a resposta

    print(f"Você: {user_input}")
    print(f"Bot: {response}")
    print("-" * 30)

    return (
        updated_chat_history  # Retorna o histórico atualizado para a pŕoxima iteração
    )


# --- 6. Interação exemplo ---
if __name__ == "__main__":
    print(
        "Olá! Digite suas mensagens para o chatbot Gemini. Digite 'sair' para encerrar."
    )

    # Inicializa o histórico de chat
    current_chat_history = []

    while True:
        user_message = input("Sua mensagem: ")
        if user_message.lower() == "sair":
            break
        # Passa o histórico de chat atualizado a cada iteração
        current_chat_history = ask_chatbot_langgraph(user_message, current_chat_history)

    print("Conversa encerrada. Até a próxima!")
