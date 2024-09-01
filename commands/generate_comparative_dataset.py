import pandas as pd
import os

def generate_comparative_dataset():
    current_dir = os.path.abspath(__file__)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    results_path = os.path.join(project_dir, 'results')
    file_path = os.path.join(results_path, 'performance_evaluation_results.csv')

    # Carregar o CSV
    df = pd.read_csv(file_path)

    # Separar o benchmark em project_name, render_type e route
    df[['project_name', 'render_type', 'route']] = df['benchmark'].str.extract(r'(.+)-([cs]{2}r)-(.+)')

    # Remover colunas desnecessárias
    df = df.drop(columns=['id', 'benchmark'])

    # Dividir em DataFrames CSR e SSR
    csr_df = df[df['render_type'] == 'csr'].copy()
    ssr_df = df[df['render_type'] == 'ssr'].copy()

    # Renomear colunas para distinção
    csr_df = csr_df.rename(columns={col: f"{col}_csr" for col in csr_df.columns if col not in ['project_name', 'route', 'scenario', 'interation']})
    ssr_df = ssr_df.rename(columns={col: f"{col}_ssr" for col in ssr_df.columns if col not in ['project_name', 'route', 'scenario', 'interation']})

    # Mesclar as colunas CSR e SSR
    combined_df = pd.merge(csr_df, ssr_df, on=['project_name', 'route', 'scenario', 'interation'], how='outer')

    # Ajustar o nome da coluna 'benchmark'
    combined_df['benchmark'] = combined_df.apply(lambda row: f"{row['project_name']}-{row['route']}", axis=1)


    # Remover colunas 'render_type_csr' e 'render_type_ssr'
    combined_df = combined_df.drop(columns=['render_type_csr', 'render_type_ssr'], errors='ignore')

    # Reordenar as colunas para manter a consistência
    metrics = [col for col in combined_df.columns if col not in ['project_name', 'benchmark', 'scenario', 'interation', 'route']]
    metrics_sorted = sorted(set([col.replace('_csr', '').replace('_ssr', '') for col in metrics]))
    columns_order = ['project_name', 'benchmark', 'scenario', 'interation']
    for metric in metrics_sorted:
        columns_order.append(f"{metric}_csr")
        columns_order.append(f"{metric}_ssr")

    combined_df = combined_df[columns_order]

    # Salvar o novo DataFrame
    output_path = os.path.join(results_path, 'comparative_performance_evaluation_results.csv')
    combined_df.to_csv(output_path, index=False)
