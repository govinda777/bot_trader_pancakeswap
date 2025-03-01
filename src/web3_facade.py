
from web3 import Web3
from src.environment import ENV_SETTINGS


class Web3Facade:
    def __init__(self, rpc_url: str = ENV_SETTINGS.RPC_URL):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))