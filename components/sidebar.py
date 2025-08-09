# components/sidebar.py
import streamlit as st
from datetime import datetime
from config import navigation_options

def set_page(page_key):
    """Callback para definir a página atual no estado da sessão."""
    st.session_state.selected_page = page_key

def render_sidebar():
    """Renderiza a barra lateral com os botões de navegação e informações de contato."""
    st.sidebar.markdown("### Navegação")
    for option_name, option_key in navigation_options:
        # O on_click garante que a página mude antes do rerun
        st.sidebar.button(
            option_name, 
            key=f"sidebar_{option_key}", 
            on_click=set_page, 
            args=(option_key,),
            use_container_width=True
        )

    st.sidebar.markdown(f"""
    <div class="contact-info">
        <h4>Para maiores informações:</h4>
        <p>📧 gestaodebiblioteca@unex.edu.br</p>
        <p>🌐 https://www.uniftc.edu.br/servicos/biblioteca</p>
        <p><strong>Última atualização:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
    </div>
    """, unsafe_allow_html=True)