import json
import pytest
from web3 import Web3
from src.environment import ENV_SETTINGS
from src.repositories.pancakeswap_router_contract_repository import PancakeSwapRouterContractRepository

@pytest.fixture
def web3():
    print("RPC_URL:", ENV_SETTINGS.RPC_URL)
    print("CHAIN_ID:", ENV_SETTINGS.CHAIN_ID)
    print("PANCAKESWAP_ROUTER_ADDRESS:", ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS)
    
    rpc_url = ENV_SETTINGS.RPC_URL
    return Web3(Web3.HTTPProvider(rpc_url))

@pytest.fixture
def pancake_swap_repository(web3) -> PancakeSwapRouterContractRepository:
    pancakeswap_router_address = ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS
    pancakeswap_router_abi = ENV_SETTINGS.PANCAKESWAP_ROUTER_ABI
    return PancakeSwapRouterContractRepository(
        web3=web3,
        pancakeswap_router_address=pancakeswap_router_address,
        pancakeswap_router_abi=pancakeswap_router_abi
    )

def test_repository_initialization(pancake_swap_repository: PancakeSwapRouterContractRepository):
    assert pancake_swap_repository.contract is not None

def test_contract_address(pancake_swap_repository: PancakeSwapRouterContractRepository):
    expected_address = ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS
    assert pancake_swap_repository.web3.is_checksum_address(expected_address)
    assert pancake_swap_repository.contract.address.lower() == expected_address.lower()

def test_web3_isConnected(pancake_swap_repository: PancakeSwapRouterContractRepository):
    assert pancake_swap_repository.web3.is_connected()