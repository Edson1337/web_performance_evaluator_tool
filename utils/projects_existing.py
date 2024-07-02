import os

def list_projects():
    projects_dir = os.path.join(os.getcwd(), "..", 'projects')
    projects = {}
    for project in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, project)
        if os.path.isdir(project_path):
            versions = [d for d in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, d))]
            projects[project] = versions
    return projects