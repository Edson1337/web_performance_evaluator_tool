#!/bin/bash
compose_dir="$1"

# Verifica se o diretório existe
if [ ! -d "$compose_dir" ]; then
  echo "Project directory '$compose_dir' not found."
  exit 1
fi

# Navega até o diretório
cd "$compose_dir" || { echo "Failed to navigate to project directory."; exit 1; }

# Verifica se o docker-compose.yml ou compose.yaml existe no diretório
if [ -f "docker-compose.yml" ]; then
  compose_file="docker-compose.yml"
elif [ -f "compose.yaml" ]; then
  compose_file="compose.yaml"
else
  echo "No docker-compose.yml or compose.yaml file found in '$compose_dir'."
  exit 1
fi

# Verifica qual comando Docker Compose está disponível e usa o correto
if command -v docker-compose &> /dev/null; then
  compose_cmd="docker-compose"
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
  compose_cmd="docker compose"
else
  echo "Neither docker-compose nor docker compose is installed."
  exit 1
fi

# Para o container com o Docker Compose
$compose_cmd -f "$compose_file" down
if [ $? -ne 0 ]; then
  echo "Failed to stop Docker Compose."
  exit 1
fi

echo "Docker Compose stopped successfully."
