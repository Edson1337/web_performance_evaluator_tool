import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import json

def open_build_version_window(root, selected_project, selected_version):
    if not selected_project or not selected_version:
        messagebox.showerror("Selection Error", "Please select a project and a version.")
        return

    selected_version_path = os.path.join(selected_project, selected_version)
    project_dir = os.path.abspath(os.path.join(os.getcwd(), f"../projects/{selected_version_path}"))
    package_json_path = os.path.join(project_dir, 'package.json')

    try:
        with open(package_json_path, 'r') as f:
            package_json = json.load(f)
            scripts = package_json.get('scripts', {})
            script_keys = list(scripts.keys())
            if not script_keys:
                messagebox.showerror("Error", f"No scripts found in package.json at {selected_version_path}")
                return
    except FileNotFoundError:
        messagebox.showerror("Error", f"package.json not found in {selected_version_path}")
        return
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Failed to parse package.json in {selected_version_path}")
        return

    build_window = tk.Toplevel(root)
    build_window.title("Build Version")
    build_window.geometry("400x350")

    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    build_window.update_idletasks()
    window_width = build_window.winfo_width()
    window_height = build_window.winfo_height()

    x = root_x + (root_width // 2) - (window_width // 2)
    y = root_y + (root_height // 2) - (window_height // 2)

    build_window.geometry(f"+{x}+{y}")

    frame = tk.Frame(build_window)
    frame.pack(pady=10, padx=10, fill='both', expand=True)
    frame.columnconfigure(1, weight=1)

    row = 0

    version_label = tk.Label(frame, text=f"Version: {selected_version}")
    version_label.grid(row=row, column=0, columnspan=2, pady=5)
    row += 1

    init_type_label = tk.Label(frame, text="Initialization Type:")
    init_type_label.grid(row=row, column=0, sticky='e', pady=5)
    init_type_var = tk.StringVar()
    init_type_var.set(script_keys[0])
    init_type_dropdown = tk.OptionMenu(frame, init_type_var, *script_keys)
    init_type_dropdown.grid(row=row, column=1, sticky='we', pady=5)
    row += 1

    package_manager_label = tk.Label(frame, text="Package Manager:")
    package_manager_label.grid(row=row, column=0, sticky='e', pady=5)
    package_manager_var = tk.StringVar()
    package_manager_var.set("npm")
    package_manager_dropdown = tk.OptionMenu(frame, package_manager_var, "npm", "pnpm", "yarn")
    package_manager_dropdown.grid(row=row, column=1, sticky='we', pady=5)
    row += 1

    port_label = tk.Label(frame, text="Port:")
    port_label.grid(row=row, column=0, sticky='e', pady=5)
    port_entry = tk.Entry(frame)
    port_entry.grid(row=row, column=1, sticky='we', pady=5)
    row += 1
    
    package_json_dict = {'path': package_json_path, 'file': package_json}
    print(package_json_dict)

    build_button = tk.Button(frame, text="Build", command=lambda: build_version(
        package_manager_var.get(),
        init_type_var.get(),
        port_entry.get(),
        project_dir,
        selected_version,
        build_window,
        package_json_path
    ))
    build_button.grid(row=row, column=0, columnspan=2, pady=10)

    frame.grid_columnconfigure(1, weight=1)

def build_version(package_manager, init_type, port, project_dir, selected_version, build_window, package_json_path):
    if port:
        if not port.isdigit() or not (1 <= int(port) <= 65535):
            messagebox.showerror("Invalid Port", "Please enter a valid port number between 1 and 65535.")
            return
    else:
        messagebox.showerror("Invalid Port", "Please enter a port number.")
        return

    with open(package_json_path, 'r') as f:
        package_json = json.load(f)
        
    print(package_json)
    package_json['executionPort'] = port

    with open(package_json_path, 'w') as f:
        json.dump(package_json, f, indent=2)

    if package_manager == 'npm':
        # lock_file = 'package-lock.json'
        install_command = f'{package_manager} install --production'
    elif package_manager == 'pnpm':
        lock_file = 'pnpm-lock.yaml'
        install_command = f'{package_manager} install --prod'
    elif package_manager == 'yarn':
        lock_file = 'yarn.lock'
        install_command = f'{package_manager} install --production'
    else:
        messagebox.showerror("Error", f"Unsupported package manager '{package_manager}'.")
        return

    dockerfile_content = f"""
    FROM node:18-slim

    # Definindo o diretório de trabalho dentro do container
    WORKDIR /app

    # Copiando o package.json para o container
    COPY package*.json ./

    # Instalando as dependências
    RUN {install_command}

    # Copiando o restante do código da aplicação
    COPY . .

    # Expondo a porta {port}
    EXPOSE {port}

    # Definindo a variável de ambiente PORT
    ENV PORT {port}

    # Comando para iniciar a aplicação
    CMD ["{package_manager}", "run", "{init_type}"]
    """

    dockerfile_path = os.path.join(project_dir, 'Dockerfile')
    try:
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content.strip())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create Dockerfile: {e}")
        return

    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts/build_docker_image.sh'))

    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"Script build_docker_image.sh not found at {script_path}.")
        return

    image_name = selected_version.lower().replace(' ', '_')

    try:
        result = subprocess.run(
            ['bash', script_path, project_dir, image_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        print(result.stdout)
        messagebox.showinfo("Success", f"Docker image '{image_name}' built successfully.")
    except subprocess.CalledProcessError as e:
        
        error_message = e.stderr.strip() if e.stderr else "An error occurred while building the Docker image."
        messagebox.showerror("Error", f"Failed to build Docker image:\n{error_message}")
    finally:
        build_window.destroy()
