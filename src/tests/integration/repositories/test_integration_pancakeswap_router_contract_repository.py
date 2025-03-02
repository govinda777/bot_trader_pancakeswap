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

def test_swap_exact_tokens_for_tokens(pancake_swap_repository: PancakeSwapRouterContractRepository, web3: Web3):
    token_in = Web3.to_checksum_address(ENV_SETTINGS.TOKEN_WBNB_ADDRESS)
    token_out = Web3.to_checksum_address(ENV_SETTINGS.TOKEN_CAKE_ADDRESS)
    to = Web3.to_checksum_address(ENV_SETTINGS.WALLET_ADDRESS)

    amount_in_ether = 0.01  # Valor a ser trocado em ether
    amount_in_wei = Web3.to_wei(amount_in_ether, 'ether')
    amount_out_min = int(amount_in_wei * 0.95)  # Aplicando 5% de slippage
    path = [token_in, token_out]
    deadline = int(time.time()) + 600  # 10 minutos
    chain_id = int(ENV_SETTINGS.CHAIN_ID)
    gas = 500000  # Aumento do limite de gás
    gas_price = web3.to_wei('50', 'gwei')

    # Obtendo a conta
    account = web3.eth.account.from_key(ENV_SETTINGS.WALLET_PRIVATE_KEY)
    nonce = web3.eth.get_transaction_count(account.address)
    balance = web3.eth.get_balance(account.address)

    # Cálculo do custo total da transação (transação + gás)
    gas_cost = gas * gas_price
    total_cost = amount_in_wei + gas_cost  # Total que deve estar disponível na conta

    print(f"=== Test Started ===")
    print(f"Total Cost (Transaction + Gas): {web3.from_wei(total_cost, 'ether')} BNB")

    if balance < total_cost:
        raise ValueError("Saldo insuficiente para cobrir a transação.")

    # Verifica saldo e allowance
    token_contract = web3.eth.contract(address=token_in, abi=ENV_SETTINGS.TOKEN_WBNB_ABI)
    token_balance = token_contract.functions.balanceOf(account.address).call()
    if token_balance < amount_in_wei:
        raise ValueError("Saldo insuficiente de WBNB.")

    allowance = token_contract.functions.allowance(account.address, ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS).call()
    if allowance < amount_in_wei:
        approve_tx = token_contract.functions.approve(
            ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS, amount_in_wei
        ).build_transaction({
            'chainId': chain_id, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce
        })
        signed_approve_tx = account.sign_transaction(approve_tx)
        approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.raw_transaction)
        web3.eth.wait_for_transaction_receipt(approve_tx_hash, timeout=120)
        nonce += 1  # Atualiza nonce

    # Simulação antes de executar
    try:
        simulation = pancake_swap_repository.swap_exact_tokens_for_tokens(
            amount_in_wei, amount_out_min, path, to, deadline, chain_id, gas, gas_price, nonce
        )
        print(f"Simulation result: {simulation}")
    except Exception as e:
        raise ValueError("Simulação de transação falhou.")

    # Criando e enviando transação
    transaction = pancake_swap_repository.swap_exact_tokens_for_tokens(
        amount_in_wei, amount_out_min, path, to, deadline, chain_id, gas, gas_price, nonce
    )
    signed_transaction = account.sign_transaction(transaction)
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

    if tx_receipt.status != 1:
        raise ValueError(f"Transação falhou: {tx_hash.hex()}")
    
    print("Transaction successful with hash:", tx_hash.hex())
    
