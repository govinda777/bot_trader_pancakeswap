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
    PRICE_URL: str = os.getenv("PRICE_URL", "default_price_url")
    PRICE_API_KEY: str = os.getenv("PRICE_API_KEY", "")
    PRICE_API_VERSION: str = os.getenv("PRICE_API_VERSION", "v2")
    
    CHAIN_ID_MAINNET: int =  os.getenv("CHAIN_ID_MAINNET", 0)
    TOKEN_WBNB_ADDRESS_MAINNET: str =  os.getenv("TOKEN_WBNB_ADDRESS_MAINNET", "")
    TOKEN_CAKE_ADDRESS_MAINNET: str =  os.getenv("TOKEN_CAKE_ADDRESS_MAINNET", "")
    
    class Config:
        env_file = '.env'


ENV_SETTINGS = EnvironmentSettings()