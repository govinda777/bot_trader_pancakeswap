import logging
from typing import List, Optional, Dict, Any
from web3 import Web3
from web3.contract import Contract
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
import json
import time

from src.environment import ENV_SETTINGS
from web3_facade import Web3Facade

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("PancakeSwapRouter")


class PancakeSwapRouterContractRepository:
    def __init__(
        self,
        web3: Web3 = Web3Facade().web3,
        pancakeswap_router_address: str = ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS,
        pancakeswap_router_abi: str = ENV_SETTINGS.PANCAKESWAP_ROUTER_ABI
    ):
        self.web3 = web3
        contract_abi = json.loads(pancakeswap_router_abi)
        self.contract: Contract = self.web3.eth.contract(
            address=pancakeswap_router_address,
            abi=contract_abi
        )

    def get_native_balance(self, address: str) -> int:
        """ Retorna o saldo nativo (BNB) em WEI para o endereço especificado. """
        balance = self.web3.eth.get_balance(address)
        logger.info(f"[SALDO] BNB de {address}: {self.web3.from_wei(balance, 'ether')} BNB")
        return balance

    def get_token_contract(self, token_address: str) -> Contract:
        """ Retorna um objeto Contract para o token (ERC20/BEP20) informado. """
        return self.web3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=ENV_SETTINGS.TOKEN_WBNB_ABI
        )

    def get_token_balance(self, token_address: str, owner_address: str) -> int:
        """ Retorna o saldo de um token (ERC20/BEP20) em WEI para o endereço especificado. """
        token_contract = self.get_token_contract(token_address)
        balance = token_contract.functions.balanceOf(owner_address).call()
        logger.info(f"[SALDO] Token {token_address} para {owner_address}: {balance} WEI")
        return balance

    def get_allowance(self, token_address: str, owner_address: str) -> int:
        """ Retorna quanto de `token_address` está aprovado para uso pelo Router. """
        token_contract = self.get_token_contract(token_address)
        allowance = token_contract.functions.allowance(
            owner_address, ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS
        ).call()
        logger.info(f"[ALLOWANCE] Token {token_address} para o Router: {allowance} WEI")
        return allowance

    def get_best_gas_price(self) -> int:
        """ Obtém o melhor gas price disponível. """
        try:
            suggested_gas_price = self.web3.eth.gas_price
            best_gas_price = int(suggested_gas_price * 1.1)  # 10% de margem p/ prioridade
            logger.info(
                f"[GAS] Sugerido: {self.web3.from_wei(suggested_gas_price, 'gwei')} Gwei | "
                f"Ajustado: {self.web3.from_wei(best_gas_price, 'gwei')} Gwei"
            )
            return best_gas_price
        except Exception as e:
            logger.warning(f"[GAS] Erro ao obter gas price, usando padrão: {e}")
            return Web3.to_wei('5', 'gwei')

    def estimate_gas_for_swap(self, transaction_params: Dict[str, Any]) -> int:
        """ Estima o consumo de gás para a transação. """
        try:
            estimated_gas = self.web3.eth.estimate_gas(transaction_params)
            adjusted_gas = int(estimated_gas * 1.1)  # 10% de margem de segurança
            logger.info(f"[GAS] Estimado: {estimated_gas} | Ajustado: {adjusted_gas}")
            return adjusted_gas
        except Exception as e:
            # Tenta extrair motivo do revert reason e string em hexa
            if len(e.args) > 0:
                reason_str = e.args[0]
            else:
                reason_str = "Sem informação adicional."

            if len(e.args) > 1:
                reason_hex = e.args[1]
            else:
                reason_hex = "Sem informação em hex."

            logger.warning(
                "[GAS] Falha na estimativa de gas, usando valor padrão.\n"
                f"        Motivo: {reason_str}\n"
                f"        Hex: {reason_hex}"
            )
            return 500000

    def approve_token_if_necessary(
        self,
        token_address: str,
        amount_in_wei: int,
        private_key: str,
        chain_id: int
    ) -> Optional[HexBytes]:
        """ Verifica e aprova o token para o Router, se necessário. """
        account = self.web3.eth.account.from_key(private_key)
        owner_address = account.address
        current_allowance = self.get_allowance(token_address, owner_address)

        if current_allowance < amount_in_wei:
            logger.info(f"[APPROVE] Necessário aprovar {amount_in_wei} WEI para o Router.")

            token_contract = self.get_token_contract(token_address)
            nonce = self.web3.eth.get_transaction_count(owner_address)
            gas_price = self.get_best_gas_price()

            approve_tx = token_contract.functions.approve(
                ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS, amount_in_wei
            ).build_transaction({
                'chainId': chain_id,
                'gas': 50000,
                'gasPrice': gas_price,
                'nonce': nonce
            })
            signed_approve_tx = account.sign_transaction(approve_tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_approve_tx.raw_transaction)
            logger.info(f"[APPROVE] Transação de aprovação enviada: {tx_hash.hex()}")
            self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            return tx_hash

        return None

    def swap_exact_tokens_for_tokens_com_checks(
        self,
        private_key: str,
        amount_in_wei: int,
        amount_out_min: int,
        path: List[str],
        to: str,
        deadline: int,
        chain_id: int
    ) -> Dict[str, Any]:
        """
        Método que executa o swap de ponta a ponta:
          - Checa saldo nativo e saldo de token
          - Faz approve (se necessário)
          - Estima gas price e gas limit
          - Constrói, assina e envia a transação
        """

        account = self.web3.eth.account.from_key(private_key)
        owner_address = account.address
        nonce = self.web3.eth.get_transaction_count(owner_address)

        balance_native = self.get_native_balance(owner_address)
        gas_price = self.get_best_gas_price()

        token_in = path[0]
        token_balance = self.get_token_balance(token_in, owner_address)
        if token_balance < amount_in_wei:
            raise ValueError(f"[ERRO] Saldo insuficiente de {token_in}. Necessário: {amount_in_wei}, Saldo: {token_balance}")

        approve_tx_hash = self.approve_token_if_necessary(
            token_address=token_in,
            amount_in_wei=amount_in_wei,
            private_key=private_key,
            chain_id=chain_id
        )
        if approve_tx_hash:
            nonce += 1

        transaction = self.contract.functions.swapExactTokensForTokens(
            amount_in_wei, amount_out_min, path, to, deadline
        ).build_transaction({
            'chainId': chain_id,
            'gas': 500000,
            'gasPrice': gas_price,
            'nonce': nonce
        })

        transaction['gas'] = self.estimate_gas_for_swap(transaction)

        gas_cost = transaction['gas'] * gas_price
        total_cost = amount_in_wei + gas_cost

        if balance_native < total_cost:
            raise ValueError(f"[ERRO] Saldo BNB insuficiente: necessário {total_cost}, disponível {balance_native}")

        signed_tx: SignedTransaction = account.sign_transaction(transaction)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logger.info(f"[TX] Enviada. Hash: {tx_hash.hex()}")

        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if tx_receipt.status != 1:
            raise ValueError(f"[ERRO] Transação de swap falhou: {tx_hash.hex()}")

        logger.info(f"[TX] Concluída com sucesso: {tx_receipt.transactionHash.hex()}")
        return tx_receipt
