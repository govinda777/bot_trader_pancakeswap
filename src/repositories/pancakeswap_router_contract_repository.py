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
        
    def approve(self, spender_address, amount_in_wei, chain_id, nonce, gas=200000, gas_price='100'):
        function_call = self.contract.functions.approve(
            spender_address, 
            amount_in_wei
        )
        
        transaction_params = {
            'chainId': chain_id,
            'gas': gas,
            'gasPrice': self.contract.web3.toWei(gas_price, 'gwei'),
            'nonce': nonce,
        }
        
        return self.build_transaction(function_call, transaction_params)
        
