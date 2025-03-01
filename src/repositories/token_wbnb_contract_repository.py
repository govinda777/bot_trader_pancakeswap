from typing import Type
from src.environment import ENV_SETTINGS
from web3 import Web3
import json
from web3.contract import (
    Contract
)

from web3_facade import Web3Facade


class TokenWbnbContractRepository:
    def __init__(self,
                 web3: Web3 = Web3Facade().web3,
                 token_wbnb_address: str = ENV_SETTINGS.TOKEN_WBNB_ADDRESS,
                 token_wbnb_abi: str = ENV_SETTINGS.TOKEN_WBNB_ABI
        ):
        self.web3 = web3
        contract_abi = json.loads(token_wbnb_abi)
        
        token_wbnb_address = Web3.to_checksum_address(ENV_SETTINGS.TOKEN_WBNB_ADDRESS)
        
        self.contract: Contract = self.web3.eth.contract(
            address=token_wbnb_address,
            abi=contract_abi
        )