import json
import pytest
from web3 import Web3
from environment import ENV_SETTINGS, EnvironmentSettings
from pancakeswap_router_contract_repository import PancakeSwapRouterContractRepository

@pytest.fixture
def web3(env_settings: EnvironmentSettings):
    
    print("RPC_URL:", env_settings.RPC_URL)
    print("CHAIN_ID:", env_settings.CHAIN_ID)
    print("PANCAKESWAP_ROUTER_ADDRESS:", env_settings.PANCAKESWAP_ROUTER_ADDRESS)
    
    rpc_url = env_settings.RPC_URL
    return Web3(Web3.HTTPProvider(rpc_url))

@pytest.fixture
def pancake_swap_repository(web3: Web3, env_settings: EnvironmentSettings) -> PancakeSwapRouterContractRepository:
    pancakeswap_router_address = env_settings.PANCAKESWAP_ROUTER_ADDRESS
    pancakeswap_router_abi = env_settings.PANCAKESWAP_ROUTER_ABI
    return PancakeSwapRouterContractRepository(
        web3=web3,
        pancakeswap_router_address=pancakeswap_router_address,
        pancakeswap_router_abi=pancakeswap_router_abi
    )

def test_repository_initialization(
    pancake_swap_repository: PancakeSwapRouterContractRepository
    ):
    assert pancake_swap_repository.pancakeswap_router_contract is not None

def test_contract_address(
    pancake_swap_repository: PancakeSwapRouterContractRepository,
    env_settings: EnvironmentSettings
    ):
    expected_address = env_settings.PANCAKESWAP_ROUTER_ADDRESS
    assert pancake_swap_repository.web3.is_checksum_address(expected_address)
    assert pancake_swap_repository.pancakeswap_router_contract.address == expected_address
    
def test_web3_isConnected(
    pancake_swap_repository: PancakeSwapRouterContractRepository
    ):
    assert pancake_swap_repository.web3.is_connected()