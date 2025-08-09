 # styles.py
import streamlit as st

def load_css():
    """Carrega o CSS customizado para a aplicação."""
    st.markdown("""
    <style>
        /* Esconde a navegação automática da multipágina do Streamlit */
        [data-testid="stSidebarNav"] { display: none; }

        /* Estilo para os botões da barra lateral */
        [data-testid="stSidebar"] .stButton > button {
            background-color: #1B263B;
            border: 1px solid #415A77;
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #415A77;
            border-color: #90E0EF;
        }
        
        /* Estilo para os botões dos cards (que são links <a>) */
        .dashboard-button {
            display: block; width: 100%; padding: 0.75rem 1rem;
            background-color: #90E0EF; color: #0D1B2A !important;
            font-weight: bold; text-align: center; border-radius: 0.5rem;
            text-decoration: none !important; border: none;
            transition: background-color 0.2s, color 0.2s; box-sizing: border-box;
        }
        .dashboard-button:hover {
            background-color: #caf0f8; color: #0D1B2A !important;
        }

        /* ESTILOS GERAIS DA PÁGINA */
        .main .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }
        body, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background-color: #1B263B !important; color: #FFFFFF !important; }
        [data-testid="stSidebar"] { background-color: #0D1B2A !important; border-right: 2px solid #415A77 !important; }
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] li, [data-testid="stSidebar"] label { color: #FFFFFF !important; }
        .card-container, .kpi-card, .dashboard-card { background-color: #415A77 !important; border-radius: 8px !important; padding: 1.5rem !important; margin-bottom: 1.5rem !important; border: 1px solid #778DA9 !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1) !important; }
        .dashboard-card { display: flex; flex-direction: column; height: 100%; }
        .dashboard-card-content { flex-grow: 1; }
        .kpi-card h3 { font-size: 1rem !important; color: #E0E1DD !important; font-weight: 600 !important; margin: 0 !important; }
        .kpi-card h2 { font-size: 2.25rem !important; color: #FFFFFF !important; font-weight: 700 !important; margin: 0 !important; }
        .logo-img { height: 45px !important; object-fit: contain !important; background-color: #FFFFFF !important; border-radius: 8px !important; padding: 5px !important; box-shadow: 0 2px 4px rgba(0,0,0,0.5) !important; }
        .contact-info { background-color: #0D1B2A !important; padding: 15px !important; border-radius: 8px !important;
            margin-top: 20px !important; border: 1px solid #415A77 !important; }
        .contact-info h4 { color: #90E0EF !important; margin-bottom: 10px !important; }
        .contact-info p { color: #E0E1DD !important; margin: 5px 0 !important; }
        .dashboard-card h3 { color: #FFFFFF; margin-bottom: 10px; font-size: 1.25rem; }
        .dashboard-card p { color: #E0E1DD; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)