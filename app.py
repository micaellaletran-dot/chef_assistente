import streamlit as st
from google import genai
import os

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Erro de Configuração: Chave de API do Gemini não encontrada. Por favor, configure a chave 'GEMINI_API_KEY' nos Streamlit Secrets.")
    st.stop()

genai.Client(api_key=api_key)

def gerar_receita(ingredientes):
    prompt = f"""
    Você é um chef 5 estrelas. Sua tarefa é criar uma receita fácil e rápida.
    USE APENAS os ingredientes fornecidos: "{ingredientes}".

    Se for absolutamente impossível criar uma receita razoável, diga exatamente o que está faltando.

    Formate sua resposta obrigatoriamente usando o formato Markdown a seguir:

    ## Título da Receita
    ### Ingredientes
    - [Item 1]
    - [Item 2]
    ### Modo de Preparo
    1. [Passo 1]
    2. [Passo 2]
    """

    try:
        client = genai.Client(api_key=api_key)
        
        resposta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return resposta.text
    except Exception as e:
        return f"Ocorreu um erro ao chamar a API do Gemini: {e}"

st.title("🍳 Chef Assistente – Gere receitas com o que você tem!")

st.write("Digite os ingredientes que você tem na geladeira separados por vírgula.")

ingredientes = st.text_area("Ingredientes:", placeholder="Ex: ovo, tomate, queijo, pão velho")

if st.button("Gerar Receita"):
    if ingredientes.strip() == "":
        st.error("Digite pelo menos 1 ingrediente.")
    else:
        with st.spinner("Criando sua receita mágica..."):
            receita = gerar_receita(ingredientes)
            st.markdown(receita)
