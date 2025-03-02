import json
import pytest
from unittest.mock import MagicMock
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import Contract
from src.environment import ENV_SETTINGS
from src.repositories.pancakeswap_router_contract_repository import PancakeSwapRouterContractRepository


class TestPancakeSwapRouterContractRepository:

    def setup_method(self):
        """Configuração inicial dos mocks para cada teste"""
        self.pancakeswap_router_address = ENV_SETTINGS.PANCAKESWAP_ROUTER_ADDRESS
        self.pancakeswap_router_abi = ENV_SETTINGS.PANCAKESWAP_ROUTER_ABI

        self.mocked_web3 = MagicMock(spec=Web3)
        self.mocked_eth = MagicMock()
        self.mocked_contract = MagicMock(spec=Contract)

        # Configura o .eth para retornar nosso mock
        self.mocked_web3.eth = self.mocked_eth
        self.mocked_eth.contract.return_value = self.mocked_contract

        # Instancia o repositório com os mocks
        self.repository = PancakeSwapRouterContractRepository(
            web3=self.mocked_web3,
            pancakeswap_router_address=self.pancakeswap_router_address,
            pancakeswap_router_abi=self.pancakeswap_router_abi
        )

    def test_initialization(self):
        """Testa se o contrato do Router é instanciado corretamente."""
        self.mocked_web3.eth.contract.assert_called_once_with(
            address=self.pancakeswap_router_address,
            abi=json.loads(self.pancakeswap_router_abi)
        )

    def test_swap_exact_tokens_for_tokens_com_checks(self):
        """Testa a execução do swap com todas as verificações."""
        private_key = "0xPrivateKey"
        amount_in_wei = 10_000_000_000_000_000  # 0.01 BNB
        amount_out_min = 9_000_000_000_000_000
        path = [
            "0x0000000000000000000000000000000000000001",
            "0x0000000000000000000000000000000000000002"
        ]
        to = "0x0000000000000000000000000000000000000003"
        deadline = 1234567890
        chain_id = 56

        # saldo nativo e saldo de token como int
        self.mocked_web3.eth.get_balance.return_value = 50_000_000_000_000_000  # 0.05 BNB
        self.mocked_contract.functions.balanceOf.return_value.call.return_value = 20_000_000_000_000_000
        self.mocked_contract.functions.allowance.return_value.call.return_value = 10_000_000_000_000_000
        self.mocked_web3.eth.get_transaction_count.return_value = 1

        # Retorno de gas_price como int
        self.mocked_web3.eth.gas_price = 1_000_000_000
        # Se acima não funcionar, tente:
        # self.mocked_web3.eth.gas_price.return_value = 1_000_000_000

        # Retorno de estimate_gas como int
        self.mocked_web3.eth.estimate_gas.return_value = 150_000

        from hexbytes import HexBytes
        expected_tx_hash_str = "0xMockTxHash"
        self.mocked_web3.eth.send_raw_transaction.return_value = HexBytes(expected_tx_hash_str.encode())
        self.mocked_web3.eth.wait_for_transaction_receipt.return_value = MagicMock(status=1)

        tx_receipt = self.repository.swap_exact_tokens_for_tokens_com_checks(
            private_key, amount_in_wei, amount_out_min, path, to, deadline, chain_id
        )

        assert tx_receipt.status == 1


    def test_estimate_gas_for_swap_success(self):
        """Testa a estimativa de gas quando bem-sucedida."""
        transaction_params = {'to': '0xMockAddress'}
        # Retorna 150000 como mock
        self.mocked_web3.eth.estimate_gas.return_value = 150000

        gas_estimate = self.repository.estimate_gas_for_swap(transaction_params)

        # 10% de margem
        assert gas_estimate == int(150000 * 1.1)

    def test_estimate_gas_for_swap_failure(self):
        """Testa a estimativa de gas quando falha e retorna erro formatado."""
        transaction_params = {'to': '0xMockAddress'}
        # Simula falha
        self.mocked_web3.eth.estimate_gas.side_effect = Exception(
            "execution reverted: TransferHelper::transferFrom: transferFrom failed"
        )

        gas_estimate = self.repository.estimate_gas_for_swap(transaction_params)
        assert gas_estimate == 500000  # Valor de fallback

    def test_approve_token_if_necessary_no_approval_needed(self):
        """Testa o caso onde não é necessário aprovar tokens."""
        token_address = "0x0000000000000000000000000000000000000001"
        amount_in_wei = 10_000_000_000_000_000
        private_key = "0xPrivateKey"
        chain_id = 56

        # Já tem allowance maior que amount_in_wei
        self.mocked_contract.functions.allowance.return_value.call.return_value = 20_000_000_000_000_000

        tx_hash = self.repository.approve_token_if_necessary(
            token_address, amount_in_wei, private_key, chain_id
        )

        # Se não for necessário aprovar, tx_hash deve ser None
        assert tx_hash is None

    def test_approve_token_if_necessary_approval_required(self):
        """Testa o caso onde a aprovação é necessária."""
        token_address = "0x0000000000000000000000000000000000000001"
        amount_in_wei = 10_000_000_000_000_000
        private_key = "0xPrivateKey"
        chain_id = 56

        # Mock da allowance menor
        self.mocked_contract.functions.allowance.return_value.call.return_value = 5_000_000_000_000_000
        self.mocked_web3.eth.get_transaction_count.return_value = 10
        # Precisamos retornar HexBytes para usar .hex()
        mock_tx_hash_str = "0xMockTxHash"
        self.mocked_web3.eth.send_raw_transaction.return_value = HexBytes(mock_tx_hash_str_str.encode())

        tx_hash = self.repository.approve_token_if_necessary(
            token_address, amount_in_wei, private_key, chain_id
        )

        # tx_hash será do tipo HexBytes
        assert tx_hash.hex() == mock_tx_hash_str, "Deveria retornar o hex exato da mockada."

