#!/bin/bash
set -x

# Adiciona o diretório atual ao PYTHONPATH
export PYTHONPATH=$(pwd)

# Ativa o ambiente virtual
source $(poetry env info --path)/bin/activate

# Carrega as variáveis de ambiente
source .env  # Carregando manualmente o .env (opcional)

# Instala as dependências.
poetry install

# Executa os testes
poetry run pytest

# Verifica os valores carregados
echo "RPC_URL: $RPC_URL"
echo "CHAIN_ID: $CHAIN_ID"
echo "PANCAKESWAP_ROUTER_ADDRESS: $PANCAKESWAP_ROUTER_ADDRESS"