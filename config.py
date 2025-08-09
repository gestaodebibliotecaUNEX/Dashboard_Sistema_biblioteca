# config.py
import streamlit as st

def set_page_config():
    """Configura as definições iniciais da página Streamlit."""
    st.set_page_config(
        page_title="Dashboard Sistema de Bibliotecas",
        page_icon="🎓",
        layout="wide"
    )

# Estrutura de dados para a barra de navegação principal
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

# Dicionário com todos os dashboards disponíveis e suas descrições
all_dashboards = {
    'minha_biblioteca':   ("💻 Dashboard Minha Biblioteca", "Análise de uso da plataforma Minha Biblioteca por curso e unidade.", 'acervo_digital'),
    'Repositorio Institucional': ("📁 Dashboard Repositório Institucional", "Submissão de TCCs no Repositório Institucional.", 'acervo_digital'),
    'pergamum':           ('🔗 Dashboard Pergamum', 'Análise de dados de uso do sistema Pergamum, como empréstimos, devoluções e renovações.', 'acervo_digital'),
    'ebsco':              ('🔗 Dashboard EBSCO', 'Análise de dados de acesso, downloads e pesquisas realizadas na plataforma EBSCO.', 'acervo_digital'),
    'uptodate':           ('🔗 Dashboard UpToDate', 'Análise de dados de uso e principais consultas realizadas na plataforma UpToDate.', 'acervo_digital'),
    'busca_integrada':    ('🔗 Dashboard Busca Integrada', 'Análise dos termos mais buscados e fontes mais acessadas através da Busca Integrada.', 'acervo_digital'),
    'emprestimos_gerais': ('📈 Dashboard Empréstimos', 'Visão geral de empréstimos, devoluções e itens mais populares do acervo físico.', 'acervo_fisico'),
    'inventario':         ('📦 Dashboard Inventário', 'Acompanhamento do inventário do acervo físico e status dos materiais.', 'acervo_fisico'),
    'indicadores_mec':    ('📝 Dashboard Indicadores MEC', 'Painel com os principais indicadores de acervo e uso exigidos pelo MEC.', 'avaliacoes_mec'),
}

# Constante para a cor da fonte nos gráficos
FONT_COLOR_GRAPHS = "#E0E1DD"