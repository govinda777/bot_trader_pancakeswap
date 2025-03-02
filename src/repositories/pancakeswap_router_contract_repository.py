from typing import Type
from src.environment import ENV_SETTINGS
from web3 import Web3
import json
from web3.contract import (
    Contract
)

from web3_facade import Web3Facade


class PancakeSwapRouterContractRepository:
    def __init__(self, 
                 web3: Web3 = Web3Facade().web3,
                 pancakeswap_router_address: str = ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS,
                 pancakeswap_router_abi: str = ENV_SETTINGS.PANCAKESWAP_ROUTER_ABI
        ):
        self.web3 = web3
        contract_abi = json.loads(pancakeswap_router_abi)

        self.contract: Contract = self.web3.eth.contract(
            address=pancakeswap_router_address, 
            abi=contract_abi
        )
    
    def swap_exact_tokens_for_tokens(
        self,
        amount_in,
        amount_out_min,
        path,
        to,
        deadline,
        chainId,
        gas,
        gasPrice,
        nonce
    ): 
        transaction = self.contract.functions.swapExactTokensForTokens(
            amount_in,
            amount_out_min,
            path,
            to,
            deadline
        )
        
        built_transaction = transaction.build_transaction({
            'chainId': chainId,
            'gas': gas,
            'gasPrice': gasPrice,
            'nonce': nonce
        })
        
        return built_transaction
        
