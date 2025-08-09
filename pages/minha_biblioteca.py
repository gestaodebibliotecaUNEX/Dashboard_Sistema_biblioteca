# pages/minha_biblioteca.py
import streamlit as st
import plotly.express as px
from utils import load_data
from config import FONT_COLOR_GRAPHS

def render_page():
    """Renderiza a página do dashboard 'Minha Biblioteca'."""
    df = load_data("assets/planilha_lyceum_e_minha_biblioteca.xlsx")
    
    if df is None:
        st.error("Não foi possível carregar os dados para exibir o dashboard 'Minha Biblioteca'.")
        return

    # --- FILTROS NA BARRA LATERAL ---
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

    # --- APLICAÇÃO DOS FILTROS ---
    df_filtrado = df.copy()
    if unidade_selecionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Unidade'] == unidade_selecionada]
    if curso_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Curso'] == curso_selecionado]
    if termo_busca:
        df_filtrado = df_filtrado[df_filtrado['Titulo do Livro'].str.contains(termo_busca, case=False, na=False)]
    if min_views > 0:
        df_filtrado = df_filtrado[df_filtrado['Total'] >= min_views]

    # --- RENDERIZAÇÃO DO CONTEÚDO DA PÁGINA ---
    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados. Tente ajustar as opções na barra lateral.")
        return

    # KPIs
    kpi_cols = st.columns(4)
    with kpi_cols[0]: st.markdown(f"""<div class="kpi-card"><h3>📚 Livros Filtrados</h3><h2>{df_filtrado['Titulo do Livro'].nunique()}</h2></div>""", unsafe_allow_html=True)
    with kpi_cols[1]: st.markdown(f"""<div class="kpi-card"><h3>👁️ Visualizações</h3><h2>{df_filtrado['Total'].sum():,}</h2></div>""", unsafe_allow_html=True)
    with kpi_cols[2]: st.markdown(f"""<div class="kpi-card"><h3>🏫 Unidades</h3><h2>{df_filtrado['Unidade'].nunique()}</h2></div>""", unsafe_allow_html=True)
    with kpi_cols[3]: st.markdown(f"""<div class="kpi-card"><h3>🎓 Cursos</h3><h2>{df_filtrado['Curso'].nunique()}</h2></div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos em colunas
    graph_cols = st.columns(2)
    with graph_cols[0], st.container(border=False):
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("📊 Top 10 Unidades por Visualização")
        df_unidade = df_filtrado.groupby('Unidade')['Total'].sum().nlargest(10).reset_index()
        fig = px.bar(df_unidade, x='Total', y='Unidade', orientation='h', text='Total', color_discrete_sequence=['#90E0EF'])
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_title=None, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=FONT_COLOR_GRAPHS)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with graph_cols[1], st.container(border=False):
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("🎯 Top 10 Cursos por Visualização")
        df_curso = df_filtrado.groupby('Curso')['Total'].sum().nlargest(10).reset_index()
        fig = px.pie(df_curso, values='Total', names='Curso', hole=0.5, color_discrete_sequence=px.colors.sequential.GnBu_r)
        fig.update_layout(legend_title_text='Cursos', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=FONT_COLOR_GRAPHS)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Outros gráficos e tabelas
    with st.container(border=False):
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("📦 Dispersão de Visualizações por Unidade")
        top_unidades_list = df_filtrado['Unidade'].value_counts().nlargest(10).index
        df_boxplot = df_filtrado[df_filtrado['Unidade'].isin(top_unidades_list)]
        fig_box = px.box(df_boxplot, x='Unidade', y='Total', color='Unidade', labels={'Total': 'Total de Visualizações', 'Unidade': 'Unidade'}, color_discrete_sequence=px.colors.qualitative.Pastel)
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