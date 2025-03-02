import json
import pytest
from unittest.mock import patch, MagicMock
from web3.eth import (
    AsyncEth,
    Eth,
)
from web3.contract import (
    Contract,
    ContractCaller,
)

from web3 import Web3
from src.environment import ENV_SETTINGS
from src.repositories.pancakeswap_router_contract_repository import PancakeSwapRouterContractRepository

class TestPancakeSwapRouterContractRepository:

    def test_initialization(self):
        pancakeswap_router_address = ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS
        pancakeswap_router_abi = ENV_SETTINGS.PANCAKESWAP_ROUTER_ABI
        
        mocked_web3 = MagicMock(spec=Web3)
        mocked_eth = MagicMock()
        mocked_contract = MagicMock(spec=Contract)

        mocked_web3.eth = mocked_eth
        mocked_eth.contract.return_value = mocked_contract

        repository = PancakeSwapRouterContractRepository(
            web3=mocked_web3,
            pancakeswap_router_address=pancakeswap_router_address,
            pancakeswap_router_abi=pancakeswap_router_abi
        )

        mocked_web3.eth.contract.assert_called_once()
    
    def test_swap_exact_tokens_for_tokens(self):
        # Dados simulados
        amount_in = 100
        amount_out_min = 90
        path = ["0xTokenA", "0xTokenB"]
        to = "0xRecipientAddress"
        deadline = 1234567890
        chainId = 56  # Exemplo: Binance Smart Chain
        gas = 200000
        gasPrice = 1000000000
        nonce = 1  # Adicionado o nonce

        # Mock setup
        pancakeswap_router_address = ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS
        pancakeswap_router_abi = ENV_SETTINGS.PANCAKESWAP_ROUTER_ABI

        mocked_web3 = MagicMock(spec=Web3)
        mocked_web3.eth = MagicMock()
        mocked_contract = MagicMock()

        mocked_web3.eth.contract.return_value = mocked_contract

        expected_transaction = {
            'to': pancakeswap_router_address,
            'gas': gas,
            'gasPrice': gasPrice,
            'nonce': nonce,
            'data': '0xmockeddata'
        }

        # Corrigido: agora está usando build_transaction() corretamente
        mocked_contract.functions.swapExactTokensForTokens.return_value.build_transaction.return_value = expected_transaction

        repository = PancakeSwapRouterContractRepository(
            web3=mocked_web3,
            pancakeswap_router_address=pancakeswap_router_address,
            pancakeswap_router_abi=pancakeswap_router_abi
        )

        # Chama o método com o nonce incluído
        transaction = repository.swap_exact_tokens_for_tokens(
            amount_in,
            amount_out_min,
            path,
            to,
            deadline,
            chainId,
            gas,
            gasPrice,
            nonce
        )

        # Debug para verificar o que está sendo retornado
        print("Transação retornada:", transaction)
        print("Transação esperada:", expected_transaction)

        # Assegura que transaction é um dicionário e não um MagicMock
        assert isinstance(transaction, dict), f"Esperado dict, mas recebeu {type(transaction)}"

        # Verifica se os valores são iguais
        assert transaction == expected_transaction, f"Diferença entre esperado e recebido: {transaction}"
