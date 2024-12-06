#!/bin/bash

echo "Parando todos os containers em execução..."
docker stop $(docker ps -q)

# Verifica o status
if [ $? -eq 0 ]; then
    echo "Todos os containers foram parados com sucesso."
else
    echo "Nenhum container executando."
fi
