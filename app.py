 # app.py (Versão Final com Cabeçalho Escuro)

import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from streamlit_option_menu import option_menu

# --- CONFIGURAÇÃO INICIAL E ESTILOS ---

st.set_page_config(
    page_title="Dashboard Sistema de Bibliotecas",
    page_icon="🎓",
    layout="wide"
)

# CSS para customizações visuais
def load_css():
    st.markdown("""
    <style>
        .main .block-container { 
            padding-top: 2rem; 
            padding-bottom: 2rem;
        }
        
        /* --- ALTERADO: Cabeçalho com fundo escuro --- */
        .main-header {
            background-color: #012F6C; /* A cor escura aplicada apenas aqui */
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .main-header .logo { 
            height: 60px;
            object-fit: contain;
        }
        /* Cor do título dentro do header alterada para branco */
        .main-header .title { 
            font-size: 2.2rem; 
            font-weight: bold; 
            color: #FFFFFF; 
            text-align: center; 
        }

        /* Cartões de Métrica (KPIs) voltaram ao tema claro */
        .metric-card {
            background-color: #F8F9FA; 
            padding: 1.5rem; 
            border-radius: 10px;
            border-left: 6px solid #1f4e79; 
            margin-bottom: 1rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s ease-in-out;
        }
        .metric-card:hover {
            transform: scale(1.03);
        }
        .metric-card h3 { 
            font-size: 1.1rem; 
            color: #6c757d;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        .metric-card h2 { 
            font-size: 2.5rem; 
            color: #1f4e79; 
            font-weight: bold; 
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# --- FUNÇÕES AUXILIARES ---

@st.cache_data
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.warning(f"Arquivo de imagem não encontrado: {bin_file}")
        return ""

@st.cache_data
def load_data():
    try:
        file_path = "planilha_lyceum_e_minha_biblioteca.xlsx"
        df = pd.read_excel(file_path, header=3)
        df.dropna(subset=['Unidade', 'Curso', 'Titulo do Livro'], inplace=True)
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0).astype(int)
        return df
    except FileNotFoundError:
        st.error(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

# --- FUNÇÕES DE CONTEÚDO ---

def render_visao_geral(df_filtrado):
    st.subheader("Visão Geral (Unidade e Curso)")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card"><h3>📚 Total de Livros</h3><h2>{df_filtrado['Titulo do Livro'].nunique()}</h2></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><h3>👁️ Total de Visualizações</h3><h2>{df_filtrado['Total'].sum():,}</h2></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><h3>🏫 Unidades</h3><h2>{df_filtrado['Unidade'].nunique()}</h2></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card"><h3>🎓 Cursos</h3><h2>{df_filtrado['Curso'].nunique()}</h2></div>""", unsafe_allow_html=True)

    st.markdown("---")

    col_graf_1, col_graf_2 = st.columns(2)
    with col_graf_1:
        st.subheader("📊 Visualizações por Unidade", divider='blue')
        df_unidade = df_filtrado.groupby('Unidade')['Total'].sum().nlargest(10).reset_index()
        fig_unidade = px.bar(df_unidade, x='Total', y='Unidade', orientation='h', text='Total', title="Top 10 Unidades")
        # --- ALTERADO: Removido tema escuro do gráfico ---
        fig_unidade.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_title=None, xaxis_title="Total de Visualizações", height=400)
        st.plotly_chart(fig_unidade, use_container_width=True)
        
    with col_graf_2:
        st.subheader("🎯 Visualizações por Curso", divider='blue')
        df_curso = df_filtrado.groupby('Curso')['Total'].sum().nlargest(10).reset_index()
        fig_curso = px.pie(df_curso, values='Total', names='Curso', title="Top 10 Cursos", hole=0.4)
        # --- ALTERADO: Removido tema escuro do gráfico ---
        fig_curso.update_layout(height=400, legend_title_text='Cursos')
        st.plotly_chart(fig_curso, use_container_width=True)

    st.markdown("---")
    
    st.subheader("📖 Análise dos Livros Mais Visualizados", divider='blue')
    top_n = st.number_input("Selecione o número de livros para exibir:", min_value=5, max_value=50, value=20, step=5)
    
    df_livros = df_filtrado.groupby(['Titulo do Livro', 'Curso', 'Unidade'])['Total'].sum().nlargest(top_n).reset_index()
    fig_livros = px.bar(df_livros, x='Total', y='Titulo do Livro', orientation='h', color='Total', hover_data=['Curso', 'Unidade'])
    # --- ALTERADO: Removido tema escuro do gráfico ---
    fig_livros.update_layout(
        height=25 * top_n, 
        yaxis={'categoryorder':'total ascending'}, 
        yaxis_title=None, 
        xaxis_title="Total de Visualizações",
        title=f"Top {top_n} Livros Mais Visualizados"
    )
    st.plotly_chart(fig_livros, use_container_width=True)

    st.subheader("📋 Dados Detalhados", divider='blue')
    st.dataframe(df_filtrado.sort_values('Total', ascending=False), use_container_width=True, height=400)
    
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar dados filtrados (CSV)", csv, "dados_biblioteca_filtrados.csv", "text/csv", use_container_width=True, type="primary")

