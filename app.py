import streamlit as st
import time
from google import genai
from google.genai import types

# ---------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------

st.set_page_config(
    page_title="Teologuinho - IEC Kairós",
    page_icon="📖"
)

st.markdown("""
<style>
.stApp { background-color: #000000; color: #ffffff; }
.stChatMessage { border-radius: 10px; border: 1px solid #333; }
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CONEXÃO COM A API
# ---------------------------------------------------

@st.cache_resource
def iniciar_cliente():
    try:
        chave = st.secrets["GEMINI_API_KEY"]
        return genai.Client(api_key=chave)
    except Exception:
        st.error("Erro: configure corretamente a GEMINI_API_KEY nos Secrets.")
        st.stop()

cliente = iniciar_cliente()

# ---------------------------------------------------
# PERSONA DO AGENTE
# ---------------------------------------------------

INSTRUCOES_SISTEMA = """
Você é o Teologuinho, assistente da Igreja Evangélica Congregacional Kairós.

Identidade:
Cristão reformado fiel às Escrituras e à tradição histórica.

Base doutrinária:
Cinco Solas da Reforma
Soberania de Deus
Doutrinas da Graça (TULIP)
Teologia da Aliança

Referências:
João Calvino
Martinho Lutero
John Knox
Jonathan Edwards
Charles Hodge
Herman Bavinck
Louis Berkhof
R.C. Sproul
John Piper
J.I. Packer

Estrutura obrigatória da resposta:

1. Resposta direta
2. Fundamentação bíblica (Livro Cap:Verso)
3. Explicação teológica clara
4. Aplicação prática
5. Sugestão de leitura reformada

Tom:
Respeitoso, pastoral e moderadamente formal.
"""

# ---------------------------------------------------
# INTERFACE
# ---------------------------------------------------

st.title("📖 Teologuinho")
st.caption("Fidelidade Bíblica — IEC Kairós")

# ---------------------------------------------------
# MEMÓRIA DO CHAT
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar histórico

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------
# FUNÇÃO DE RESPOSTA
# ---------------------------------------------------

def gerar_resposta(prompt):

    ultimo_erro = None

    for tentativa in range(3):

        try:

            time.sleep(1.5)

            response = cliente.models.generate_content(

                model="gemini-2.0-flash",

                contents=[prompt],

                config=types.GenerateContentConfig(
                    system_instruction=INSTRUCOES_SISTEMA,
                    temperature=0.3,
                    max_output_tokens=700
                )
            )

            # EXTRAÇÃO SEGURA DO TEXTO

            if response and response.candidates:

                texto = ""

                for parte in response.candidates[0].content.parts:

                    if hasattr(parte, "text"):
                        texto += parte.text

                if texto.strip():
                    return texto

            return "Não consegui gerar uma resposta agora. Tente novamente."

        except Exception as erro:

            ultimo_erro = erro

            time.sleep(6)

    return f"Ocorreu um erro ao consultar o servidor: {ultimo_erro}"

# ---------------------------------------------------
# CHAT
# ---------------------------------------------------

if prompt := st.chat_input("Em que posso ajudar, meu irmão?"):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        resposta = gerar_resposta(prompt)

        if resposta:
            st.markdown(resposta)
        else:
            st.warning("Não consegui gerar resposta.")

        st.session_state.messages.append(
            {"role": "assistant", "content": resposta}
        )
