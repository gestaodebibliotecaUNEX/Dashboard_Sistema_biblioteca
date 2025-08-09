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
# Formato: (Nome_Exibido, chave_unica)
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
# ESTRUTURA:
# 'chave_unica': (
#     "Título do Card",
#     "Descrição do Card",
#     "categoria_da_navegacao",
#     "Link_Externo"  # Use None se for um dashboard interno do projeto
# )
all_dashboards = {
    # Dashboard INTERNO (o link é 'None')
    'minha_biblioteca': (
        "📚💻Minha Biblioteca",
        "Análise de uso da plataforma Minha Biblioteca por curso e unidade.",
        'acervo_digital',
        None  # Este é interno, então não tem link.
    ),
    'repositorio_institucional': (
        "🏛️ Repositório Institucional",
        "Análise de acesso e downloads do Repositório Institucional.",
        'acervo_digital',
        'https://url-do-seu-dashboard-pergamum.com' # Substitua pelo seu link

    ),
    
    # Dashboards EXTERNOS (preencha com os seus links)
    'pergamum': (
        '🏛️ Pergamum',
        'Análise de dados de uso do sistema Pergamum',
        'acervo_fisico',  # <-- ESTA É A LINHA QUE AJUSTAMOS
        'https://url-do-seu-dashboard-pergamum.com' # Substitua pelo seu link
    ),
    'ebsco': (
        '🔗 EBSCO',
        'Análise de dados de acesso, downloads e pesquisas realizadas na plataforma EBSCO.',
        'acervo_digital',
        'https://url-do-seu-dashboard-ebsco.com' # Substitua pelo seu link
    ),
    'uptodate': (
        '🔗 UpToDate',
        'Análise de uso da plataforma UpToDate.',
        'acervo_digital',
        'https://url-do-seu-dashboard-uptodate.com' # Substitua pelo seu link
    ),
    
    # Outros dashboards que ainda serão construídos ou linkados
    'busca_integrada': (
        '🔗 Busca Integrada',
        'Análise da Plataforma Busca Integrada.',
        'acervo_digital',
        None # Deixe como None por enquanto
    ),
     
    'inventario': (
        '📦 Dashboard Inventário',
        'Acompanhamento do inventário do acervo físico e status dos materiais.',
        'acervo_fisico',
        None # Deixe como None por enquanto
    ),
    'indicadores_mec': (
        '📝 Indicadores MEC',
        'Painel com os principais indicadores de acervo e uso exigidos pelo MEC.',
        'avaliacoes_mec',
        None # Deixe como None por enquanto
    ),
}

# Constante para a cor da fonte nos gráficos
FONT_COLOR_GRAPHS = "#E0E1DD"