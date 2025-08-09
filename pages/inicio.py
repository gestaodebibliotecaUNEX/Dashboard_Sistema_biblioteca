# pages/inicio.py
import streamlit as st

def render_page():
    """Renderiza o conteúdo da página inicial."""

    st.image("assets/image.png", use_container_width=True)
    st.subheader("Bem-vindo ao Sistema de Bibliotecas")
    st.markdown("Use o menu à esquerda para navegar entre as diferentes seções e explorar os dashboards de análise de dados.")