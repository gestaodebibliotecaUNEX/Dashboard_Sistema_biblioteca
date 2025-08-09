# utils.py
import streamlit as st
import pandas as pd
import base64

@st.cache_data
def get_base64_of_bin_file(bin_file):
    """Codifica um arquivo binário (como imagem) para Base64."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        # Não exibe erro no log se o ficheiro do logo não for encontrado
        return ""

@st.cache_data
def load_data(file_path):
    """
    Carrega e pré-processa os dados da planilha Excel.
    Retorna um DataFrame ou None em caso de erro.
    """
    try:
        df = pd.read_excel(file_path, header=3)
        df.dropna(subset=['Unidade', 'Curso', 'Titulo do Livro'], inplace=True)
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0).astype(int)
        df = df[df['Total'] > 0]
        return df
    except FileNotFoundError:
        st.error(f"Ficheiro de dados '{file_path}' não encontrado!", icon="🚨")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os dados: {e}")
        return None