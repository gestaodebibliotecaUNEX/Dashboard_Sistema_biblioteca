# app.py
import streamlit as st
import config
import styles
from components import header, sidebar
from pages import inicio, minha_biblioteca, hub_page, placeholder_page

def main():
    """Função principal que executa a aplicação Streamlit."""
    config.set_page_config()
    styles.load_css()

    query_params = st.query_params
    page_from_query = query_params.get("page")

    if page_from_query:
        st.session_state.selected_page = page_from_query
        st.query_params.clear()
    
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "inicio"

    header.render_header()
    sidebar.render_sidebar()

    current_page_key = st.session_state.selected_page

    # Lógica de roteamento final
    if current_page_key == 'inicio':
        inicio.render_page()
    elif current_page_key == 'minha_biblioteca':
        minha_biblioteca.render_page()
    elif current_page_key in config.all_dashboards and current_page_key not in ['minha_biblioteca']:
        title, desc, _, _ = config.all_dashboards.get(current_page_key)
        placeholder_page.render_page(title, desc)
    elif any(current_page_key == nav_key for _, nav_key in config.navigation_options):
         page_name = [name for name, key in config.navigation_options if key == current_page_key][0]
         hub_page.render_page(current_page_key, page_name)
    else:
        st.error(f"Página não encontrada para a chave: '{current_page_key}'")

if __name__ == "__main__":
    main()