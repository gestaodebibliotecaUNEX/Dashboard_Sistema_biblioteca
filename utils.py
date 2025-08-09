 # utils.py
import streamlit as st
import pandas as pd
import base64

# A função get_base64_of_bin_file continua igual...
@st.cache_data
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

# --- ALTERAÇÃO AQUI ---
@st.cache_data
def load_data(): # Removemos o argumento file_path
    """
    Carrega os dados do ficheiro Parquet otimizado.
    Retorna um DataFrame ou None em caso de erro.
    """
    file_path = "assets/dados_otimizados.parquet" # Aponta para o novo ficheiro
    try:
        # Usamos pd.read_parquet, que é muito mais rápido
        df = pd.read_parquet(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Ficheiro de dados '{file_path}' não encontrado! Execute o script 'converter.py' primeiro.", icon="🚨")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os dados: {e}")
        return None