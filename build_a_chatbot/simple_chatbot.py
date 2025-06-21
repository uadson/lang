from config import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory


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

# --- 3. Gerenciamento do Histórico de Chat (simples) ---
# Para este exemplo básico, vamos manter o histórico em uma lista python.
# Em aplicações reais a ferramenta como Memory do LangChain seria utilizada.
## chat_history = []
# ConversationBufferMemory armazena o histórico da conversa.
memory = ConversationBufferMemory(return_messages=True)

# --- 4. Construir a cadeia LangChain ---
# A cadeia conecta o prompt, o modelo LLM e um parser de saída.
chain = (
    RunnablePassthrough.assign(
        # chat_history=lambda x: chat_history  # Passa o histórico de chat atual
        chat_history=lambda x: memory.load_memory_variables({})[
            "history"
        ]  # Carrega o histórico da memória
    )
    | prompt
    | llm
    | StrOutputParser()
)


# --- 5. Função para interagir com o Chatbot ---
def ask_chatbot(user_input: str):
    ## global chat_history  # Indica que vamos modificar a variável global chat_history

    # Invoca a cadeia com a entrada do usuário
    response = chain.invoke({"input": user_input})

    # Adiciona a mensagem do usuário e resposta da IA ao histórico
    ## chat_history.append(HumanMessage(content=user_input))
    ## chat_history.append(AIMessage(content=response))

    # Salva a mensagem do usuário e a resposta do AI na memória
    memory.save_context({"input": user_input}, {"output": response})

    # Imprime a mensagem do usuário e a resposta da IA
    print(f"Você: {user_input}")
    print(f"Bot: {response}")
    print("-" * 30)


# --- 7. Interação Exemplo ---
if __name__ == "__main__":
    print(
        "Olá! Digite suas mensagens para o chatbot Gemini. Digite 'sair' para encerrar."
    )

    while True:
        user_message = input("Sua mensagem: ")
        if user_message.lower() == "sair":
            break
        ask_chatbot(user_message)

    print("Conversa encerrada. Até a próxima!")
