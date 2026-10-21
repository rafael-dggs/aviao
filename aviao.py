
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configurações da API Groq
api_key = os.getenv("GROQ_API_KEY")
base_url = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1",
)
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Configuração da página: deve vir antes dos elementos visuais
st.set_page_config(
    page_title="Assistente IA",
    page_icon="✈️",
    layout="centered",
)

st.title("✈️ Assistente de Inteligência Artificial")
st.caption("Converse com seu assistente virtual.")

# Valida a chave da API
if not api_key:
    st.error(
        "GROQ_API_KEY não configurada. "
        "Adicione a chave ao arquivo .env."
    )
    st.stop()

# Inicializa o cliente uma única vez por execução do app
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

# Inicializa o histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Você é um assistente útil, preciso e didático. "
                "Responda em português, salvo solicitação contrária."
            ),
        }
    ]

# Exibe o histórico, sem mostrar a mensagem de sistema
for message in st.session_state.messages:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo para enviar mensagens
prompt = st.chat_input("Digite sua mensagem...")

if prompt:
    # Salva e exibe a mensagem do usuário
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Consulta a API e exibe a resposta
    with st.chat_message("assistant"):
        try:
            with st.spinner("Pensando..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                )

            answer = response.choices[0].message.content
            answer = answer or "A API retornou uma resposta vazia."

            st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            st.error(
                "Não foi possível consultar a API Groq. "
                "Verifique sua chave, o modelo e a conexão."
            )
            st.exception(error)
