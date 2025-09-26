import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Coder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_PROMPT ="""
Você é o "IA Coder", um assistente de IA especialista em programação, com foco principal em Python. Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
1.  **Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com código.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

with st.sidebar:
    st.title("🤖 AI Coder")
    st.markdown("Um assistente de IA focado em programção Python para ajudar iniciantes.")

    groq_api_key = st.text_input(
        "Insira sua API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    st.markdown("___")

st.title("AI Coder")
st.title("Assistente Pessoal de programação Python 🐍")
st.caption("Faça sua pergunta sobre Linguagem Python e obtenha código, explicações e referências.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = None

if groq_api_key:
    try:
        client = Groq(api_key = groq_api_key)
    except Exception as e:
        st.sidebar.error(e)
        st.stop()

elif st.session_state.messages:
    st.warning("Por favor, insira sua API Key Groq na barra lateral para continuar.")

if prompt := st.chat_input("Qual sua dúvida sobre Python?"):
    if client is None:
        st.warning("Por favor, insira sua API Key Groq na barra lateral para continuar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for message in st.session_state.messages:
        messages_for_api.append(message)

    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="openai/gpt-oss-20b",
                    temperature=0.7,
                    max_tokens=2048,
                )

                ai_resposta = chat_completion.choices[0].message.content

                st.markdown(ai_resposta)

                st.session_state.messages.append({"role": "assistant", "content": ai_resposta})

            except Exception as e:
                st.error(e)
