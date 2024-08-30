import tkinter as tk
from tkinter import messagebox, Listbox, SINGLE
from commands.evaluate_app_performance import execute_evaluation
from commands.generate_csv import generate_csv
from commands.generate_comparative_dataset import generate_comparative_dataset
from utils.projects_existing import list_projects
import os

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

def create_gui():
    global projects, project_listbox, version_listbox, route_entry
    root = tk.Tk()
    root.title("Performance Evaluation Analyzer")
    root.geometry("600x600")

    projects = list_projects()

    project_frame = tk.Frame(root)
    project_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    version_frame = tk.Frame(root)
    version_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    project_listbox = Listbox(project_frame, selectmode=SINGLE)
    project_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    project_listbox.bind('<<ListboxSelect>>', on_project_select)

    version_listbox = Listbox(version_frame, selectmode=SINGLE)
    version_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    version_listbox.bind('<<ListboxSelect>>', on_version_select)

    route_label = tk.Label(root, text="Route:")
    route_label.pack(pady=2)
    route_entry = tk.Entry(root)
    route_entry.pack(pady=5)

    evaluate_button = tk.Button(root, text="Evaluate", command=run_evaluation)
    evaluate_button.pack(pady=8)

    dataframe_button = tk.Button(root, text="Generate CSV", command=create_csv)
    dataframe_button.pack(pady=8)

    comparative_dataset_button = tk.Button(root, text="Generate Comparative Dataset", command=create_comparative_dataset)
    comparative_dataset_button.pack(pady=8)

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=8)

    for project in projects:
        project_listbox.insert(tk.END, project)

    root.mainloop()