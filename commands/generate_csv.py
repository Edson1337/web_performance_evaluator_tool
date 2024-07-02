import os
import json
import pandas as pd
from utils.benchmark_name import extract_benchmark

def generate_csv():
    current_dir = os.path.abspath(__file__)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    results_path = os.path.join(project_dir, 'results')
    data = []

    for root, _, files in os.walk(results_path):
        for file in files:
            if file.endswith('.json'):
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
                            iteration_run = metrics.get('interation_run', '')
                            metrics_results = metrics.get('metricsResults', {})

                            data_row = {
                                'id': performance_id,
                                'project_name': project_name,
                                'benchmark': benchmark,
                                'scenario': scenario_name,
                                'iteration': iteration_run,
                            }
                            data_row.update(metrics_results)
                            data.append(data_row)

    df = pd.DataFrame(data)
    output_csv_path = os.path.join(results_path, 'performance_evaluation_results.csv')
    df.to_csv(output_csv_path, index=False)
    print(f"CSV file saved at {output_csv_path}")