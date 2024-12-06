import os
import subprocess
from tkinter import messagebox

class AppOperations:
    def __init__(self):
        self.scripts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts')

    def start_builded_app(self, selected_project, selected_version):
        if not selected_project or not selected_version:
            messagebox.showerror("Selection Error", "Please select a project and a version.")
            return

        selected_version_path = os.path.join(selected_project, selected_version)
        project_dir = os.path.abspath(os.path.join(os.getcwd(), f"../projects/{selected_version_path}"))

        compose_file_path = os.path.join(project_dir, "compose.yaml")
        if not os.path.exists(compose_file_path):
            messagebox.showerror("Error", f"No compose.yaml file found in {project_dir}.")
            return

        script_path = os.path.join(self.scripts_dir, "start_apps.sh")
        print(f"Script path: {script_path}")

        try:
            subprocess.run(
                ['bash', script_path, project_dir],
                stdout=None,
                stderr=None,
                text=True,
                check=True
            )
            messagebox.showinfo("Success", "Application started successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to start the application:\n{e}")

    def stop_builded_app(self, selected_project, selected_version):
        if not selected_project or not selected_version:
            messagebox.showerror("Selection Error", "Please select a project and a version.")
            return

        selected_version_path = os.path.join(selected_project, selected_version)
        project_dir = os.path.abspath(os.path.join(os.getcwd(), f"../projects/{selected_version_path}"))

        compose_file_path = os.path.join(project_dir, "compose.yaml")
        if not os.path.exists(compose_file_path):
            messagebox.showerror("Error", f"No compose.yaml file found in {project_dir}.")
            return

        script_path = os.path.join(self.scripts_dir, "stop_apps.sh")
        print(f"Script path: {script_path}")

        try:
            subprocess.run(
                ['bash', script_path, project_dir],
                stdout=None,
                stderr=None,
                text=True,
                check=True
            )
            messagebox.showinfo("Success", "Application stopped successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to stop the application:\n{e}")
