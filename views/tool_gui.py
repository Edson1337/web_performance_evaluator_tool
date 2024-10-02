import os
import subprocess
import tkinter as tk
from tkinter import messagebox, Listbox, SINGLE
from commands.evaluate_app_performance import execute_evaluation
from commands.generate_csv import generate_csv
from commands.generate_comparative_dataset import generate_comparative_dataset
from utils.projects_existing import list_projects
from views.add_project_window import open_add_project_window
from views.build_version_window import open_build_version_window

def create_gui():
    root = tk.Tk()
    root.title("Web Performance Evaluator")
    root.geometry("600x500")

    selected_project = None
    selected_version = None
    projects = list_projects()

    def on_project_select(event):
        nonlocal selected_project, selected_version
        w = event.widget
        if w.curselection():
            index = int(w.curselection()[0])
            selected_project = w.get(index)
            versions = projects.get(selected_project, [])
            version_listbox.delete(0, tk.END)
            for version in versions:
                version_listbox.insert(tk.END, version)
            selected_version = None  # Resetar a versão selecionada

    def on_version_select(event):
        nonlocal selected_version
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

    def create_csv_file():
        generate_csv()
        messagebox.showinfo("CSV Generated", "CSV file has been generated and saved in the results directory.")

    def create_comparative_dataset():
        generate_comparative_dataset()
        messagebox.showinfo("Dataset Generated", "Comparative dataset has been generated and saved in the results directory.")

    def start_apps():
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts/start_apps.sh')
        subprocess.call([script_path])

    def stop_apps():
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts/stop_apps.sh')
        subprocess.call([script_path])

    def open_compose_yaml():
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts/select_project.sh')
        subprocess.call([script_path])

    def on_exit():
        stop_apps()
        root.destroy()

    control_frame = tk.LabelFrame(root, text="Application(s) Options", font=("Helvetica", 14, "bold"))
    control_frame.pack(pady=10, padx=20, fill=tk.X, ipady=20)

    start_button = tk.Button(control_frame, text="Start", bg="darkseagreen", fg="white", command=start_apps)
    start_button.pack(side=tk.LEFT, padx=5)

    stop_button = tk.Button(control_frame, text="Stop", bg="lightcoral", fg="white", command=stop_apps)
    stop_button.pack(side=tk.LEFT, padx=5)

    choose_button = tk.Button(control_frame, text="Choose", command=open_compose_yaml)
    choose_button.pack(side=tk.LEFT, padx=5)

    listbox_frame = tk.Frame(root)
    listbox_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=2)

    listbox_frame.grid_rowconfigure(0, weight=1)
    listbox_frame.grid_columnconfigure(0, weight=1)
    listbox_frame.grid_columnconfigure(1, weight=1)

    project_frame = tk.LabelFrame(listbox_frame, text="Projects", font=("Helvetica", 14, "bold"))
    project_frame.grid(row=0, column=0, sticky="nsew", padx=5)

    project_frame.grid_rowconfigure(0, weight=1)
    project_frame.grid_rowconfigure(1, weight=0)
    project_frame.grid_columnconfigure(0, weight=1)

    project_listbox = Listbox(project_frame, selectmode=SINGLE)
    project_listbox.grid(row=0, column=0, sticky="nsew")
    project_listbox.bind('<<ListboxSelect>>', on_project_select)

    add_project_button = tk.Button(project_frame, text="New Project", width=12, bg="green", fg="white", command=lambda: open_add_project_window(root, projects, project_listbox, version_listbox))
    add_project_button.grid(row=1, column=0, sticky='sw', padx=5, pady=5)

    version_frame = tk.LabelFrame(listbox_frame, text="Version", font=("Helvetica", 14, "bold"))
    version_frame.grid(row=0, column=1, sticky="nsew", padx=5)

    version_frame.grid_rowconfigure(0, weight=1)
    version_frame.grid_rowconfigure(1, weight=0)
    version_frame.grid_columnconfigure(0, weight=1)

    version_listbox = Listbox(version_frame, selectmode=SINGLE)
    version_listbox.grid(row=0, column=0, sticky="nsew")
    version_listbox.bind('<<ListboxSelect>>', on_version_select)

    build_versions_button = tk.Button(version_frame, text="Build Versions", width=12, bg="blue", fg="white", command=lambda: open_build_version_window(root, selected_project, selected_version))
    build_versions_button.grid(row=1, column=0, sticky='sw', padx=5, pady=5)

    evaluation_frame = tk.Frame(root)
    evaluation_frame.pack(pady=5)

    route_label = tk.Label(evaluation_frame, text="Route:")
    route_label.pack(side=tk.LEFT, padx=5)

    route_entry = tk.Entry(evaluation_frame)
    route_entry.pack(side=tk.LEFT, padx=5)

    evaluate_button = tk.Button(evaluation_frame, text="Evaluate", command=run_evaluation)
    evaluate_button.pack(side=tk.LEFT, padx=5)

    dataframe_button = tk.Button(root, text="Generate CSV", command=create_csv_file)
    dataframe_button.pack(pady=8)

    comparative_dataset_button = tk.Button(root, text="Generate Comparative Dataset", command=create_comparative_dataset)
    comparative_dataset_button.pack(pady=8)

    exit_button = tk.Button(root, text="Exit", bg="red", fg="white", command=on_exit)
    exit_button.pack(pady=8)

    for project in projects:
        project_listbox.insert(tk.END, project)

    root.mainloop()