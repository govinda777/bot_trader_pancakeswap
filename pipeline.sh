#!/bin/bash

# Criar a imagem Docker
docker build -t bot-trader-pancakeswap .

# Executar o contêiner
docker run --rm bot-trader-pancakeswap