import httpx
from src.environment import ENV_SETTINGS

class HttpClient:
    def __init__(self, client: httpx.AsyncClient = None):
        self.client = client or httpx.AsyncClient()
    
    async def get(self, url: str, params: dict = None, headers: dict = None):
        response = await self.client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

class PricingRepository:
    def __init__(self, 
                 http_client: HttpClient,
                 price_url: str = ENV_SETTINGS.PRICE_URL,
                 price_api_key: str = ENV_SETTINGS.PRICE_API_KEY,
                 price_api_version: str = ENV_SETTINGS.PRICE_API_VERSION):
        self.price_url = price_url
        self.http_client = http_client
        self.price_api_key = price_api_key
        self.price_api_version = price_api_version
    
    async def get_price(self, 
                        sell_amount: int, 
                        chain_id: int = ENV_SETTINGS.CHAIN_ID_MAINNET, 
                        sell_token: str = ENV_SETTINGS.TOKEN_WBNB_ADDRESS_MAINNET, 
                        buy_token: str = ENV_SETTINGS.TOKEN_CAKE_ADDRESS_MAINNET, 
                        **kwargs):
        
        url = f"{self.price_url}/swap/permit2/price"
        
        params = {
            "chainId": chain_id,
            "sellToken": sell_token,
            "buyToken": buy_token,
            "sellAmount": str(sell_amount)
        }
        
        optional_params = [
            "taker", "txOrigin", "swapFeeRecipient", "swapFeeBps", "swapFeeToken", 
            "tradeSurplusRecipient", "gasPrice", "slippageBps", "excludedSources", "sellEntireBalance"
        ]
        
        for param in optional_params:
            if param in kwargs and kwargs[param] is not None:
                params[param] = str(kwargs[param])
        
        headers = {
            "0x-api-key": self.price_api_key,
            "0x-version": self.price_api_version
        }
        
        data = await self.http_client.get(url, params=params, headers=headers)
        
        if "buyAmount" in data and "sellAmount" in data:
            buy_amount = float(data["buyAmount"])
            sell_amount = float(data["sellAmount"])
        
            price = buy_amount / sell_amount
            
            return price
        else:
            raise ValueError("Não foi possível encontrar buyAmount e/ou sellAmount na resposta da API.")    
