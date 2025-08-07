 # app.py (Versão final com função de carregamento original)

import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# --- CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Sistema de Bibliotecas",
    page_icon="🎓",
    layout="wide"
)

# --- CSS PARA ESTILIZAÇÃO PROFISSIONAL ---
def load_css():
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
        body, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #111827;
            color: #E5E7EB;
        }
        [data-testid="stSidebar"] {
            background-color: #1F2937;
            border-right: 1px solid #374151;
        }
        [data-testid="stSidebar"] .st-emotion-cache-1b0udgb, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
             color: #FFFFFF;
        }
        .card-container {
            background-color: #1F2937;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #374151;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        }
        .kpi-card {
            background-color: #1F2937;
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #374151;
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
        }
        .kpi-card h3 {
            font-size: 1rem;
            color: #9CA3AF;
            font-weight: 600;
            margin: 0;
        }
        .kpi-card h2 {
            font-size: 2.25rem;
            color: #FFFFFF;
            font-weight: 700;
            margin: 0;
        }
        .logo-img {
            height: 45px;
            object-fit: contain;
            background-color: #FFFFFF;
            border-radius: 8px;
            padding: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.5);
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
        return ""

# --- ALTERAÇÃO AQUI: De volta à sua função original ---
@st.cache_data
def load_data():
    try:
        file_path = "planilha_lyceum_e_minha_biblioteca.xlsx"
        df = pd.read_excel(file_path, header=3)
        df.dropna(subset=['Unidade', 'Curso', 'Titulo do Livro'], inplace=True)
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0).astype(int)
        df = df[df['Total'] > 0] # Mantendo esta limpeza para gráficos melhores
        return df
    except FileNotFoundError:
        st.error(f"Ficheiro de dados '{file_path}' não encontrado!", icon="🚨")
        st.warning("""
        **Por favor, certifique-se de que o ficheiro `planilha_lyceum_e_minha_biblioteca.xlsx` está na mesma pasta que o seu script `app.py`.**
        """)
        return None
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

# --- CARREGAMENTO INICIAL DOS DADOS ---
df = load_data()

# --- LAYOUT DA BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("Dashboard de Bibliotecas")
    st.markdown("---")
    
    selected_page = st.radio(
        "Navegação",
        ["Minha Biblioteca", "Pergamum", "Repositório Institucional"],
        captions=["Análise de acessos", "Em breve", "Em breve"]
    )
    st.markdown("---")

    df_filtrado = None
    if df is not None and selected_page == "Minha Biblioteca":
        st.header("🔍 Filtros Interativos")
        unidades = ['Todas'] + sorted(df['Unidade'].unique().tolist())
        unidade_selecionada = st.selectbox("Selecione a Unidade:", unidades)
        
        if unidade_selecionada != 'Todas':
            cursos_filtrados = df[df['Unidade'] == unidade_selecionada]['Curso'].unique()
        else:
            cursos_filtrados = df['Curso'].unique()
        
        cursos = ['Todos'] + sorted(cursos_filtrados.tolist())
        curso_selecionado = st.selectbox("Selecione o Curso:", cursos)
        
        termo_busca = st.text_input("Buscar por Título do Livro:", placeholder="Ex: Anatomia Humana")
        
        if not df.empty:
            min_views = st.slider(
                "Filtrar por nº mínimo de visualizações:", 
                min_value=0, 
                max_value=int(df['Total'].max()), 
                value=0,
                step=10
            )
        else:
            min_views = 0
        
        # --- LÓGICA DE FILTRAGEM ---
        df_filtrado = df.copy()
        if unidade_selecionada != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Unidade'] == unidade_selecionada]
        if curso_selecionado != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Curso'] == curso_selecionado]
        if termo_busca:
            df_filtrado = df_filtrado[df_filtrado['Titulo do Livro'].str.contains(termo_busca, case=False, na=False)]
        if min_views > 0:
            df_filtrado = df_filtrado[df_filtrado['Total'] >= min_views]

# --- RENDERIZAÇÃO DA PÁGINA PRINCIPAL ---

# Cabeçalho com Logos
logo1_b64 = get_base64_of_bin_file("image.png")
logo2_b64 = get_base64_of_bin_file("logo.png")
logo3_b64 = get_base64_of_bin_file("UNEX-LOGO.png")

