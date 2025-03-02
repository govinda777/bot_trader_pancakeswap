#!/bin/bash
# set -e  # Termina o script se um comando falhar
# set -x  # Exibe cada comando antes de executá-lo

# Nome da imagem Docker
IMAGE_NAME="bot-trader-pancakeswap:latest"

# Build da imagem Docker
docker build -t $IMAGE_NAME .

# Executa os testes dentro de um novo container usando a imagem criada
docker run --rm $IMAGE_NAME

# Nota: o --rm garante que o container seja removido após a execução, mantendo o ambiente limpo