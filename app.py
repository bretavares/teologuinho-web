import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Diagnóstico Teologuinho", page_icon="📖")
st.title("📖 Diagnóstico do Teologuinho")

# 1. TESTE DOS SECRETS
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("ERRO: O nome 'GEMINI_API_KEY' não foi encontrado nos Secrets. Verifique se escreveu exatamente assim.")
        st.stop()
    
    CHAVE = st.secrets["GEMINI_API_KEY"]
    cliente = genai.Client(api_key=CHAVE)
    st.success("Conexão com os Secrets: OK!")
except Exception as e:
    st.error(f"Erro ao ler Secrets: {e}")
    st.stop()

# 2. TESTE DE COMUNICAÇÃO
if prompt := st.chat_input("Diga 'Oi' para testar a conexão"):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Teste com o modelo mais básico possível
            response = cliente.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            st.markdown(response.text)
            st.balloons()
        except Exception as e:
            # ISSO VAI MOSTRAR O ERRO REAL NA TELA
            st.error("--- ERRO DETECTADO ---")
            st.code(str(e)) 
            st.info("Copie o código acima e me mande para eu resolver para você.")
