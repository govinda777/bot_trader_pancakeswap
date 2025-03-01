import pytest
from src.repositories.pricing_repository import PricingRepository, HttpClient
from src.environment import ENV_SETTINGS

# Garantir que o valor de PRICE_URL está configurado corretamente
@pytest.mark.asyncio
async def test_get_price_real_api():
    # Garantir que o PRICE_URL está presente
    assert ENV_SETTINGS.PRICE_URL != "default_price_url", "Preço URL não está configurado corretamente!"

    # Instanciando o HttpClient
    http_client = HttpClient(client=None)

    # Instanciando o PricingRepository
    pricing_repo = PricingRepository(http_client=http_client)

    # Definindo os parâmetros conforme o curl
    chain_id = 1
    buy_token = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    sell_token = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    sell_amount = 100000000
    taker = "0x70a9f34f9b34c64957b9c401a97bfed35b95049e"
    slippage_bps = 100
    sell_entire_balance = False

    # Chamada real à API para pegar o preço
    price = await pricing_repo.get_price(
        chain_id=chain_id,
        buy_token=buy_token,
        sell_token=sell_token,
        sell_amount=sell_amount,
        taker=taker,
        slippage_bps=slippage_bps,
        sell_entire_balance=sell_entire_balance
    )

    # Verifique se o preço retornado é um número (o que indica que a API retornou um preço válido)
    assert isinstance(price, float), f"O preço retornado deveria ser um float, mas foi {type(price)}"
    assert price > 0, "O preço retornado deve ser maior que zero"
