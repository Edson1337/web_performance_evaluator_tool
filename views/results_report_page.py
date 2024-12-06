import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

# Configuração da página para modo largo
st.set_page_config(layout="wide")

# Carregar o DataFrame
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['statisticalTestU'] = pd.to_numeric(df['statisticalTestU'], errors='coerce')
    df['isSignificant'] = pd.to_numeric(df['isSignificant'], errors='coerce')
    return df

# Função para classificar a significância
def classify_significance(row):
    significance = abs(row['isSignificant'])
    if significance < 0.3:
        return 'small'
    elif 0.3 < significance < 0.5:
        return 'medium'
    else:
        return 'large'

# Função para verificar se há mudança significativa (somente quando statisticalTestU <= 0.05)
def has_significant_change(row):
    return (
        not pd.isnull(row['statisticalTestU']) and 
        row['statisticalTestU'] <= 0.05
    )

# Definir o caminho para o arquivo de resultados
current_dir = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
results_path = os.path.join(project_dir, 'results')
statistical_result = os.path.join(results_path, 'merged_results.csv')
file_path = statistical_result

# Carregar os dados
df = load_data(file_path)

# Criar a coluna 'improvement' antes da filtragem
df['improvement'] = np.where(df['isSignificant'] < 0, 'Baseline', 'Current')
df['significance_level'] = df.apply(classify_significance, axis=1)
df['has_change'] = df.apply(has_significant_change, axis=1)
df['is_regression'] = df['isSignificant'] < 0

# Filtrar as linhas com mudanças significativas
df_filtered = df[df['has_change']]

# Adicionar um selectbox para escolher o projectName, aplicável ao heatmap e ao line plot
project_names = df['projectName'].unique()
selected_project = st.selectbox('Select a Project for Analysis', project_names)

# Filtrar o DataFrame para o projeto selecionado apenas para o heatmap e line plot
df_project = df_filtered[df_filtered['projectName'] == selected_project]

# Título do dashboard
st.title('Performance Analysis Dashboard')

# Verificação se a métrica 'firstContentfulPaint' está presente após os filtros
if 'firstContentfulPaint' not in df_project['metricName'].unique():
    st.write("Warning: 'firstContentfulPaint' is not present in the filtered data.")

# 1. Heatmap e Line Plot Lado a Lado
col1, col2 = st.columns([1, 1])

# Heatmap de Médias de isSignificant
with col1:
    st.subheader('Heatmap of Average Significant Changes')
    if not df_project.empty:
        heatmap_data = df_project.pivot_table(
            index='metricName', 
            columns='scenarioName', 
            values='isSignificant', 
            aggfunc='mean', 
            fill_value=0
        )
        num_metrics = len(heatmap_data.index)
        num_scenarios = len(heatmap_data.columns)
        plt.figure(figsize=(max(8, num_scenarios * 0.6), max(7, num_metrics * 0.6)))
        sns.heatmap(
            heatmap_data, 
            annot=True, 
            fmt=".2f", 
            cmap='coolwarm', 
            cbar_kws={'label': 'Average isSignificant'}, 
            vmin=-1, 
            vmax=1,
            annot_kws={'size': 8}
        )
        plt.title(f'Average isSignificant per Metric and Scenario for {selected_project}', fontsize=16)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(rotation=0, fontsize=10)
        plt.tight_layout(pad=2)
        st.pyplot(plt)
    else:
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.text(0.5, 0.5, f"No significant changes found for project {selected_project}.", 
                fontsize=16, ha='center', va='center', transform=ax.transAxes)
        ax.axis('off')
        st.pyplot(fig)

# Line Plot de Evolução dos Valores de isSignificant (Com métricas significativas e não significativas)
available_line_styles = [(0, ()), (0, (3, 5)), (0, (1, 1)), (0, (5, 5, 1, 5)), (0, (3, 1, 1, 1))]

# Função para gerar o estilo de linha dinamicamente com base na quantidade de métricas
def generate_line_styles(metric_names):
    # Repetir estilos se houver mais métricas do que estilos
    return dict(zip(metric_names, itertools.cycle(available_line_styles)))

# Gera os estilos de linha dinamicamente com base nas métricas no dataframe
metric_names = df_project['metricName'].unique()
line_styles = generate_line_styles(metric_names)

# Line Plot de Evolução dos Valores de isSignificant com diferentes estilos de linha
with col2:
    st.subheader('Line Plot of isSignificant by Scenario')
    if not df_project.empty:
        plt.figure(figsize=(10, 6))
        for metric, metric_data in df_project.groupby('metricName'):
            sns.lineplot(
                data=metric_data, 
                x='scenarioName', 
                y='isSignificant', 
                label=metric, 
                linestyle=line_styles[metric],  # Aplicar estilo de linha específico para cada métrica
                marker='o',  # Adicionar marcadores
                linewidth=2  # Controlar a espessura da linha
            )
        plt.title(f'isSignificant Values by Scenario for Each Metric in {selected_project}', fontsize=14)
        plt.xlabel('Scenario Name', fontsize=12)
        plt.ylabel('isSignificant', fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.legend(title='Metric')
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write("No data available for the line plot.")

# 2. Tabelas de Contagem de Regressões e Dados Gerais
col3, col4 = st.columns([1, 1])

# Tabela de Contagem de Regressões
with col3:
    st.subheader('Regression Count by Application and Metric')
    regressions_by_application = df[df['is_regression']].groupby(['projectName', 'metricName']).size().reset_index(name='regression_count')
    st.dataframe(regressions_by_application)

# Exibir a tabela completa dos dados originais
with col4:
    st.subheader("Complete Data Overview")
    st.dataframe(df[['projectName', 'scenarioName', 'metricName', 'isSignificant', 'statisticalTestU', 'significance_level', 'improvement']])
