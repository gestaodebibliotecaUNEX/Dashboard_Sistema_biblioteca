import streamlit as st
import pandas as pd
import plotly.express as px




 
@st.cache_data
def load_data_from_single_file(filename="Total_de_Acesso.xlsx"):
    """
    Esta função carrega e limpa os dados de um único arquivo Excel.
    Ela cria dois dataframes: um com o total geral e outro com os detalhes por unidade.
    """
    try:
        # CORREÇÃO APLICADA AQUI:
        # Trocamos pd.read_csv por pd.read_excel para ler o arquivo .xlsx corretamente.
        df = pd.read_excel(filename, header=1)

        # Limpa os nomes das colunas (remove espaços em branco no início e no fim)
        df.columns = df.columns.str.strip()

        # Limpa os valores na coluna 'Curso'
        if 'Curso' in df.columns:
            df['Curso'] = df['Curso'].str.strip()
        else:
            st.error("Erro: A coluna 'Curso' não foi encontrada no arquivo. Verifique o Excel.")
            return None, None


        # Verifica se a coluna de total existe e a renomeia
        if 'Total geral' not in df.columns:
            st.error("Erro: A coluna 'Total geral' não foi encontrada no arquivo. Verifique o Excel.")
            return None, None
        df.rename(columns={'Total geral': 'Total de Visualizações'}, inplace=True)

        # --- Criação do DataFrame df_geral ---
        df_geral = df[['Curso', 'Total de Visualizações']].copy()
        # Garante que a coluna de visualizações seja numérica e sem valores nulos
        df_geral['Total de Visualizações'] = pd.to_numeric(df_geral['Total de Visualizações'], errors='coerce').fillna(0).astype(int)
        df_geral.dropna(inplace=True)

        # --- Criação do DataFrame df_unidades ---
        df_unidades = df.drop(columns=['Total de Visualizações'])

        # Converte todas as colunas de unidades para numérico, preenchendo erros/nulos com 0
        for col in df_unidades.columns:
            if col != 'Curso':
                df_unidades[col] = pd.to_numeric(df_unidades[col], errors='coerce').fillna(0).astype(int)

        return df_geral, df_unidades

    except FileNotFoundError:
        # Exibe uma mensagem de erro amigável se o arquivo não for encontrado
        st.error(f"Erro: Arquivo '{filename}' não encontrado.")
        st.error("Por favor, certifique-se de que o arquivo Excel está na mesma pasta que o script Python.")
        return None, None
    except Exception as e:
        # Captura outros erros possíveis durante o carregamento
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
        return None, None


# --- Instalação da dependência para ler arquivos Excel ---
# Para pd.read_excel funcionar, você pode precisar instalar a biblioteca 'openpyxl'.
# No seu terminal, execute: pip install openpyxl


# Carrega os dados usando a função
df_geral, df_unidades = load_data_from_single_file()

# Se o carregamento de dados falhar, interrompe a execução do restante do app
if df_geral is None or df_unidades is None:
    st.stop()


# --- 2. Layout do Dashboard com Streamlit ---

# Configuração da página para usar a largura total e define um título para a aba do navegador
st.set_page_config(layout="wide", page_title="Dashboard de Visualizações")

# Título do Dashboard
st.title("📊 Dashboard de Visualizações de Cursos e Unidades")

# Seção de Visão Geral
st.header("Visão Geral", divider='rainbow')
col1, col2 = st.columns(2)

with col1:
    # Gráfico 1: Total de Visualizações por Curso
    st.subheader("Total de Visualizações por Curso")
    fig_total_cursos = px.bar(
        df_geral.sort_values('Total de Visualizações', ascending=False),
        x='Curso',
        y='Total de Visualizações',
        template='plotly_white',
        text_auto=True
    )
    fig_total_cursos.update_traces(marker_color='#1E90FF')
    fig_total_cursos.update_layout(title_x=0.5, xaxis_tickangle=-45)
    st.plotly_chart(fig_total_cursos, use_container_width=True)

with col2:
    # Gráfico 2: Distribuição de Visualizações por Unidade
    st.subheader("Distribuição por Unidade")
    # Calcula o total por unidade a partir do dataframe detalhado
    unidades_total = df_unidades.drop(columns=['Curso']).sum().reset_index()
    unidades_total.columns = ['Unidade', 'Visualizações']

    fig_total_unidades = px.pie(
        unidades_total,
        names='Unidade',
        values='Visualizações',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_total_unidades.update_traces(textinfo='percent+label', pull=[0.05] * len(unidades_total))
    st.plotly_chart(fig_total_unidades, use_container_width=True)

# --- 3. Seção Interativa ---

st.header("Análise Detalhada Interativa", divider='rainbow')
col3, col4 = st.columns(2)

# Seletor e gráfico por Curso
with col3:
    st.subheader("Análise por Curso")
    curso_selecionado = st.selectbox(
        'Selecione um Curso para ver os detalhes por Unidade:',
        options=df_unidades['Curso'].unique(),
        index=0
    )

    # Filtra os dados para o curso selecionado e formata para o gráfico
    dados_curso = df_unidades[df_unidades['Curso'] == curso_selecionado].melt(
        id_vars=['Curso'], var_name='Unidade', value_name='Visualizações'
    )
    dados_curso = dados_curso[dados_curso['Visualizações'] > 0]

    fig_detalhe_curso = px.bar(
        dados_curso.sort_values('Visualizações', ascending=False),
        x='Unidade',
        y='Visualizações',
        title=f'Visualizações de {curso_selecionado} por Unidade',
        text_auto=True,
        color='Unidade'
    )
    fig_detalhe_curso.update_layout(title_x=0.5, xaxis_title=None, showlegend=False)
    st.plotly_chart(fig_detalhe_curso, use_container_width=True)

# Seletor e gráfico por Unidade
with col4:
    st.subheader("Análise por Unidade")
    unidades_lista = df_unidades.columns[1:].tolist()
    unidade_selecionada = st.selectbox(
        'Selecione uma Unidade para ver os cursos mais populares:',
        options=unidades_lista,
        index=0
    )

    # Seleciona os dados da unidade e os cursos
    dados_unidade = df_unidades[['Curso', unidade_selecionada]].rename(columns={unidade_selecionada: 'Visualizações'})
    dados_unidade = dados_unidade[dados_unidade['Visualizações'] > 0]

    fig_detalhe_unidade = px.bar(
        dados_unidade.sort_values('Visualizações', ascending=True),
        x='Visualizações',
        y='Curso',
        orientation='h',
        title=f'Top Cursos na Unidade: {unidade_selecionada}',
        text='Visualizações',
        color='Curso',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_detalhe_unidade.update_layout(title_x=0.5, yaxis_title=None, showlegend=False)
    fig_detalhe_unidade.update_traces(textposition='outside')
    st.plotly_chart(fig_detalhe_unidade, use_container_width=True)