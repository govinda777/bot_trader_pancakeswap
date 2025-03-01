import json
import pytest
from web3 import Web3
from src.environment import ENV_SETTINGS
from src.repository.token_wbnb_contract_repository import TokenWbnbContractRepository

@pytest.fixture
def web3():
    print("RPC_URL:", ENV_SETTINGS.RPC_URL)
    print("CHAIN_ID:", ENV_SETTINGS.CHAIN_ID)
    print("TOKEN_WBNB_ADDRESS:", ENV_SETTINGS.TOKEN_WBNB_ADDRESS)
    
    rpc_url = ENV_SETTINGS.RPC_URL
    return Web3(Web3.HTTPProvider(rpc_url))

@pytest.fixture
def token_wbnb_repository(web3) -> TokenWbnbContractRepository:
    token_wbnb_address = ENV_SETTINGS.TOKEN_WBNB_ADDRESS
    token_wbnb_abi = ENV_SETTINGS.TOKEN_WBNB_ABI
    return TokenWbnbContractRepository(
        web3=web3,
        token_wbnb_address=token_wbnb_address,
        token_wbnb_abi=token_wbnb_abi
    )

def test_repository_initialization(token_wbnb_repository: TokenWbnbContractRepository):
    assert token_wbnb_repository.contract is not None

def test_contract_address(token_wbnb_repository: TokenWbnbContractRepository):
    expected_address = ENV_SETTINGS.TOKEN_WBNB_ADDRESS
    assert token_wbnb_repository.contract.address.lower() == expected_address.lower()

def test_web3_isConnected(token_wbnb_repository: TokenWbnbContractRepository):
    assert token_wbnb_repository.web3.is_connected()
