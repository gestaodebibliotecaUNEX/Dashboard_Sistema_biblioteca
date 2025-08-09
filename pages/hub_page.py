# pages/hub_page.py
import streamlit as st
from config import all_dashboards
from components.sidebar import set_page

def render_page(page_key, page_name):
    """Renderiza uma página de 'hub' que mostra os dashboards disponíveis em uma categoria."""
    st.header(page_name)
    st.markdown(f"Explore os dashboards disponíveis na seção **{page_name.split(' ', 1)[1]}**.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filtra os dashboards que pertencem a esta página de hub
    dash_items = {key: val for key, val in all_dashboards.items() if val[2] == page_key}

    if not dash_items:
        st.info("Nenhum dashboard foi configurado para esta seção ainda. Em breve, novos painéis estarão disponíveis aqui!", icon="🛠️")
        return

    num_cols = 3
    # Agrupa os itens em linhas de `num_cols`
    grouped_items = [list(dash_items.items())[i:i + num_cols] for i in range(0, len(dash_items), num_cols)]

    for row in grouped_items:
        cols = st.columns(num_cols)
        for i, (key, (title, desc, _)) in enumerate(row):
            with cols[i]:
                # Usar um container para o cartão e outro para o botão garante alinhamento
                with st.container():
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <div class="dashboard-card-content">
                            <h3>{title}</h3>
                            <p>{desc}</p>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    
                    if st.button("Acessar Dashboard", key=f"btn_{key}", on_click=set_page, args=(key,)):
                        # A lógica de rerun é tratada pelo Streamlit após o callback on_click
                        pass