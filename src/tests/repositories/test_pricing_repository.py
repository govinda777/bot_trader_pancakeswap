import pytest
import httpx
from httpx import Response
from repositories.pricing_repository import PricingRepository
from src.environment import ENV_SETTINGS

@pytest.mark.asyncio
async def test_get_price():
    async def mock_get(url: str, headers: dict = None):
        return {"price": "123.45"}
    
    class MockHttpClient:
        async def get(self, url: str, headers: dict = None):
            return await mock_get(url, headers)
    
    http_client = MockHttpClient()
    pricing_repo = PricingRepository(http_client=http_client, price_url="https://mock-api.com")
    
    price = await pricing_repo.get_price(chain_id=1, sell_token="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", buy_token="0xdac17f958d2ee523a2206206994597c13d831ec7", sell_amount=100)
    assert price == 123.45
