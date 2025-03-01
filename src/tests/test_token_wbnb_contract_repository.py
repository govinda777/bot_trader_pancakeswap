import json
import pytest
from unittest.mock import patch, MagicMock
from web3.contract import Contract
from web3 import Web3
from src.environment import ENV_SETTINGS
from src.repository.token_wbnb_contract_repository import TokenWbnbContractRepository

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
