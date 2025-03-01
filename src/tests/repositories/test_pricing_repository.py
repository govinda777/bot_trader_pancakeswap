import pytest
import logging
from httpx import HTTPError
from repositories.pricing_repository import HttpClient, PricingRepository
from src.environment import ENV_SETTINGS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_get_price_integration():
    """
    Teste de integração que realmente faz a chamada à API do 0x para coletar
    o preço de WBNB -> CAKE na rede BSC Mainnet. Verifica se o preço retornado é maior que zero.
    """
    # Instancia o HttpClient real (sem mocks)
    http_client = HttpClient()

    # Cria o repositório de preços usando as credenciais/URL do EnvironmentSettings
    pricing_repo = PricingRepository(http_client=http_client)

    # Variáveis configuradas para a BSC Mainnet
    chain_id = 56  # Hard-coded para BSC Mainnet
    wbnb_address = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"  # Endereço de WBNB (Mainnet)
    cake_address = "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82"  # Endereço de CAKE (Mainnet)
    sell_amount = 100000000  # Exemplo: 0.1 WBNB (ajuste conforme precisão desejada)

    # Parâmetros opcionais que podem personalizar como a troca é executada na API
    optional_params = {
        # "taker": O endereço do usuário que está executando a operação de swap.
        # Isso pode ser usado para análises de taxas ou para rotas específicas que exigem um endereço de taker.
        "taker": "0x70a9f34f9b34c64957b9c401a97bfed35b95049e",

        # "slippageBps": Define o slippage máximo permitido para a operação, em basis points (bps).
        # 100 bps corresponde a 1% de slippage. Se o preço mudar mais que essa porcentagem durante a execução,
        # a operação pode ser revertida para evitar custos inesperados.
        "slippageBps": "100",

        # "sellEntireBalance": Um booleano que indica se o usuário deseja vender todo o saldo do token vendido.
        # Configurado como "false" aqui, o que significa que apenas a quantidade especificada em sell_amount é vendida.
        # Se configurado para "true", ignora o sellAmount e tenta vender todo o saldo do token presente na carteira especificada.
        "sellEntireBalance": "false"
    }

    try:
        logger.info("Realizando chamada à API do 0x...")
        logger.info(f"Parâmetros: chain_id={chain_id}, sell_token={wbnb_address}, buy_token={cake_address}, sell_amount={sell_amount}")
        
        price = await pricing_repo.get_price(
            chain_id=chain_id,
            sell_token=wbnb_address,
            buy_token=cake_address,
            sell_amount=sell_amount,
            **optional_params
        )

        assert price > 0, "O preço retornado pela API deveria ser maior que 0."
        logger.info(f"Teste OK: Preço obtido = {price}")

    except HTTPError as exc:
        logger.error(f"Falha na comunicação com a API do 0x: {exc}")
        pytest.fail(f"Falha na comunicação com a API do 0x: {exc}")
    except ValueError as exc:
        logger.error(f"Resposta inválida do 0x (falta buyAmount ou sellAmount): {exc}")
        pytest.fail(f"Resposta inválida do 0x (falta buyAmount ou sellAmount): {exc}")