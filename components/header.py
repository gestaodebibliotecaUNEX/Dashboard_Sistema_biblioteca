# components/header.py
import streamlit as st
from utils import get_base64_of_bin_file

def render_header():
    """Renderiza o cabeçalho da aplicação com título e logos."""
    logo1_b64 = get_base64_of_bin_file("assets/image.png")
    logo2_b64 = get_base64_of_bin_file("assets/logo.png")
    logo3_b64 = get_base64_of_bin_file("assets/UNEX-LOGO.png")
    
    col_title, col_logo1, col_logo2, col_logo3 = st.columns([0.55, 0.15, 0.15, 0.15])
    with col_title:
        st.markdown('<h1 style="font-size: 2.1rem; color: #FFFFFF; font-weight: 700;">PAINÉIS DO SISTEMA DE BIBLIOTECA UNIFTC/UNEX</h1>', unsafe_allow_html=True)
    with col_logo1:
        if logo1_b64: st.markdown(f'<img src="data:image/png;base64,{logo1_b64}" class="logo-img">', unsafe_allow_html=True)
    with col_logo2:
        if logo2_b64: st.markdown(f'<img src="data:image/png;base64,{logo2_b64}" class="logo-img">', unsafe_allow_html=True)
    with col_logo3:
        if logo3_b64: st.markdown(f'<img src="data:image/png;base64,{logo3_b64}" class="logo-img">', unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)