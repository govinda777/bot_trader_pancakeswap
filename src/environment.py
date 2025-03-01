import os
from pydantic_settings import BaseSettings

class EnvironmentSettings(BaseSettings):
    RPC_URL: str = os.getenv("RPC_URL", "default_rpc_url")
    CHAIN_ID: str = os.getenv("CHAIN_ID", "default_chain_id")
    WALLET_ADDRESS: str = os.getenv("WALLET_ADDRESS")
    WALLET_PRIVATE_KEY: str = os.getenv("WALLET_PRIVATE_KEY")
    PANCAKESWAP_ROUTER_ADDRESS: str = os.getenv("PANCAKESWAP_ROUTER_ADDRESS", "default_address")
    PANCAKESWAP_ROUTER_ABI: str = os.getenv("PANCAKESWAP_ROUTER_ABI", "{}")
    TOKEN_WBNB_ADDRESS: str = os.getenv("TOKEN_WBNB_ADDRESS", "default_address")
    TOKEN_WBNB_ABI: str = os.getenv("TOKEN_WBNB_ABI", "{}")
    
    class Config:
        env_file = '.env'


ENV_SETTINGS = EnvironmentSettings()