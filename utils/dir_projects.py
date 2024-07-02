import os

def get_projects_path():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    # Verifica se já está dentro de 'performance-evaluation-analyzer'
    if 'performance-evaluation-analyzer' in current_dir:
        # Encontra o índice onde termina 'performance-evaluation-analyzer'
        index = current_dir.find('performance-evaluation-analyzer') + len('performance-evaluation-analyzer')
        # Corta o caminho até esse ponto e adiciona 'projects'
        base_dir = current_dir[:index]
        projects_path = os.path.join(base_dir, "projects")
    else:
        # Se não encontrou, sobe na hierarquia (caso necessário)
        while not current_dir.endswith("performance-evaluation-analyzer"):
            current_dir = os.path.dirname(current_dir)
        projects_path = os.path.join(current_dir, "projects")
    return projects_path