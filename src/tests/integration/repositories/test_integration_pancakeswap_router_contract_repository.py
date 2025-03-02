import time
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


def test_swap_exact_tokens_for_tokens(pancake_swap_repository: PancakeSwapRouterContractRepository):
    # 1) Preparando parâmetros
    token_in = Web3.to_checksum_address(ENV_SETTINGS.TOKEN_WBNB_ADDRESS)
    token_out = Web3.to_checksum_address(ENV_SETTINGS.TOKEN_CAKE_ADDRESS)
    to = Web3.to_checksum_address(ENV_SETTINGS.WALLET_ADDRESS)

    amount_in_ether = 0.01
    amount_in_wei = Web3.to_wei(amount_in_ether, 'ether')
    amount_out_min = int(amount_in_wei * 0.95)  # Exemplo de 5% de slippage
    path = [token_in, token_out]
    deadline = int(time.time()) + 600  # 10 minutos
    chain_id = int(ENV_SETTINGS.CHAIN_ID)
    private_key = ENV_SETTINGS.WALLET_PRIVATE_KEY

    # 2) Chamando o método que agora calcula o melhor gas automaticamente
    tx_receipt = pancake_swap_repository.swap_exact_tokens_for_tokens_com_checks(
        private_key=private_key,
        amount_in_wei=amount_in_wei,
        amount_out_min=amount_out_min,
        path=path,
        to=to,
        deadline=deadline,
        chain_id=chain_id
    )

    # 3) Verificando se a transação foi bem-sucedida
    assert tx_receipt.status == 1, "A transação de swap falhou"
    print(f"Transação realizada com sucesso. Hash: {tx_receipt.transactionHash.hex()}")