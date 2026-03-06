import streamlit as st
from google import genai
from google.genai import types

# 1. CONFIGURAÇÕES VISUAIS (Estilo Minimalista e Escuro)
st.set_page_config(page_title="Teologuinho - IEC Kairós", page_icon="📖")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stChatMessage { border-radius: 10px; border: 1px solid #333; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO COM A API
try:
    CHAVE_API = st.secrets["GEMINI_API_KEY"]
    cliente = genai.Client(api_key=CHAVE_API)
except Exception:
    st.error("Erro: Verifique a GEMINI_API_KEY nos Secrets do Streamlit.")
    st.stop()

# 3. PERSONA E DIRETRIZES TEOLÓGICAS
INSTRUCOES_SISTEMA = """
Você é o Teologuinho, um assistente especializado em Teologia Reformada Histórica.
Sua identidade: Cristão reformado, estudante de teologia, fiel às Escrituras.
Igreja: Congrega na Igreja Evangélica Congregacional Kairós (IEC Kairós), pastoreado pelo Pr. Cristiano Ribeiro e acompanhado pelo presbítero Hudson.

BASES: Cinco Solas, Soberania de Deus, Doutrinas da Graça, Teologia da Aliança.
AUTORES: Calvino, Lutero, Knox, Edwards, Hodge, Bavinck, Berkhof, Sproul, Piper, Packer.

ESTRUTURA DE RESPOSTA:
1. Resposta direta e clara.
2. Fundamentação bíblica (Livro, Cap:Ver).
3. Explicação teológica simples (didática).
4. Aplicação prática para a vida.
5. Sugestão de leitura (ex: Institutas, Packer, Sproul).

REGRAS: Linguagem respeitosa e moderadamente formal. Evite gírias ou humor irreverente.
Se não souber, indique que há diferentes interpretações.
"""

# 4. INTERFACE DO CHAT
st.title("📖 Teologuinho")
st.caption("Fidelidade Bíblica e Doutrina Reformada")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LÓGICA DE RESPOSTA (Correção do Erro 404)
if prompt := st.chat_input("Em que posso ajudar, irmão?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # MODELO ATUALIZADO PARA EVITAR O ERRO 404
            response = cliente.models.generate_content(
                model='gemini-1.5-flash', 
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=INSTRUCOES_SISTEMA,
                    temperature=0.3
                )
            )
            
            resposta_texto = response.text
            st.markdown(resposta_texto)
            st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
            
        except Exception as e:
            st.error(f"Erro de comunicação: {e}")
            st.info("Dica: Se o erro 404 persistir, tente trocar o nome do modelo para 'gemini-1.5-flash-8b'.")
