import os
import subprocess


def execute_sitespeed_from_shell_script(parsed_json: dict):
    url = parsed_json["performance_evaluation"]["url"]

    script_ssr_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'sitespeed_executer_baseline.sh')
    script_csr_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'sitespeed_executer_comparative.sh')
    
    command_to_ssr = f'bash {script_ssr_path} {url}'
    command_to_csr = f'bash {script_csr_path} {url}'

    print("Starting Evaluation...")
    try:
        directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'baseline_to_statistical')
        os.makedirs(directory_path, exist_ok=True)
        print(f'Directory {directory_path} created or already existing.')
        
        if ("ssr" or "_before") not in parsed_json["performance_evaluation"]["app_name"]:
            print("Script for analysis with Compare started")
            process = subprocess.Popen(command_to_csr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        else:
            print("Script for Baseline started")
            process = subprocess.Popen(command_to_ssr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8').strip())
        
        process.stdout.close()
        process.wait()
    except subprocess.CalledProcessError as error:
        print(f'Error: {error}')
