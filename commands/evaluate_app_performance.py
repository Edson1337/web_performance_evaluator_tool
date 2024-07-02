import os
import json
from utils.settings_files_builder import rewrite_url_in_file, delete_sitespeed_results
from result_summarization.summarized_results_creator import assemble_summarize_results
from sitespeed_run.sitespeed_bat_runner import execute_sitespeed_from_bat
from schema.config_json import parsed_json 
from utils.performance_id_generator import generate_performance_test_id
from utils.app_running import check_port
from utils.recharger_evaluation_json import reset_setup_json
from utils.url_field_creator import create_url

command_cmd = 'sitespeed_executer.bat'
sitespeed_result_path = os.path.normpath('sitespeed-result/')
root_folder_path = os.path.normpath("temp_scenario_settings/")
regex_pattern = r'^.*$'  # Standard regex for matching any file

def execute_evaluation(project_path, route):
    print(f"Executing performance evaluation for project {project_path}")
    print(f"Route: {route}")
    try:
        project_dir = os.path.join(os.getcwd(), f"../projects/{project_path}")
        package_json_path = os.path.join(project_dir, 'package.json')
        
        with open(package_json_path) as f:
            package_json = json.load(f)
            dev_script = package_json['scripts']['dev']
            host = "127.0.0.1"
            port = int(dev_script.split('-p')[1].strip())
            if check_port(host, port):
                project_name = package_json['name']
                parsed_json['performance_evaluation']['app_name'] = project_name
                local_host = f"http://localhost:{port}"
                url = create_url(local_host, route)
                parsed_json['performance_evaluation']['url'] = f"{url}"

                # delete_sitespeed_results(sitespeed_result_path)

                try:
                    print(parsed_json)
                    rewrite_url_in_file(parsed_json)
                    execute_sitespeed_from_bat()
                    generate_performance_test_id(parsed_json)
                    assemble_summarize_results(parsed_json)
                except Exception as error:
                    print(error)
                finally:
                    delete_sitespeed_results(sitespeed_result_path)
                    reset_setup_json(parsed_json)  



        print({'message': 'Process completed successfully'})

    except Exception as error:
        print('Error processing:', error)