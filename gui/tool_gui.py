import tkinter as tk
from tkinter import messagebox, Listbox, SINGLE, Entry
from commands.evaluate_app_performance import execute_evaluation
from commands.generate_csv import generate_csv
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
        route = route_entry.get().strip()
        execute_evaluation(project_path, route)
    else:
        messagebox.showerror("Selection Error", "Please select a project, a version, and enter a route.")

def create_csv():
    generate_csv()
    messagebox.showinfo("CSV Generated", "CSV file has been generated and saved in the results directory.")

def create_gui():
    global projects, project_listbox, version_listbox, route_entry
    root = tk.Tk()
    root.title("Performance Evaluation Analyzer")
    root.geometry("500x600")

    projects = list_projects()

    project_frame = tk.Frame(root)
    project_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    version_frame = tk.Frame(root)
    version_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    route_frame = tk.Frame(root)
    route_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)

    project_listbox = Listbox(project_frame, selectmode=SINGLE)
    project_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    project_listbox.bind('<<ListboxSelect>>', on_project_select)

    version_listbox = Listbox(version_frame, selectmode=SINGLE)
    version_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    version_listbox.bind('<<ListboxSelect>>', on_version_select)

    route_label = tk.Label(route_frame, text="Route:")
    route_label.pack(side=tk.LEFT, padx=5)

    route_entry = Entry(route_frame)
    route_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    evaluate_button = tk.Button(root, text="Evaluate", command=run_evaluation)
    evaluate_button.pack(pady=10)

    dataframe_button = tk.Button(root, text="Generate CSV", command=create_csv)
    dataframe_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=10)

    for project in projects:
        project_listbox.insert(tk.END, project)

    root.mainloop()