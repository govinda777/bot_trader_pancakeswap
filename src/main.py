
from datetime import time

from repositories.pricing_repository import PricingRepository


async def main():
    PROFITABILITY = 1.1
    sell_threshold = 200
    stop_order = False  # Variável para controlar a ordem de parada do robô

    print("Olá sou o Robô Vendedor de Token, para interromper o bot pressione ao mesmo tempo CTRL + C")
    time.sleep(5)

    while not stop_order:
        
        try:
            pricing_repository = PricingRepository()
            token_price = await pricing_repository.get_price(1)
            print("Preço em dolar do Token:" + str(token_price))
        except Exception as e:
            print("Error:", str(e))
        time.sleep(5)

        if token_price >= (sell_threshold * PROFITABILITY):
            # Vender tokens se o preço estiver acima ou igual ao limiar de venda
            print("O Preço é maior que o limiar de venda de " + str(sell_threshold))
            print("Portanto, vou vender token")