def render_minha_biblioteca():
    df = load_data()
    if df.empty: return

    st.sidebar.header("🔍 Filtros Interativos")
    unidades = ['Todas'] + sorted(df['Unidade'].unique().tolist())
    unidade_selecionada = st.sidebar.selectbox("Unidade:", unidades)
    
    if unidade_selecionada != 'Todas': cursos_filtrados = df[df['Unidade'] == unidade_selecionada]['Curso'].unique()
    else: cursos_filtrados = df['Curso'].unique()
    cursos = ['Todos'] + sorted(cursos_filtrados.tolist())
    curso_selecionado = st.sidebar.selectbox("Curso:", cursos)
    
    termo_busca = st.sidebar.text_input("Buscar Título do Livro:", placeholder="Ex: Anatomia")
    min_views = st.sidebar.slider("Nº Mínimo de Visualizações:", 0, int(df['Total'].max()), 0, 10)

    df_filtrado = df.copy()
    if unidade_selecionada != 'Todas': df_filtrado = df_filtrado[df_filtrado['Unidade'] == unidade_selecionada]
    if curso_selecionado != 'Todos': df_filtrado = df_filtrado[df_filtrado['Curso'] == curso_selecionado]
    if termo_busca: df_filtrado = df_filtrado[df_filtrado['Titulo do Livro'].str.contains(termo_busca, case=False, na=False)]
    if min_views > 0: df_filtrado = df_filtrado[df_filtrado['Total'] >= min_views]
    
    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
    else:
        tab_geral, tab_aluno, tab_professor = st.tabs(["Visão Geral", "Análise por Aluno", "Análise por Professor"])
        with tab_geral: render_visao_geral(df_filtrado)
        with tab_aluno: st.info("🚧 Funcionalidade em desenvolvimento.")
        with tab_professor: st.info("🚧 Funcionalidade em desenvolvimento.")

def render_pergamum():
    st.header("🏛️ Análise de Dados - Pergamum")
    st.warning("Página em construção.", icon="🚧")

def render_repositorio():
    st.header("📂 Análise de Dados - Repositório Institucional")
    st.warning("Página em construção.", icon="🚧")

# --- LAYOUT PRINCIPAL DA APLICAÇÃO ---
logo1_b64 = get_base64_of_bin_file("image.png")
logo2_b64 = get_base64_of_bin_file("logo.png")
logo3_b64 = get_base64_of_bin_file("UNEX-LOGO.png")

st.markdown(f"""
<div class="main-header">
    <img src="data:image/png;base64,{logo1_b64}" class="logo">
    <div class="title">Dashboard Sistema de Bibliotecas</div>
    <img src="data:image/png;base64,{logo2_b64}" class="logo">
    <img src="data:image/png;base64,{logo3_b64}" class="logo">
</div>
""", unsafe_allow_html=True)

selected_page = option_menu(
    menu_title=None,
    options=["Minha Biblioteca", "Pergamum", "Repositório Institucional"],
    icons=["book-half", "bank", "folder2-open"],
    orientation="horizontal",
    # Estilos do menu voltaram a ser otimizados para tema claro
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa", "border-radius": "10px"},
        "icon": {"color": "#1f4e79", "font-size": "20px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#1f4e79"},
    }
)

if selected_page == "Minha Biblioteca": render_minha_biblioteca()
elif selected_page == "Pergamum": render_pergamum()
elif selected_page == "Repositório Institucional": render_repositorio()