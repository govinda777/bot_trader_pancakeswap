import os
from pydantic_settings import BaseSettings

class EnvironmentSettings(BaseSettings):
    RPC_URL: str = os.getenv("RPC_URL")
    CHAIN_ID: str = os.getenv("CHAIN_ID")
    PANCAKESWAP_ROUTER_ADDRESS: str = os.getenv("PANCAKESWAP_ROUTER_ADDRESS")
    PANCAKESWAP_ROUTER_ABI: str = os.getenv("PANCAKESWAP_ROUTER_ABI")
    WALLET_ADDRESS: str = os.getenv("WALLET_ADDRESS")
    WALLET_PRIVATE_KEY: str = os.getenv("WALLET_PRIVATE_KEY")
    
    class Config:
        env_file = '.env'


ENV_SETTINGS = EnvironmentSettings()