col_title, col_logo1, col_logo2, col_logo3 = st.columns([0.55, 0.15, 0.15, 0.15])
with col_title:
    st.header(f"Análise de Dados: {selected_page}")
with col_logo1:
    if logo1_b64:
        st.markdown(f'<img src="data:image/png;base64,{logo1_b64}" class="logo-img">', unsafe_allow_html=True)
with col_logo2:
    if logo2_b64:
        st.markdown(f'<img src="data:image/png;base64,{logo2_b64}" class="logo-img">', unsafe_allow_html=True)
with col_logo3:
    if logo3_b64:
        st.markdown(f'<img src="data:image/png;base64,{logo3_b64}" class="logo-img">', unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)

# Lógica condicional para renderizar o dashboard ou mensagens
if selected_page == "Minha Biblioteca":
    if df_filtrado is not None and not df_filtrado.empty:
        # KPIs
        kpi_cols = st.columns(4)
        with kpi_cols[0]:
            st.markdown(f"""<div class="kpi-card"><h3>📚 Total de Livros</h3><h2>{df_filtrado['Titulo do Livro'].nunique()}</h2></div>""", unsafe_allow_html=True)
        with kpi_cols[1]:
            st.markdown(f"""<div class="kpi-card"><h3>👁️ Total de Visualizações</h3><h2>{df_filtrado['Total'].sum():,}</h2></div>""", unsafe_allow_html=True)
        with kpi_cols[2]:
            st.markdown(f"""<div class="kpi-card"><h3>🏫 Unidades</h3><h2>{df_filtrado['Unidade'].nunique()}</h2></div>""", unsafe_allow_html=True)
        with kpi_cols[3]:
            st.markdown(f"""<div class="kpi-card"><h3>🎓 Cursos</h3><h2>{df_filtrado['Curso'].nunique()}</h2></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráficos em Colunas
        graph_cols = st.columns(2)
        with graph_cols[0]:
            with st.container():
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.subheader("📊 Top 10 Unidades por Visualização")
                df_unidade = df_filtrado.groupby('Unidade')['Total'].sum().nlargest(10).reset_index()
                fig = px.bar(df_unidade, x='Total', y='Unidade', orientation='h', text='Total', color_discrete_sequence=['#4C88E8'])
                fig.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_title=None, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#E5E7EB')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with graph_cols[1]:
            with st.container():
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.subheader("🎯 Top 10 Cursos por Visualização")
                df_curso = df_filtrado.groupby('Curso')['Total'].sum().nlargest(10).reset_index()
                fig = px.pie(df_curso, values='Total', names='Curso', hole=0.5, color_discrete_sequence=px.colors.sequential.Blues_r)
                fig.update_layout(legend_title_text='Cursos', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#E5E7EB')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Gráfico Treemap
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.subheader("🗺️ Mapa de Visualizações (Unidade > Curso)")
            fig_treemap = px.treemap(df_filtrado, path=[px.Constant("Todas as Unidades"), 'Unidade', 'Curso'], values='Total',
                                     color='Curso', hover_data=['Total'],
                                     color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_treemap.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#E5E7EB')
            st.plotly_chart(fig_treemap, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráfico de Livros
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.subheader("📖 Livros Mais Visualizados")
            top_n = st.number_input("Selecione o número de livros para exibir no ranking:", min_value=5, max_value=50, value=15, step=5)
            df_livros = df_filtrado.groupby(['Titulo do Livro'])['Total'].sum().nlargest(top_n).reset_index()
            fig = px.bar(df_livros, x='Total', y='Titulo do Livro', orientation='h', color='Total', color_continuous_scale='Blues')
            fig.update_layout(height=max(400, top_n * 25), yaxis={'categoryorder':'total ascending'}, yaxis_title=None, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#E5E7EB')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Tabela Interativa
        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.subheader("🔍 Dados Detalhados (Tabela Interativa)")
            df_tabela = df_filtrado[['Titulo do Livro', 'Curso', 'Unidade', 'Total']].sort_values('Total', ascending=False)
            st.dataframe(df_tabela.reset_index(drop=True), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif df is None:
        pass
    else:
        st.warning("Nenhum dado encontrado com os filtros aplicados. Tente ajustar os filtros na barra lateral.")

elif selected_page in ["Pergamum", "Repositório Institucional"]:
    st.info("🚧 Página em construção. Em breve, novos insights estarão disponíveis aqui!")