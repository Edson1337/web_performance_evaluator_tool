import os
import json
import pandas as pd
import re
from utils.benchmark_name import extract_benchmark

# Regex para capturar JSONs com o padrão específico
json_file_pattern = re.compile(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.json')

def generate_csv():
    current_dir = os.path.abspath(__file__)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    results_path = os.path.join(project_dir, 'results')
    dataframes_folder = os.path.join(results_path, 'dataframes')
    os.makedirs(dataframes_folder, exist_ok=True)
    data = []

    for root, dirs, files in os.walk(results_path):
        # Ignora a pasta 'baseline_to_statistical' e pastas que correspondem ao padrão de nomes dos JSONs
        dirs[:] = [d for d in dirs if d != ('baseline_to_statistical' or 'comparative') and not json_file_pattern.match(d)]

        for file in files:
            if json_file_pattern.match(file):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    parsed_json = json.load(f)
                    evaluation = parsed_json.get('performance_evaluation', {})
                    scenarios = evaluation.get('scenarios', [])
                    performance_id = evaluation.get('performance_evaluation_id', '')
                    project_name = evaluation.get('project_name', '')
                    app_name = evaluation.get('app_name', '')
                    url = evaluation.get('url', '')

                    benchmark = extract_benchmark(url, app_name)

                    for scenario in scenarios:
                        scenario_name = scenario.get('scenario_name', '')
                        detailed_metrics = scenario.get('detailedMetricsResults', [])
                        for metrics in detailed_metrics:
                            interation_run = metrics.get('interation_run', '')
                            metrics_results = metrics.get('metricsResults', {})

                            data_row = {
                                'id': performance_id,
                                'project_name': project_name,
                                'benchmark': benchmark,
                                'scenario': scenario_name,
                                'interation': interation_run,
                            }
                            data_row.update(metrics_results)
                            data.append(data_row)

    df = pd.DataFrame(data)
    output_csv_path = os.path.join(dataframes_folder, 'performance_evaluation_results.csv')
    df.to_csv(output_csv_path, index=False)
    print(f"CSV file saved at {output_csv_path}")
