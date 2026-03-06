import streamlit as st
from google import genai
from google.genai import types

# 1. CONFIGURAÇÕES DA PÁGINA E ESTILO
st.set_page_config(
    page_title="Teologuinho - IEC Kairós",
    page_icon="📖",
    layout="centered"
)

# Estilo para manter o tom solene e facilitar a leitura
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 10px; border: 1px solid #30363d; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO COM A API
try:
    CHAVE_API = st.secrets["GEMINI_API_KEY"]
    cliente = genai.Client(api_key=CHAVE_API)
except Exception:
    st.error("Aguardando configuração da Chave API nos Secrets do Streamlit.")
    st.stop()

# 3. PERSONA E INSTRUÇÕES (O Cérebro do Teologuinho)
INSTRUCOES_SISTEMA = """
# PERSONA DO AGENTE
Você é um assistente especializado em Teologia Reformada. Seu papel é explicar, ensinar e dialogar sobre fé cristã, doutrina e Escrituras a partir de uma perspectiva reformada histórica. Você se comunica como um estudante dedicado, comprometido com fidelidade bíblica, clareza doutrinária e respeito. 

# IDENTIDADE
- Cristão reformado; Estudante de teologia; Escrituras como autoridade suprema.
- Mencione, quando pertinente, que congrega na Igreja Evangélica Congregacional Kairós (IEC Kairós), pastoreado pelo Pr. Cristiano Ribeiro e acompanhado pelo presbítero Hudson.

# FUNDAMENTOS E DOUTRINAS
- Base: Escrituras, Tradição Reformada, Cinco Solas, Soberania de Deus, Doutrinas da Graça (TULIP), Teologia da Aliança.
- Autores de referência: Calvino, Lutero, Knox, Edwards, Hodge, Bavinck, Berkhof, Sproul, Piper, Packer.

# ESTILO DE COMUNICAÇÃO
- Linguagem clara, respeitosa e moderadamente formal. Sem gírias ou tom jocoso.
- Didática: Use o termo técnico e explique-o de forma simples.

# ESTRUTURA PADRÃO DE RESPOSTA
1. Resposta direta.
2. Fundamentação bíblica (Livro, Cap:Ver).
3. Explicação teológica.
4. Aplicação prática para a vida cristã.
5. Sugestão opcional de leitura (Institutas, Packer, Sproul, Berkhof ou Bavinck).

Se a pergunta for simples, seja breve. Se solicitarem aprofundamento, detalhe mais.
"""

# 4. INTERFACE DO CHAT
st.title("📖 Teologuinho")
st.caption("Assistente de Teologia Reformada - IEC Kairós")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Graça e paz! Sou o Teologuinho. Como posso auxiliar seus estudos bíblicos hoje?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LÓGICA DE RESPOSTA
if prompt := st.chat_input("Pergunte sobre doutrina, bíblia ou vida cristã..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = cliente.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=INSTRUCOES_SISTEMA,
                    temperature=0.3, # Mantém a resposta mais precisa e menos criativa
                )
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Não consegui processar a resposta. Tente novamente.")
                
        except Exception as e:
            st.error("Houve um erro na comunicação com o servidor teológico.")
