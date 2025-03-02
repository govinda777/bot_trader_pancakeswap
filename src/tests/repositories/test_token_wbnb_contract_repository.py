import pytest
from unittest.mock import MagicMock
from web3.contract import Contract
from web3 import Web3
from src.environment import ENV_SETTINGS
from src.repositories.token_wbnb_contract_repository import TokenWbnbContractRepository

class TestTokenWbnbContractRepository:
    
    def test_initialization(self):
        token_wbnb_address = ENV_SETTINGS.TOKEN_WBNB_ADDRESS
        token_wbnb_abi = ENV_SETTINGS.TOKEN_WBNB_ABI
        
        mocked_web3 = MagicMock(spec=Web3)
        mocked_eth = MagicMock()
        mocked_contract = MagicMock(spec=Contract)

        mocked_web3.eth = mocked_eth
        mocked_eth.contract.return_value = mocked_contract

        repository = TokenWbnbContractRepository(
            web3=mocked_web3,
            token_wbnb_address=token_wbnb_address,
            token_wbnb_abi=token_wbnb_abi
        )

        mocked_web3.eth.contract.assert_called_once()

    def test_approve(self):
        # Dados simulados
        spender_address = "0xSpenderAddress"
        amount_in_wei = 1000
        chain_id = 56  # Exemplo: Binance Smart Chain
        gas = 200000
        gas_price = 1000000000
        nonce = 1

        # Mock setup
        token_wbnb_address = ENV_SETTINGS.TOKEN_WBNB_ADDRESS
        token_wbnb_abi = ENV_SETTINGS.TOKEN_WBNB_ABI

        mocked_web3 = MagicMock(spec=Web3)
        mocked_web3.eth = MagicMock()
        mocked_contract = MagicMock(spec=Contract)

        mocked_web3.eth.contract.return_value = mocked_contract
        mocked_contract.functions.approve.return_value.buildTransaction.return_value = {
            'transaction': 'data'
        }  # O que a função deveria retornar

        repository = TokenWbnbContractRepository(
            web3=mocked_web3,
            token_wbnb_address=token_wbnb_address,
            token_wbnb_abi=token_wbnb_abi
        )

        # Chama o método
        transaction = repository.approve(
            spender_address,
            amount_in_wei,
            chain_id,
            gas,
            gas_price,
            nonce
        )

        # Verifica se a função interna do contrato foi chamada corretamente
        mocked_contract.functions.approve.assert_called_once_with(
            spender_address,
            amount_in_wei
        )

        # Verifica se o buildTransaction foi chamado com os argumentos corretos
        mocked_contract.functions.approve.return_value.buildTransaction.assert_called_once_with({
            'chainId': chain_id,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

        # Verifica se a transação retornada é a esperada
        assert transaction == {'transaction': 'data'}