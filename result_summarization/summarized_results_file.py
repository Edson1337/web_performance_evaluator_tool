import json
import os
import re
import shutil
from utils.route_name import extract_route
from commands.generate_statistical_comparative_dataset import merge_jsons_to_dataframe

RENDER_TYPE_SUFFIX_REGEX = r'-(csr|ssr)$'


def create_file(parsed_json: dict) -> None:
    # Extração de dados importantes
    app_name = parsed_json['performance_evaluation']['app_name']
    performance_test_id = parsed_json['performance_evaluation']['performance_evaluation_id']
    url = parsed_json['performance_evaluation']['url']
    del parsed_json['performance_evaluation']['metrics']

    # Configuração de diretórios
    route = extract_route(url)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    results_path = os.path.join(project_dir, 'results')
    os.makedirs(results_path, exist_ok=True)

    # Criação do nome e caminho do projeto
    project_name = re.sub(RENDER_TYPE_SUFFIX_REGEX, '', app_name)
    parsed_json['performance_evaluation']['project_name'] = project_name
    render_type_folder = re.search(RENDER_TYPE_SUFFIX_REGEX, app_name)
    render_type_folder = render_type_folder.group(1) if render_type_folder else "default"
    output_directory = os.path.join(results_path, project_name, route, render_type_folder)
    os.makedirs(output_directory, exist_ok=True)
    # statiscal_results = parsed_json['performance_evaluation']['scenarios']
    # print(f"o que tem aqui: {parsed_json['performance_evaluation']['scenarios']}")

    # Salvar JSON no diretório de destino
    output_path = os.path.join(output_directory, f"{performance_test_id}.json")
    results_string = json.dumps(parsed_json, indent=4)
    print(results_string)
    with open(output_path, 'w') as file:
        json.dump(parsed_json, file, indent=4)
    print(f"JSON saved to {output_path}")
        
    source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sitespeed-result')
    move_params = {
        'destination_dir': output_directory,
        'source_dir': source_dir,
        'new_folder_name': performance_test_id
    }

    # Mover a pasta de análise para o diretório de destino
    move_analysis_folder(move_params)
    if ('-csr' or '_after') in app_name:
        move_baseline_folder(os.path.dirname(source_dir), os.path.dirname(output_directory))
        
        comparative_dir = output_directory = os.path.join(results_path, project_name, route, "comparative")
        os.makedirs(comparative_dir, exist_ok=True)
        statiscal_results = parsed_json['performance_evaluation']['scenarios']
        for statistical_result in statiscal_results:
            # print(f"o que tem aqui: {statiscal_result}")
            for metric in statistical_result['statisticalResult']['metrics']:
                metric['projectName'] = project_name
                metric['scenarioName'] = statistical_result['scenario_name']
            statistical_path = os.path.join(comparative_dir, f"{performance_test_id}_{statistical_result['scenario_name']}_comparative.json")
            with open(statistical_path, 'w') as file:
                json.dump(statistical_result['statisticalResult'], file, indent=4)
            del statistical_result['statisticalResult']
                
        print(f"Comparative Results saved in: {comparative_dir}")


def move_analysis_folder(params: dict) -> None:
    source_dir = params['source_dir']
    destination_dir = params['destination_dir']
    new_folder_name = params['new_folder_name']

    folders = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]

    if folders:
        original_folder_path = os.path.join(source_dir, folders[0])
        new_folder_path = os.path.join(destination_dir, new_folder_name)

        shutil.move(original_folder_path, new_folder_path)
        print(f"Moved and renamed: {folders[0]} to {new_folder_path}")
    else:
        print(f"No directories found in {source_dir}")


def move_baseline_folder(source_dir: str, results_dir: str) -> None:
    baseline_folder_name = 'baseline_to_statistical'
    baseline_folder_path = os.path.join(source_dir, baseline_folder_name)

    if os.path.exists(baseline_folder_path) and os.path.isdir(baseline_folder_path):
        new_folder_path = os.path.join(results_dir, baseline_folder_name)

        # Move a pasta
        shutil.move(baseline_folder_path, new_folder_path)
        print(f"Moved '{baseline_folder_name}' to '{new_folder_path}'")
    else:
        print(f"No folder named '{baseline_folder_name}' found in '{source_dir}'")