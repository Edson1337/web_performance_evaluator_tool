import os
import subprocess

script_ssr_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sitespeed_executer_ssr.sh')
command_to_ssr = f'bash {script_ssr_path}'
script_csr_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sitespeed_executer_csr.sh')
command_to_csr = f'bash {script_csr_path}'

def execute_sitespeed_from_shell_script(parsed_json: dict):
    print("Try running this project in CMD or PowerShell terminal!")
    try:
        # Criando o diretório antes de executar o script
        directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'baseline_to_statistical')
        os.makedirs(directory_path, exist_ok=True)
        print(f'Diretório {directory_path} criado ou já existente.')

        if "ssr" not in parsed_json["performance_evaluation"]["app_name"]:
            print("Script para a analise com Compare iniciado")
            process = subprocess.Popen(command_to_csr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            print("Script para a Baseline iniciado")
            process = subprocess.Popen(command_to_ssr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Imprimindo a saída em tempo real
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8').strip())
        
        process.stdout.close()
        process.wait()
    except subprocess.CalledProcessError as error:
        print(f'Error: {error}')
