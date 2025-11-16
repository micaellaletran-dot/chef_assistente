import streamlit as st
from google import genai
import os

# ==========================
# CONFIGURAÇÃO DO GEMINI
# ==========================

# 🛑 CORREÇÃO DE SEGURANÇA: NUNCA codifique a chave de API diretamente aqui.
# A melhor prática é usar st.secrets para carregar a chave de um arquivo secreto 
# (secrets.toml) localmente, ou da área "Secrets" do Streamlit Cloud.
try:
    # Tenta carregar a chave usando st.secrets
    # O Streamlit usa o nome da variável de ambiente definida em 'Secrets'
    # Vamos assumir que o nome da chave é 'GEMINI_API_KEY' (Boa Prática).
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    # Se a chave não for encontrada nos secrets (ex: testando localmente sem secrets.toml)
    # Tenta usar uma variável de ambiente do sistema (para teste local avançado)
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Se a chave ainda não for encontrada, mostre um erro crítico.
    st.error("Erro de Configuração: Chave de API do Gemini não encontrada. Por favor, configure a chave 'GEMINI_API_KEY' nos Streamlit Secrets.")
    # Interrompe a execução do resto do app se a chave for vital
    st.stop()

# Configure o cliente Gemini APÓS a verificação da chave
genai.Client(api_key=api_key)

# O modelo 'gemini-pro' foi renomeado para 'gemini-2.5-flash' para uma experiência mais rápida e econômica.
# Recomenda-se o uso do método 'generate_content' diretamente do cliente.
# model = genai.GenerativeModel("gemini-2.5-flash") # Não é mais necessário instanciar o modelo assim
# Você pode chamar genai.Client() diretamente para acessar o serviço.


# ==========================
# FUNÇÃO PRINCIPAL
# ==========================
def gerar_receita(ingredientes):
    # O prompt está excelente! Adicionei uma pequena melhoria para torná-lo ainda mais claro.
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
        # Usa o método generate_content() do cliente configurado
        client = genai.Client(api_key=api_key)
        
        resposta = client.models.generate_content(
            model='gemini-2.5-flash', # Recomendado: mais rápido e eficiente
            contents=prompt
        )
        return resposta.text
    except Exception as e:
        # Captura qualquer erro de API ou conexão
        return f"Ocorreu um erro ao chamar a API do Gemini: {e}"


# ==========================
# INTERFACE STREAMLIT
# ==========================

st.title("🍳 Chef Assistente – Gere receitas com o que você tem!")

# O st.write abaixo está bem colocado.
st.write("Digite os ingredientes que você tem na geladeira separados por vírgula.")

# Use st.text_area para mais espaço e melhor UX em inputs longos.
ingredientes = st.text_area("Ingredientes:", placeholder="Ex: ovo, tomate, queijo, pão velho")

if st.button("Gerar Receita"):
    if ingredientes.strip() == "":
        st.error("Digite pelo menos 1 ingrediente.")
    else:
        with st.spinner("Criando sua receita mágica..."):
            receita = gerar_receita(ingredientes)
            # st.success("Receita pronta!") # Removido para não poluir a tela.
            st.markdown(receita)