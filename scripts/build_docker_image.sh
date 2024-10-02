#!/bin/bash

# Arguments
project_dir="$1"
image_name="$2"

# Navegar para o diretório do projeto
cd "$project_dir" || { echo "Failed to navigate to project directory."; exit 1; }

# Construir a imagem Docker
docker build -t "$image_name" .

# Verificar se a construção foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "Docker image '$image_name' built successfully."
    exit 0
else
    echo "Failed to build Docker image '$image_name'." >&2
    exit 1
fi
