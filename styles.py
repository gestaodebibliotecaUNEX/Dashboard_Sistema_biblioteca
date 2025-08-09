# styles.py
import streamlit as st

def load_css():
    """Carrega o CSS customizado para a aplicação."""
    st.markdown("""
    <style>
          [data-testid="stSidebarNav"] {
            display: none;
        }       
        .main .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }
        body, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0c6c8f !important;
            color: #FFFFFF !important;
        }
                
        [data-testid="stSidebar"] {
            background-color: #056081 !important;
            border-right: 2px solid #415A77 !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] .st-emotion-cache-1b0udgb, [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .st-caption {
             color: #FFFFFF !important;
        }
        .card-container, .kpi-card, .dashboard-card {
            background-color: #415A77 !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            margin-bottom: 1.5rem !important;
            border: 1px solid #778DA9 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1) !important;
        }
        
        .dashboard-card {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .dashboard-card-content {
            flex-grow: 1; 
        }

        .kpi-card h3 { font-size: 1rem !important; color: #E0E1DD !important; font-weight: 600 !important; margin: 0 !important; }
        .kpi-card h2 { font-size: 2.25rem !important; color: #FFFFFF !important; font-weight: 700 !important; margin: 0 !important; }
        .logo-img { height: 45px !important; object-fit: contain !important; background-color: #FFFFFF !important;
            border-radius: 8px !important; padding: 5px !important; box-shadow: 0 2px 4px rgba(0,0,0,0.5) !important; }
        .contact-info { background-color: #0D1B2A !important; padding: 15px !important; border-radius: 8px !important;
            margin-top: 20px !important; border: 1px solid #415A77 !important; }
        .contact-info h4 { color: #90E0EF !important; margin-bottom: 10px !important; }
        .contact-info p { color: #E0E1DD !important; margin: 5px 0 !important; }
        .dashboard-card h3 { color: #FFFFFF; margin-bottom: 10px; font-size: 1.25rem; }
        .dashboard-card p { color: #E0E1DD; font-size: 0.9rem; }
        
        .dashboard-card .stButton>button {
            background-color: #90E0EF;
            color: #0D1B2A;
            width: 100%;
            font-weight: bold;
            margin-top: 1rem;
        }
        .dashboard-card .stButton>button:hover {
            background-color: #caf0f8;
            color: #0D1B2A;
        }
    </style>
    """, unsafe_allow_html=True)