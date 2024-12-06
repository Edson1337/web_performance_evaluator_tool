#!/bin/bash
echo "[SH] Script shell to After Applications started."

url=$1

echo "[SH] Received URL: $url"

configsFolder="configs/"

if [ ! -d "$configsFolder" ]; then
    echo "[SH] $configsFolder"
    echo "[SH] The folder path is not valid."
    exit 1
fi

for configFile in "$configsFolder"/*; do
    echo "------------------ \"$configFile\" ------------------"

    browser=$(jq -r '.browsertime.browser' "$configFile")
    profile=$(jq -r '.browsertime.connectivity.profile' "$configFile")
    device=$(jq -r '.browsertime.chrome.mobileEmulation.deviceName // "desktop"' "$configFile")

    device=$(echo "$device" | tr '[:upper:]' '[:lower:]' | tr -d ' ')

    compare_id="${browser}_${profile}_${device}"

    jq --arg id "$compare_id" '. + {
        "compare": {
            "id": $id,
            "baselinePath": "./baseline_to_statistical",
            "testType": "wilcoxon",
            "wilcoxon": {
                "method": "exact"
            },
            "alternative": "two-sided"
        }
    }' "$configFile" > tmp.$$.json && mv tmp.$$.json "$configFile"

    docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:34.9.0 --config "$configFile" "$url"

    jq 'del(.compare)' "$configFile" > tmp.$$.json && mv tmp.$$.json "$configFile"

    rm -f tmp.$$.json

done

echo "[SH] Script shell ended."
