import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime

# --- CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Sistema de Bibliotecas",
    page_icon="🎓",
    layout="wide"
)

# --- CSS PARA ESTILIZAÇÃO ---
def load_css():
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }
        body, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #1B263B !important;
            color: #FFFFFF !important;
        }
        [data-testid="stSidebar"] {
            background-color: #0D1B2A !important;
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

@st.cache_data
def load_data():
    try:
        file_path = "planilha_lyceum_e_minha_biblioteca.xlsx"
        df = pd.read_excel(file_path, header=3)
        df.dropna(subset=['Unidade', 'Curso', 'Titulo do Livro'], inplace=True)
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0).astype(int)
        df = df[df['Total'] > 0]
        return df
    except FileNotFoundError:
        st.error(f"Ficheiro de dados '{file_path}' não encontrado!", icon="🚨")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

# --- ESTRUTURA DE DADOS E NAVEGAÇÃO ---
navigation_options = [
    ("🏠 Painel de Controle", "inicio"),
    ("💾 Acervo Digital", "acervo_digital"),
    ("📖 Acervo Físico", "acervo_fisico"),
    ("📊 Avaliações MEC", "avaliacoes_mec"),
    ("📋 Contratações", "contratacoes"),
    ("👥 Educação de Usuários", "educacao_usuarios"),
    ("🏗️ Infraestrutura", "infraestrutura"),
    ("👤 Pessoas", "pessoas")
]

all_dashboards = {
    'minha_biblioteca':     ("📚 Dashboard Minha Biblioteca",     "Análise de uso da plataforma Minha Biblioteca por curso e unidade.", 'acervo_digital'),
    'pergamum':             ('🔗 Dashboard Pergamum',            'Análise de dados de uso do sistema Pergamum, como empréstimos, devoluções e renovações.', 'acervo_digital'),
    'ebsco':                ('🔗 Dashboard EBSCO',               'Análise de dados de acesso, downloads e pesquisas realizadas na plataforma EBSCO.', 'acervo_digital'),
    'uptodate':             ('🔗 Dashboard UpToDate',            'Análise de dados de uso e principais consultas realizadas na plataforma UpToDate.', 'acervo_digital'),
    'busca_integrada':      ('🔗 Dashboard Busca Integrada',     'Análise dos termos mais buscados e fontes mais acessadas através da Busca Integrada.', 'acervo_digital'),
    'emprestimos_gerais':   ('📈 Dashboard Empréstimos',         'Visão geral de empréstimos, devoluções e itens mais populares do acervo físico.', 'acervo_fisico'),
    'inventario':           ('📦 Dashboard Inventário',          'Acompanhamento do inventário do acervo físico e status dos materiais.', 'acervo_fisico'),
    'indicadores_mec':      ('📝 Dashboard Indicadores MEC',     'Painel com os principais indicadores de acervo e uso exigidos pelo MEC.', 'avaliacoes_mec'),
}

if 'selected_page' not in st.session_state:
    st.session_state.selected_page = 'inicio'

def set_page(page_key):
    st.session_state.selected_page = page_key

# --- BARRA LATERAL ---
st.sidebar.markdown("### Navegação")
for option_name, option_key in navigation_options:
    if st.sidebar.button(option_name, key=f"sidebar_{option_key}", use_container_width=True):
        set_page(option_key)
        st.rerun()

