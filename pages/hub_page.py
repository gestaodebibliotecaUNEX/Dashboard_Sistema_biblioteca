 # pages/hub_page.py
import streamlit as st
from config import all_dashboards

def render_page(page_key, page_name):
    """Renderiza uma página de 'hub' que mostra os dashboards disponíveis em uma categoria."""
    st.header(page_name)
    st.markdown(f"Explore os dashboards disponíveis na seção **{page_name.split(' ', 1)[1]}**.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    dash_items = {key: val for key, val in all_dashboards.items() if val[2] == page_key}

    if not dash_items:
        st.info("Nenhum dashboard foi configurado para esta seção ainda. Em breve, novos painéis estarão disponíveis aqui!", icon="🛠️")
        return

    num_cols = 3
    grouped_items = [list(dash_items.items())[i:i + num_cols] for i in range(0, len(dash_items), num_cols)]

    for row in grouped_items:
        cols = st.columns(num_cols)
        for i, (key, (title, desc, _, url)) in enumerate(row):
            with cols[i]:
                # Card com título e descrição
                st.markdown(f"""
                <div class="dashboard-card">
                    <div class="dashboard-card-content">
                        <h3>{title}</h3>
                        <p>{desc}</p>
                    </div>
                </div>""", unsafe_allow_html=True)

                # Lógica unificada para criar o botão como um link
                link = ""
                target = ""
                icon = ""

                if url:
                    # CASO 1: Dashboard externo
                    link = url
                    target = "_blank"  # Abre em nova aba
                    icon = " ↗️"
                else:
                    # CASO 2: Dashboard interno
                    link = f"?page={key}" # Cria um link para a própria página com um parâmetro
                    target = "_self"   # Abre na mesma aba

                # Renderiza o botão, que é sempre um link <a> agora
                st.markdown(f'<a href="{link}" target="{target}" class="dashboard-button">Acessar Dashboard{icon}</a>', unsafe_allow_html=True)