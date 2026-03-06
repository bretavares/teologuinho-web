import streamlit as st
import time
from google import genai
from google.genai import types

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Teologuinho - IEC Kairós", page_icon="📖")

st.markdown("""
<style>
.stApp { background-color: #000000; color: #ffffff; }
.stChatMessage { border-radius: 10px; border: 1px solid #333; }
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 2. CONEXÃO COM A API (COM CACHE PARA EVITAR MÚLTIPLAS CONEXÕES)

@st.cache_resource
def iniciar_cliente():
    try:
        chave = st.secrets["GEMINI_API_KEY"]
        return genai.Client(api_key=chave)
    except Exception:
        st.error("Erro: Verifique se a 'GEMINI_API_KEY' está correta nos Secrets.")
        st.stop()

cliente = iniciar_cliente()

# 3. PERSONA DO AGENTE

INSTRUCOES_SISTEMA = """
Você é o Teologuinho, assistente da Igreja Evangélica Congregacional Kairós.

Identidade:
Cristão reformado, fiel às Escrituras e à tradição histórica.

Bases teológicas:
Cinco Solas, Soberania de Deus, Doutrinas da Graça (TULIP), Teologia da Aliança.

Referências:
Calvino, Lutero, Knox, Edwards, Hodge, Bavinck, Berkhof, Sproul, Piper e Packer.

Estrutura obrigatória das respostas:

1. Resposta direta
2. Fundamentação bíblica (Livro Cap:Verso)
3. Explicação teológica clara
4. Aplicação prática
5. Sugestão de leitura reformada

Tom:
Respeitoso, pastoral e moderadamente formal.
"""

# 4. INTERFACE

st.title("📖 Teologuinho")
st.caption("Fidelidade Bíblica — IEC Kairós")

# MEMÓRIA DA CONVERSA
if "messages" not in st.session_state:
    st.session_state.messages = []

# MOSTRAR HISTÓRICO
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. FUNÇÃO PARA GERAR RESPOSTA COM RETRY AUTOMÁTICO

def gerar_resposta(prompt):

    for tentativa in range(3):

        try:

            # pequena pausa para evitar rate limit
            time.sleep(1.5)

            response = cliente.models.generate_content(

                model="gemini-1.5-flash-002",

                contents=prompt,

                config=types.GenerateContentConfig(
                    system_instruction=INSTRUCOES_SISTEMA,
                    temperature=0.3,
                    max_output_tokens=800
                )

            )

            if response.text:
                return response.text

        except Exception as erro:

            # espera antes de tentar novamente
            time.sleep(10)

            ultimo_erro = erro

    return f"Erro ao gerar resposta: {ultimo_erro}"

# 6. CHAT

if prompt := st.chat_input("Em que posso ajudar, meu irmão?"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        resposta = gerar_resposta(prompt)

        st.markdown(resposta)

        st.session_state.messages.append(
            {"role": "assistant", "content": resposta}
        )
