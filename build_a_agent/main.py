from config import tavily_client, llm
from typing import List, Literal, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser


# --- 1. Tipo do estado ---
class ChatState(TypedDict):
    chat_history: List[HumanMessage | AIMessage]
    input: str


# --- 2. Prompt do Chat ---
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente útil e amigável."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)


# --- 3. Classificador ---
def classificator_node(state: ChatState) -> Literal["use_tavily", "normal_response"]:
    """
    Decide se a consulta do usuário requer uma busca na web.
    """
    text = state["input"].lower()

    # Lógica aprimorada: se a pergunta for factual, sobre os eventos atuais ou exigir informação externa.
    # Adicionamos mais termos e consideramos a intenção de buscar informações específicas.
    keywords_for_tavily = [
        "últimas",
        "hoje",
        "agora",
        "quem é",
        "o que é",
        "quando",
        "notícia",
        "atual",
        "informações sobre",
        "fatos sobre",
        "previsão do tempo",
        "onde fica",
        "notícias de",
        "acontecendo em",
        "qual o",
        "como está",
        "eleições",
        "mercado financeiro",
        "eventos de hoje",
    ]

    if any(keyword in text for keyword in keywords_for_tavily):
        print(
            f"DEBUG: Palavra-chave detectada: {', '.join([k for k in keywords_for_tavily if k in text])} -> Usando Tavily."
        )
        return "use_tavily"

    print("DEBUG: Nenhuma palavra-chave factual detectada -> Resposta normal.")
    return "normal_response"


# --- 4. Nó com Tavily ---
def use_tavily_node(state: ChatState) -> ChatState:
    """
    Executa uma busca na web usando Tavily e retorna a informação encontrada.
    """
    query = state["input"]
    print(f"🔎 Buscando na web via Tavily para: '{query}'")

    try:
        # A API TavilySearchResults retorna uma lista de dicionários com 'content'
        results = tavily_client.invoke({"query": query})
        print(f"Tipo: {type(results)}")
        # O resultado de TavilySearch pode ser uma lista de strings ou dicionários.
        # Se for uma lista de dicionários com 'content', você pode querer concatenar.
        # Caso contrário, dependendo do que `tavily_client.invoke` retorna, pode ser necessário ajustar.

        # Para fins deste exemplo, vamos assumir que o resultado é uma string com a resposta ou um resumo.
        # Em um caso real, você pode precisar iterar sobre 'results' e formatar.
        # Garante que a resposta seja texto
        if isinstance(results, str):
            info = results
        elif isinstance(results, dict) and "results" in results:
            info = " ".join([r["content"] for r in results["results"]])
        else:
            info = str(results)

        if not info:
            info = "Não encontrei uma resposta confiável na web."
            print("DEBUG: Tavily não retornou informações úteis.")
        else:
            print(f"DEBUG: Informação encontrada por Tavily: {str(info)[:150]}...")
            # Imprime os primeiros 150 caracteres

    except Exception as e:
        info = f"Ocorreu um erro ao buscar no Tavily: {e}"
        print(f"ERRO: {info}")

    updated_history = state["chat_history"] + [
        HumanMessage(content=query),
        AIMessage(content=info),  # A resposta do Tavily é a resposta do "bot" neste nó
    ]

    # O input original é mantido para que, se o fluxo continuar, ele ainda esteja disponível.
    # No entanto, como este nó leva ao END, o 'input' não será usado novamente neste fluxo.
    return {"chat_history": updated_history, "input": query}


# --- 5. Nó normal com LLM ---
def normal_response_node(state: ChatState) -> ChatState:
    """
    Gera uma resposta usando o LLM sem busca na web.
    """
    print("💬 Gerando resposta normal com o LLM...")
    chain = prompt | llm | StrOutputParser()

    response = chain.invoke(
        {"input": state["input"], "chat_history": state["chat_history"]}
    )

    updated_history = state["chat_history"] + [
        HumanMessage(content=state["input"]),
        AIMessage(content=response),
    ]

    # O input original é mantido.
    return {"chat_history": updated_history, "input": state["input"]}


def classificador_pass(state: ChatState) -> ChatState:
    return state


# --- 6. Montar o Grafo ---
workflow = StateGraph(ChatState)

workflow.add_node("classificador", classificador_pass)
workflow.add_node("use_tavily", use_tavily_node)
workflow.add_node("normal_response", normal_response_node)
workflow.set_entry_point("classificador")
workflow.add_conditional_edges(
    "classificador",
    classificator_node,
    {
        "use_tavily": "use_tavily",
        "normal_response": "normal_response",
    },
)


workflow.add_edge("use_tavily", END)
workflow.add_edge("normal_response", END)

app = workflow.compile()


# --- 7. Função de conversa ---
def chat_loop():
    chat_history = []
    print(
        "👋 Olá! Sou um assistente que pode buscar informações na web se precisar. Digite 'sair' para encerrar."
    )
    print("---")
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "tchau", "bye"]:
            print("Bot: Até a próxima! 👋")
            break

        state = {"input": user_input, "chat_history": chat_history}
        final_state = app.invoke(state)

        # O histórico de chat é atualizado dentro dos nós e retornado no final_state
        chat_history = final_state["chat_history"]

        # A última mensagem no histórico é a resposta do bot
        resposta = chat_history[-1].content
        print(f"Bot: {resposta}")
        print("-" * 40)


# --- 8. Executar ---
if __name__ == "__main__":
    # Testes rápidos (descomente para testar sem rodar o loop interativo)
    # print("--- Teste 1: Pergunta normal ---")
    # test_state_1 = {"input": "Qual é a capital da França?", "chat_history": []}
    # result_1 = app.invoke(test_state_1)
    # print(f"Bot (Teste 1): {result_1['chat_history'][-1].content}")
    # print("-" * 40)

    # print("--- Teste 2: Pergunta que requer busca ---")
    # test_state_2 = {"input": "Quais são as últimas notícias sobre IA?", "chat_history": []}
    # result_2 = app.invoke(test_state_2)
    # print(f"Bot (Teste 2): {result_2['chat_history'][-1].content}")
    # print("-" * 40)

    chat_loop()
