 # app.py
import streamlit as st
import config
import styles
from components import header, sidebar
# --- CORREÇÃO AQUI ---
# Voltamos a importar da pasta 'pages' para resolver o erro.
from pages import inicio, minha_biblioteca, hub_page, placeholder_page

def main():
    """Função principal que executa a aplicação Streamlit."""
    
    # 1. Configurações iniciais
    config.set_page_config()
    styles.load_css()

    # 2. Inicializa o estado da sessão para controle de navegação
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = 'inicio'

    # 3. Renderiza os componentes fixos da interface
    header.render_header()
    sidebar.render_sidebar()

    # 4. Roteamento: decide qual página renderizar com base no estado
    current_page_key = st.session_state.selected_page

    is_hub_page = any(current_page_key == nav_key for _, nav_key in config.navigation_options if nav_key != 'inicio')
    is_dashboard_page = current_page_key in config.all_dashboards

    if current_page_key == 'inicio':
        inicio.render_page()
    elif current_page_key == 'minha_biblioteca':
        minha_biblioteca.render_page()
        
    elif is_hub_page and not is_dashboard_page:
        page_name = [name for name, key in config.navigation_options if key == current_page_key][0]
        hub_page.render_page(current_page_key, page_name)
    elif is_dashboard_page:
        title, desc, _ = config.all_dashboards.get(current_page_key)
        placeholder_page.render_page(title, desc)
    else:
        st.error("Página não encontrada.")

if __name__ == "__main__":
    main()