#!/bin/bash

set -e

OUTPUT_PATH="build/"

# Limpiamos el directorio:
rm -rf $OUTPUT_PATH
mkdir -p -- $OUTPUT_PATH

# Buildeamos la máquina y ejecutamos el script de build del agente dentro de la misma:
SERVICE_NAME="service"
CONTAINER_NAME="$SERVICE_NAME-container"

docker build . -t builder-scapy-image
docker rm -f builder-scapy 2> /dev/null
docker run --name builder-scapy -v "$PWD"/"$OUTPUT_PATH":/code/build_output -t builder-scapy-image bash -c "pyinstaller --distpath build_output -F src/runner.py"