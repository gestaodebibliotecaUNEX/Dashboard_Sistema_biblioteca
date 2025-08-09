# pages/placeholder_page.py
import streamlit as st

def render_page(title, description):
    """Renderiza uma página placeholder para dashboards em desenvolvimento."""
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.header(f"🚧 {title} 🚧")
    st.info("Este painel está em construção. Em breve, novos insights e funcionalidades estarão disponíveis aqui!", icon="🛠️")
    st.markdown(f"**O que esperar deste dashboard:** {description}")
    st.markdown('</div>', unsafe_allow_html=True)