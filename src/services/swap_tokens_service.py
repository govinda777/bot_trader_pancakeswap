import datetime
from web3 import Web3
from web3.contract import (
    Contract,
    ContractCaller,
)

from src.environment import ENV_SETTINGS
from src.repositories.pancakeswap_router_contract_repository import PancakeSwapRouterContractRepository
from src.repositories.token_wbnb_contract_repository import TokenWbnbContractRepository
from web3_facade import Web3Facade


class SwapTokensService:
    def __init__(self, 
                 pancakeswap_router_contract_repository: PancakeSwapRouterContractRepository,
                 token_wbnb_contract_repository: TokenWbnbContractRepository,
                 web3: Web3 = Web3Facade().web3,
                 chain_id: int = ENV_SETTINGS.CHAIN_ID,
                 wallet_address: str = ENV_SETTINGS.WALLET_ADDRESS,
                 private_key: str = ENV_SETTINGS.WALLET_PRIVATE_KEY
    ):
        self.web3 = web3
        self.pancakeswap_router_contract_repository = pancakeswap_router_contract_repository
        self.token_wbnb_contract_repository = token_wbnb_contract_repository
        self.chain_id = chain_id
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.nonce = self.web3.eth.get_transaction_count(self.wallet_address)
    
    def swap(self, token_in, token_out, amount_in) -> str:
        amount_in = Web3.to_wei(amount_in, 'ether')
        amount_out_min = 0
        path = [Web3.to_checksum_address(token_in), Web3.to_checksum_address(token_out)]
        to = self.wallet_address

        now = datetime.datetime.now()
        timestamp_atual = int(now.timestamp() * 1000)
        deadline = timestamp_atual + 10000

        transaction = self.pancakeswap_router_contract_repository.swap_exact_tokens_for_tokens(
            amount_in,
            amount_out_min,
            path,
            to,
            deadline,
            self.chain_id,
            200000,
            self.web3.toWei('50', 'gwei')
        )
        
        signed_transaction = self.web3.eth.account.signTransaction(transaction, self.private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return tx_hash.hex()
        
    def approve_spending(self, spender_address, amount) -> str:
        amount_in_wei = self.web3.toWei(amount, 'ether')
        nonce = self.web3.eth.getTransactionCount(self.wallet_address)

        transaction = self.token_wbnb_contract_repository.approve(
            spender_address, 
            amount_in_wei,
            self.chain_id,
            200000,
            self.web3.toWei('100', 'gwei'),
            nonce + 1
        )
        
        signed_transaction = self.web3.eth.account.signTransaction(transaction, self.private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        
        return tx_hash.hex()