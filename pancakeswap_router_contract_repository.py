from typing import Type
from environment import ENV_SETTINGS
from web3 import Web3
import json
from web3.contract import (
    Contract,
    ContractCaller,
)


class PancakeSwapRouterContractRepository:
    def __init__(self, 
                 web3: Web3,
                 pancakeswap_router_address: str = ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS,
                 pancakeswap_router_abi: str = ENV_SETTINGS.PANCAKESWAP_ROUTER_ABI
        ):
        self.web3 = web3
        contract_abi = json.loads(pancakeswap_router_abi)
        
        chain_id = ENV_SETTINGS.CHAIN_ID
        account = ENV_SETTINGS.WALLET_ADDRESS
        private_key = ENV_SETTINGS.WALLET_PRIVATE_KEY

        self.pancakeswap_router_contract: Contract = self.web3.eth.contract(
            address=pancakeswap_router_address, 
            abi=contract_abi
        )
        
