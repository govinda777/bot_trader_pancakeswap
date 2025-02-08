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
from environment import ENV_SETTINGS
from pancakeswap_router_contract_repository import PancakeSwapRouterContractRepository

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
        