st.sidebar.markdown(f"""
<div class="contact-info">
    <h4>Para maiores informações:</h4>
    <p>📧 gestaodebiblioteca@unex.edu.br</p>
    <p>🌐 https://www.uniftc.edu.br/servicos/biblioteca</p>
    <p><strong>Última atualização:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
</div>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
logo1_b64 = get_base64_of_bin_file("image.png")
logo2_b64 = get_base64_of_bin_file("logo.png")
logo3_b64 = get_base64_of_bin_file("UNEX-LOGO.png")
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


# --- FUNÇÃO PARA GERAR PÁGINAS DE HUB (CORRIGE O NameError) ---
def render_hub_page(page_key, page_name):
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
        for i, (key, (title, desc, _)) in enumerate(row):
            with cols[i]:
                st.markdown(f"""
                <div class="dashboard-card">
                    <div class="dashboard-card-content">
                        <h3>{title}</h3>
                        <p>{desc}</p>
                    </div>
                </div>""", unsafe_allow_html=True)
                if st.button("Acessar Dashboard", key=f"btn_{key}"):
                    set_page(key)
                    st.rerun()

# --- ROTEAMENTO DE PÁGINAS ---
current_page_key = st.session_state.selected_page

if current_page_key == 'inicio':
    st.subheader("Bem-vindo ao Sistema de Bibliotecas")
    st.markdown("Use o menu à esquerda para navegar entre as diferentes seções e explorar os dashboards de análise de dados.")
    st.image("Biblioteca.jpg", use_container_width=True)

elif current_page_key == 'minha_biblioteca':
    FONT_COLOR_GRAPHS = "#E0E1DD"
    df = load_data()
    if df is not None:
        st.sidebar.markdown("---")
        st.sidebar.header("🔍 Filtros (Minha Biblioteca)")
        
        unidades = ['Todas'] + sorted(df['Unidade'].unique().tolist())
        unidade_selecionada = st.sidebar.selectbox("Selecione a Unidade:", unidades)
        
        cursos_options = df['Curso'].unique()
        if unidade_selecionada != 'Todas':
            cursos_options = df[df['Unidade'] == unidade_selecionada]['Curso'].unique()
        
        cursos = ['Todos'] + sorted(cursos_options.tolist())
        curso_selecionado = st.sidebar.selectbox("Selecione o Curso:", cursos)
        
        termo_busca = st.sidebar.text_input("Buscar por Título do Livro:", placeholder="Ex: Anatomia")
        
        min_views = st.sidebar.slider(
            "Nº mínimo de visualizações:", 
            min_value=0, max_value=int(df['Total'].max()), value=0, step=10
        )

        df_filtrado = df.copy()
        if unidade_selecionada != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Unidade'] == unidade_selecionada]
        if curso_selecionado != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Curso'] == curso_selecionado]
        if termo_busca:
            df_filtrado = df_filtrado[df_filtrado['Titulo do Livro'].str.contains(termo_busca, case=False, na=False)]
        if min_views > 0:
            df_filtrado = df_filtrado[df_filtrado['Total'] >= min_views]

        if not df_filtrado.empty:
            kpi_cols = st.columns(4)
            with kpi_cols[0]: st.markdown(f"""<div class="kpi-card"><h3>📚 Livros Filtrados</h3><h2>{df_filtrado['Titulo do Livro'].nunique()}</h2></div>""", unsafe_allow_html=True)
            with kpi_cols[1]: st.markdown(f"""<div class="kpi-card"><h3>👁️ Visualizações</h3><h2>{df_filtrado['Total'].sum():,}</h2></div>""", unsafe_allow_html=True)
            with kpi_cols[2]: st.markdown(f"""<div class="kpi-card"><h3>🏫 Unidades</h3><h2>{df_filtrado['Unidade'].nunique()}</h2></div>""", unsafe_allow_html=True)
            with kpi_cols[3]: st.markdown(f"""<div class="kpi-card"><h3>🎓 Cursos</h3><h2>{df_filtrado['Curso'].nunique()}</h2></div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            graph_cols = st.columns(2)
            with graph_cols[0]:
                with st.container(border=False):
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)
                    st.subheader("📊 Top 10 Unidades por Visualização")
                    df_unidade = df_filtrado.groupby('Unidade')['Total'].sum().nlargest(10).reset_index()
                    fig = px.bar(df_unidade, x='Total', y='Unidade', orientation='h', text='Total', color_discrete_sequence=['#90E0EF'])
                    fig.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_title=None, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=FONT_COLOR_GRAPHS)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            with graph_cols[1]:
                with st.container(border=False):
                    st.markdown('<div class="card-container">', unsafe_allow_html=True)
                    st.subheader("🎯 Top 10 Cursos por Visualização")
                    df_curso = df_filtrado.groupby('Curso')['Total'].sum().nlargest(10).reset_index()
                    fig = px.pie(df_curso, values='Total', names='Curso', hole=0.5, color_discrete_sequence=px.colors.sequential.GnBu_r)
                    fig.update_layout(legend_title_text='Cursos', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=FONT_COLOR_GRAPHS)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with st.container(border=False):
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.subheader("📦 Dispersão de Visualizações por Unidade")
                top_unidades_list = df_filtrado['Unidade'].value_counts().nlargest(10).index
                df_boxplot = df_filtrado[df_filtrado['Unidade'].isin(top_unidades_list)]
                fig_box = px.box(df_boxplot, x='Unidade', y='Total', color='Unidade',
                                 labels={'Total': 'Total de Visualizações', 'Unidade': 'Unidade'},
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=FONT_COLOR_GRAPHS)
                st.plotly_chart(fig_box, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with st.container(border=False):
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.subheader("🗺️ Mapa de Visualizações (Unidade > Curso > Livro)")
                st.info("Clique nas Unidades e Cursos para expandir e ver os livros.", icon="💡")
                fig_treemap = px.treemap(df_filtrado, path=[px.Constant("Visão Geral"), 'Unidade', 'Curso', 'Titulo do Livro'], values='Total', color='Curso', hover_data=['Total'], color_discrete_sequence=px.colors.qualitative.Set3)
                fig_treemap.update_layout(height=700, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=FONT_COLOR_GRAPHS)
                st.plotly_chart(fig_treemap, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with st.container(border=False):
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.subheader("📖 Livros Mais Visualizados")
                top_n = st.number_input("Selecione o ranking de livros para exibir:", min_value=5, max_value=50, value=15, step=5)
                df_livros = df_filtrado.groupby(['Titulo do Livro'])['Total'].sum().nlargest(top_n).reset_index()
                fig = px.bar(df_livros, x='Total', y='Titulo do Livro', orientation='h', color='Total', color_continuous_scale='GnBu')
                fig.update_layout(height=max(400, top_n * 25), yaxis={'categoryorder':'total ascending'}, yaxis_title=None, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=FONT_COLOR_GRAPHS)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with st.container(border=False):
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.subheader("🔍 Dados Detalhados (Tabela Interativa)")
                df_tabela = df_filtrado[['Titulo do Livro', 'Curso', 'Unidade', 'Total']].sort_values('Total', ascending=False)
                st.dataframe(df_tabela.reset_index(drop=True), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Nenhum dado encontrado com os filtros aplicados. Tente ajustar as opções na barra lateral.")
    else:
        # CORREÇÃO DO SyntaxError: Parêntese de fechamento adicionado.
        st.error("Não foi possível carregar os dados para exibir o dashboard 'Minha Biblioteca'.")

else:
    is_hub_page = any(current_page_key == nav_key for _, nav_key in navigation_options if nav_key != 'inicio')
    
    if is_hub_page:
        page_name = [name for name, key in navigation_options if key == current_page_key][0]
        render_hub_page(current_page_key, page_name)
    
    else:
        title, desc, _ = all_dashboards.get(current_page_key, ("Painel Não Encontrado", "", ""))
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.header(f"🚧 {title} 🚧")
        st.info("Este painel está em construção. Em breve, novos insights e funcionalidades estarão disponíveis aqui!", icon="🛠️")
        st.markdown(f"**O que esperar deste dashboard:** {desc}")
        st.markdown('</div>', unsafe_allow_html=True)