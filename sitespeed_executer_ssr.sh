#!/bin/bash
echo "[SH] Script shell started."

# Definindo o diretório raiz e o diretório de configurações
rootFolder="./temp_scenario_settings/"
configsFolder="${rootFolder}configs/"

# Verificando se o diretório de configurações existe
if [ ! -d "$configsFolder" ]; then
    echo "[SH] $configsFolder"
    echo "[SH] O caminho da pasta não é válido."
    exit 1
fi

# Iterando sobre cada arquivo de configuração encontrado no diretório
for configFile in "$configsFolder"/*; do
    echo "------------------ \"$configFile\" ------------------"

    # Extraindo valores do JSON
    browser=$(jq -r '.browsertime.browser' "$configFile")
    profile=$(jq -r '.browsertime.connectivity.profile' "$configFile")
    device=$(jq -r '.browsertime.chrome.mobileEmulation.deviceName // "desktop"' "$configFile")

    # Normalizando o nome do device (substituir espaços por "")
    device=$(echo "$device" | tr '[:upper:]' '[:lower:]' | tr -d ' ')

    # Gerando um ID dinâmico usando os valores extraídos
    compare_id="${browser}_${profile}_${device}"

    # Adicionando o objeto "compare" ao arquivo JSON usando jq
    jq --arg id "$compare_id" '. + {
        "compare": {
            "id": $id,
            "baselinePath": "./baseline_to_statistical",
            "saveBaseline": true,
            "testType": "mannwhitneyu",
            "alternative": "two-sided",
            "mannwhitneyu": {
                "useContinuity": false,
                "method": "auto"
            }
        }
    }' "$configFile" > tmp.$$.json && mv tmp.$$.json "$configFile"

    # Executando o Docker para rodar o sitespeed.io com a configuração atual
    docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:34.9.0 --config "$configFile" "${rootFolder}urls.txt"

    # Removendo o objeto "compare" do arquivo JSON usando jq
    jq 'del(.compare)' "$configFile" > tmp.$$.json && mv tmp.$$.json "$configFile"

    # Removendo o arquivo temporário
    rm -f tmp.$$.json

done

echo "[SH] Script shell ended."
