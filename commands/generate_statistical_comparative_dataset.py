import os
import json
import pandas as pd

def merge_jsons_to_dataframe():
    current_dir = os.path.abspath(__file__)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    results_path = os.path.join(project_dir, 'results')
    # Lista para armazenar os dados dos JSONs
    all_data = []

    # Percorrer recursivamente o diretório de resultados
    for root, _, files in os.walk(results_path):
        if "comparative" in root:
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Adiciona cada métrica à lista
                        if "metrics" in data:
                            all_data.extend(data["metrics"])

    # Transforma a lista de dicionários em um DataFrame
    df = pd.DataFrame(all_data)
    
    # Verifica se os campos 'currentVersion' e 'baselineVersion' são dicionários e os normaliza
    if 'currentVersion' in df.columns and 'baselineVersion' in df.columns:
        df_current = pd.json_normalize(df['currentVersion'])
        df_baseline = pd.json_normalize(df['baselineVersion'])
        
        # Renomear as colunas para distinguir entre currentVersion e baselineVersion
        df_current.columns = [f'current_{col}' for col in df_current.columns]
        df_baseline.columns = [f'baseline_{col}' for col in df_baseline.columns]
        
        # Concatenar os DataFrames de current e baseline com as colunas principais
        df_final = pd.concat([df.drop(['currentVersion', 'baselineVersion'], axis=1), df_current, df_baseline], axis=1)
    else:
        df_final = df

    # Converte a coluna 'statisticalTestU' para float, substituindo valores inválidos por NaN
    df_final['statisticalTestU'] = pd.to_numeric(df_final['statisticalTestU'], errors='coerce')

    # Ajustar a coluna de magnitude: se statisticalTestU for None ou maior que 0.05, definir a magnitude como None
    df_final['magnitude'] = df_final.apply(
        lambda row: None if pd.isnull(row['statisticalTestU']) or row['statisticalTestU'] > 0.05 else row.get('magnitude'),
        axis=1
    )

    output_csv_path = os.path.join(results_path, 'merged_results.csv')
    # Salva o DataFrame final em um arquivo CSV
    df_final.to_csv(output_csv_path, index=False)
    print("Arquivo 'merged_results.csv' gerado com sucesso.")
