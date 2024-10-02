import json
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def open_add_project_window(root, projects, project_listbox, version_listbox):
    add_window = tk.Toplevel(root)
    add_window.title("Add New Project")
    add_window.geometry("400x400")

    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    add_window.update_idletasks()
    window_width = add_window.winfo_width()
    window_height = add_window.winfo_height()

    x = root_x + (root_width // 2) - (window_width // 2)
    y = root_y + (root_height // 2) - (window_height // 2)

    add_window.geometry(f"+{x}+{y}")

    frame = tk.Frame(add_window)
    frame.pack(pady=10, padx=10, fill='both', expand=True)
    frame.columnconfigure(1, weight=1)

    row = 0

    project_name_label = tk.Label(frame, text="Project Name:")
    project_name_label.grid(row=row, column=0, sticky='e', pady=5)
    project_name_entry = tk.Entry(frame)
    project_name_entry.grid(row=row, column=1, sticky='we', pady=5)
    row += 1

    evaluation_type_label = tk.Label(frame, text="Evaluation Type:")
    evaluation_type_label.grid(row=row, column=0, sticky='e', pady=5)
    evaluation_type_var = tk.StringVar()
    evaluation_type_var.set("Rendering")
    evaluation_type_dropdown = tk.OptionMenu(frame, evaluation_type_var, "Rendering", "Commit")
    evaluation_type_dropdown.grid(row=row, column=1, sticky='we', pady=5)
    row += 1

    dynamic_fields_frame = tk.Frame(frame)
    dynamic_fields_frame.grid(row=row, column=0, columnspan=2, sticky='we')
    row += 1

    def update_dynamic_fields(*args):
        for widget in dynamic_fields_frame.winfo_children():
            widget.destroy()

        dynamic_fields_frame.entries = {}

        eval_type = evaluation_type_var.get()
        if eval_type == "Rendering":
            ssr_label = tk.Label(dynamic_fields_frame, text="SSR Repo Link:")
            ssr_label.grid(row=0, column=0, sticky='e', pady=5)
            ssr_entry = tk.Entry(dynamic_fields_frame)
            ssr_entry.grid(row=0, column=1, sticky='we', pady=5)
            dynamic_fields_frame.entries['ssr_link'] = ssr_entry

            csr_label = tk.Label(dynamic_fields_frame, text="CSR Repo Link:")
            csr_label.grid(row=1, column=0, sticky='e', pady=5)
            csr_entry = tk.Entry(dynamic_fields_frame)
            csr_entry.grid(row=1, column=1, sticky='we', pady=5)
            dynamic_fields_frame.entries['csr_link'] = csr_entry

        elif eval_type == "Commit":
            repo_label = tk.Label(dynamic_fields_frame, text="Repository Link:")
            repo_label.grid(row=0, column=0, sticky='e', pady=5)
            repo_entry = tk.Entry(dynamic_fields_frame)
            repo_entry.grid(row=0, column=1, sticky='we', pady=5)
            dynamic_fields_frame.entries['repository_link'] = repo_entry

            before_label = tk.Label(dynamic_fields_frame, text="Before Hash:")
            before_label.grid(row=1, column=0, sticky='e', pady=5)
            before_entry = tk.Entry(dynamic_fields_frame)
            before_entry.grid(row=1, column=1, sticky='we', pady=5)
            dynamic_fields_frame.entries['before_hash'] = before_entry

            after_label = tk.Label(dynamic_fields_frame, text="After Hash:")
            after_label.grid(row=2, column=0, sticky='e', pady=5)
            after_entry = tk.Entry(dynamic_fields_frame)
            after_entry.grid(row=2, column=1, sticky='we', pady=5)
            dynamic_fields_frame.entries['after_hash'] = after_entry

    evaluation_type_var.trace('w', update_dynamic_fields)
    update_dynamic_fields()

    create_project_button = tk.Button(frame, text="Create Project", command=lambda: create_project(
        project_name_entry.get(),
        evaluation_type_var.get(),
        dynamic_fields_frame.entries,
        add_window,
        projects,
        project_listbox,
        version_listbox
    ))
    create_project_button.grid(row=row, column=0, columnspan=2, pady=10)
    frame.grid_columnconfigure(1, weight=1)

def create_project(project_name, evaluation_type, entries, add_window, projects, project_listbox, version_listbox):
    project_name = project_name.strip()
    evaluation_type = evaluation_type.lower().strip()

    if not project_name:
        messagebox.showerror("Error", "Please enter a project name.")
        return

    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts/create_project.sh')

    if evaluation_type == "rendering":
        ssr_link = entries.get('ssr_link').get().strip()
        csr_link = entries.get('csr_link').get().strip()

        if not ssr_link or not csr_link:
            messagebox.showerror("Error", "Please provide both SSR and CSR repository links.")
            return

        try:
            subprocess.run(
                ['bash', script_path,
                 project_name,
                 evaluation_type,
                 ssr_link,
                 csr_link],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            ssr_version = f"{project_name}-ssr"
            csr_version = f"{project_name}-csr"
            

            if project_name not in projects:
                projects[project_name] = [ssr_version, csr_version]
                project_listbox.insert(tk.END, project_name)
            else:
                for version_name in [ssr_version, csr_version]:
                    if version_name not in projects[project_name]:
                        projects[project_name].append(version_name)
                        if project_listbox.curselection():
                            selected_index = int(project_listbox.curselection()[0])
                            if project_listbox.get(selected_index) == project_name:
                                version_listbox.insert(tk.END, version_name)

            
            messagebox.showinfo("Project Created", f"Project '{project_name}' has been created with SSR and CSR versions.")

            update_project_name_in_package(project_name, ssr_version)
            update_project_name_in_package(project_name, csr_version)

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip()
            messagebox.showerror("Error", f"Failed to create project '{project_name}':\n{error_message}")
        finally:
            add_window.destroy()

    elif evaluation_type == "commit":
        repository_link = entries.get('repository_link').get().strip()
        before_hash = entries.get('before_hash').get().strip()
        after_hash = entries.get('after_hash').get().strip()

        if not repository_link or not before_hash or not after_hash:
            messagebox.showerror("Error", "Please provide the repository link and both before and after hashes.")
            return

        try:
            subprocess.run(
                ['bash', script_path,
                 project_name,
                 evaluation_type,
                 repository_link,
                 before_hash,
                 after_hash],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            before_version = f"{project_name}_before"
            after_version = f"{project_name}_after"

            if project_name not in projects:
                projects[project_name] = [before_version, after_version]
                project_listbox.insert(tk.END, project_name)
            else:
                for version_name in [before_version, after_version]:
                    if version_name not in projects[project_name]:
                        projects[project_name].append(version_name)
                        if project_listbox.curselection():
                            selected_index = int(project_listbox.curselection()[0])
                            if project_listbox.get(selected_index) == project_name:
                                version_listbox.insert(tk.END, version_name)

            messagebox.showinfo("Project Created", f"Project '{project_name}' has been created with before and after versions.")

            update_project_name_in_package(project_name, before_version)
            update_project_name_in_package(project_name, after_version)

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip()
            messagebox.showerror("Error", f"Failed to create project '{project_name}':\n{error_message}")
        finally:
            add_window.destroy()
    
    else:
        messagebox.showerror("Error", f"Unknown evaluation type '{evaluation_type}'.")

def update_project_name_in_package(project_name, version_name):
    """
    Atualiza o campo 'name' no arquivo package.json localizado em project_dir.

    Args:
        project_name (str): Novo nome para o projeto.
        project_dir (str): Caminho para o diretório do projeto que contém package.json.
    """
    project_dir = os.path.abspath(os.path.join(os.getcwd(), f"../projects/{project_name}/{version_name}"))
    package_json_path = os.path.join(project_dir, 'package.json')

    if not os.path.isfile(package_json_path):
        messagebox.showerror("Erro", f"O arquivo package.json não foi encontrado em: {project_dir}")
        return

    try:
        with open(package_json_path, 'r') as f:
            package_json = json.load(f)

        if 'name' not in package_json:
            messagebox.showerror("Erro", f"A chave 'name' não foi encontrada em {package_json_path}.")
            return

        old_name = package_json['name']
        package_json['name'] = version_name

        with open(package_json_path, 'w') as f:
            json.dump(package_json, f, indent=2)

        messagebox.showinfo("Sucesso", f"O campo 'name' foi atualizado de '{old_name}' para '{version_name}' em {package_json_path}.")

    except json.JSONDecodeError:
        messagebox.showerror("Erro", f"O arquivo {package_json_path} não contém um JSON válido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}") 