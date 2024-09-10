import os
import subprocess
import tkinter as tk
from tkinter import messagebox, Listbox, SINGLE
from commands.evaluate_app_performance import execute_evaluation
from commands.generate_csv import generate_csv
from commands.generate_comparative_dataset import generate_comparative_dataset
from utils.projects_existing import list_projects

selected_project = None
selected_version = None

def on_project_select(event):
    global selected_project, selected_version
    w = event.widget
    if w.curselection():
        index = int(w.curselection()[0])
        selected_project = w.get(index)
        versions = projects[selected_project]
        version_listbox.delete(0, tk.END)
        for version in versions:
            version_listbox.insert(tk.END, version)
        selected_version = None  # Reset the selected version

def on_version_select(event):
    global selected_version
    w = event.widget
    if w.curselection():
        index = int(w.curselection()[0])
        selected_version = w.get(index)

def run_evaluation():
    if selected_project and selected_version:
        project_path = os.path.join(selected_project, selected_version)
        route = route_entry.get()
        execute_evaluation(project_path, route)
    else:
        messagebox.showerror("Selection Error", "Please select a project and a version.")

def create_csv():
    generate_csv()
    messagebox.showinfo("CSV Generated", "CSV file has been generated and saved in the results directory.")

def create_comparative_dataset():
    generate_comparative_dataset()
    messagebox.showinfo("Dataset Generated", "Comparative dataset has been generated and saved in the results directory.")

def start_apps():
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'start_apps.sh')
    subprocess.call([script_path])

def stop_apps():
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'stop_apps.sh')
    subprocess.call([script_path])

def open_compose_yaml():
    # Caminho para o script shell que abre o compose.yaml
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'select_project.sh')
    subprocess.call([script_path])

def on_exit(root):
    stop_apps()  # Executa o script para parar os containers
    root.destroy()  # Fecha a interface

def create_gui():
    global projects, project_listbox, version_listbox, route_entry
    root = tk.Tk()
    root.title("Performance Evaluation Analyzer")
    root.geometry("600x450")

    projects = list_projects()

    # Criar um Frame para conter o Label e os botões Start, Stop, e Choose
    control_frame = tk.LabelFrame(root, text="Application(s) Options", font=("Helvetica", 14, "bold"))
    control_frame.pack(pady=10, padx=20, fill=tk.X, ipady=20)

    # Adicionar botões "Start", "Stop" e "Choose" no Frame
    start_button = tk.Button(control_frame, text="Start", bg="darkseagreen", fg="white", command=start_apps)
    start_button.pack(side=tk.LEFT, padx=5)

    stop_button = tk.Button(control_frame, text="Stop", bg="lightcoral", fg="white", command=stop_apps)
    stop_button.pack(side=tk.LEFT, padx=5)

    choose_button = tk.Button(control_frame, text="Choose", command=open_compose_yaml)
    choose_button.pack(side=tk.LEFT, padx=5)

    # Criar um Frame para conter project_frame e version_frame lado a lado
    listbox_frame = tk.Frame(root)
    listbox_frame.pack(fill=tk.X, expand=True, padx=8, pady=2)

    # Usar grid para melhor controle dos frames
    listbox_frame.grid_rowconfigure(0, weight=1)
    listbox_frame.grid_columnconfigure(0, weight=1)
    listbox_frame.grid_columnconfigure(1, weight=1)

    # Criar o project_frame dentro do listbox_frame
    project_frame = tk.LabelFrame(listbox_frame, text="Projects", font=("Helvetica", 14, "bold"))
    project_frame.grid(row=0, column=0, sticky="nsew", padx=5)

    # Criar o version_frame dentro do listbox_frame
    version_frame = tk.LabelFrame(listbox_frame, text="Version", font=("Helvetica", 14, "bold"))
    version_frame.grid(row=0, column=1, sticky="nsew", padx=5)

    # Defina a altura dos Listboxes
    project_listbox = Listbox(project_frame, selectmode=SINGLE, height=5)
    project_listbox.pack(fill=tk.X, expand=True)
    project_listbox.bind('<<ListboxSelect>>', on_project_select)

    version_listbox = Listbox(version_frame, selectmode=SINGLE, height=5)
    version_listbox.pack(fill=tk.X, expand=True)
    version_listbox.bind('<<ListboxSelect>>', on_version_select)

    evaluation_frame = tk.Frame(root)
    evaluation_frame.pack(pady=5)

    route_label = tk.Label(evaluation_frame, text="Route:")
    route_label.pack(side=tk.LEFT, padx=5)

    route_entry = tk.Entry(evaluation_frame)
    route_entry.pack(side=tk.LEFT, padx=5)

    evaluate_button = tk.Button(evaluation_frame, text="Evaluate", command=run_evaluation)
    evaluate_button.pack(side=tk.LEFT, padx=5)

    dataframe_button = tk.Button(root, text="Generate CSV", command=create_csv)
    dataframe_button.pack(pady=8)

    comparative_dataset_button = tk.Button(root, text="Generate Comparative Dataset", command=create_comparative_dataset)
    comparative_dataset_button.pack(pady=8)

    exit_button = tk.Button(root, text="Exit", bg="red", fg="white", command=lambda: on_exit(root))
    exit_button.pack(pady=8)

    for project in projects:
        project_listbox.insert(tk.END, project)

    root.mainloop()
