import json
import os
import re

render_type_sufix_regex = r'-(csr|ssr)$'

def create_file(parsed_json):
    app_name = parsed_json['performance_evaluation']['app_name']
    performance_test_id = parsed_json['performance_evaluation']['performance_evaluation_id']
    del parsed_json['performance_evaluation']['metrics']

    current_dir = os.path.abspath(__file__)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    results_path = os.path.join(project_dir, 'results')

    if not os.path.exists(results_path):
        os.makedirs(results_path)
        print(f"'{results_path}' folder created.")
    else:
        print(f"'{results_path}' already exist.")
    
    project_name = re.sub(render_type_sufix_regex, '', app_name)
    parsed_json['performance_evaluation']['project_name'] = project_name

    sufix_match = re.search(render_type_sufix_regex, app_name)
    if sufix_match:
        render_type_folder = sufix_match.group(1) 
    else:
        render_type_folder = "default"

    output_directory = os.path.join(results_path, project_name, render_type_folder)
    os.makedirs(output_directory, exist_ok=True)

    output_path = os.path.join(output_directory, f"{performance_test_id}.json")
    
    results_string = json.dumps(parsed_json, indent=4)
    print(results_string)
    
    with open(output_path, 'w') as file:
        file.write(results_string)