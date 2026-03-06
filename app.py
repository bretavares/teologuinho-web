import streamlit as st
from google import genai
from google.genai import types

# 1. ESTILO E CONFIGURAÇÃO (Preto e Branco conforme sua preferência)
st.set_page_config(page_title="Teologuinho - IEC Kairós", page_icon="📖")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stChatMessage { border-radius: 10px; border: 1px solid #333; }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO COM A API
try:
    CHAVE_API = st.secrets["GEMINI_API_KEY"]
    # Inicializa o cliente com a versão mais estável da API
    cliente = genai.Client(api_key=CHAVE_API)
except Exception:
    st.error("Erro: Verifique se a 'GEMINI_API_KEY' está correta nos Secrets.")
    st.stop()

# 3. PERSONA REFORMADA (Instruções do Sistema)
INSTRUCOES_SISTEMA = """
Você é o Teologuinho, assistente da Igreja Evangélica Congregacional Kairós (IEC Kairós).
Liderança: Pastoreado pelo Pr. Cristiano Ribeiro e acompanhado pelo presbítero Hudson.
Identidade: Cristão reformado, fiel às Escrituras e à tradição histórica.

BASES: Cinco Solas, Soberania de Deus, Doutrinas da Graça (TULIP), Teologia da Aliança.
REFERÊNCIAS: Calvino, Lutero, Knox, Edwards, Hodge, Bavinck, Berkhof, Sproul, Piper, Packer.

ESTRUTURA OBRIGATÓRIA DE RESPOSTA:
1. Resposta direta.
2. Fundamentação bíblica (Livro Cap:Ver).
3. Explicação teológica didática (explique termos técnicos).
4. Aplicação prática.
5. Sugestão de leitura reformada.

Tom: Respeitoso, moderadamente formal e pastoral.
"""

# 4. INTERFACE
st.title("📖 Teologuinho")
st.caption("Fidelidade Bíblica - IEC Kairós")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LÓGICA DE RESPOSTA (Ajustada para evitar erro 404)
if prompt := st.chat_input("Em que posso ajudar, meu irmão?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Trocamos para o modelo 2.0 que resolve o conflito de v1beta
            response = cliente.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=INSTRUCOES_SISTEMA,
                    temperature=0.3
                )
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Ocorreu um erro na geração da resposta. Tente novamente.")
                
        except Exception as e:
            # Se o 2.0 falhar, tentamos automaticamente a versão estável alternativa
            try:
                response_alt = cliente.models.generate_content(
                    model='gemini-1.5-flash-002',
                    contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=INSTRUCOES_SISTEMA)
                )
                st.markdown(response_alt.text)
                st.session_state.messages.append({"role": "assistant", "content": response_alt.text})
            except:
                st.error(f"Erro persistente no servidor do Google: {e}")
