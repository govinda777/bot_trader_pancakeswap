import os
from pydantic_settings import BaseSettings

class EnvironmentSettings(BaseSettings):
    RPC_URL: str = os.getenv("RPC_URL", "default_rpc_url")
    CHAIN_ID: str = os.getenv("CHAIN_ID", "default_chain_id")
    PANCAKESWAP_ROUTER_ADDRESS: str = os.getenv("PANCAKESWAP_ROUTER_ADDRESS", "default_address")
    PANCAKESWAP_ROUTER_ABI: str = os.getenv("PANCAKESWAP_ROUTER_ABI", "{}")
    WALLET_ADDRESS: str = os.getenv("WALLET_ADDRESS")
    WALLET_PRIVATE_KEY: str = os.getenv("WALLET_PRIVATE_KEY")
    
    class Config:
        env_file = '.env'


ENV_SETTINGS = EnvironmentSettings()