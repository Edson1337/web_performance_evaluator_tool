import subprocess


command_cmd = 'sitespeed_executer.bat'

def execute_sitespeed_from_bat():
    print("Try running this project in CMD or PowerShell terminal!")
    try:
        output = subprocess.check_output(command_cmd, shell=True)
        print(f'Output: {output}')
    except subprocess.CalledProcessError as error:
        print(f'Error: {error}')