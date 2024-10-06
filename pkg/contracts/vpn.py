from web3 import AsyncWeb3

from internal import model


class ContractVPN(model.IContractVPN):
    def __init__(
            self,
            contract_address: str,
            contract_abi: list | str,
            owner_address: str,
            owner_private_key: str,
    ):
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider('https://rpc.cardona.zkevm-rpc.com'))
        self.checksum_address = AsyncWeb3.to_checksum_address(contract_address)
        self.contract = self.w3.eth.contract(self.checksum_address, abi=contract_abi)
        self.owner_address = owner_address
        self.owner_private_key = owner_private_key

    async def _send_transaction(self, function):
        gas_estimate = await function.estimate_gas({'from': self.owner_address})
        gas_price = await self.w3.eth.gas_price
        transaction = await function.build_transaction({
            'from': self.owner_address,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': self.w3.eth.get_transaction_count(AsyncWeb3.to_checksum_address(self.owner_address))
        })
        signed_tx = self.w3.eth.account.sign_transaction(transaction, self.owner_private_key)
        tx_hash = await self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    async def update_client_balance(self, client_address: str, amount: int, tx_block: int):
        function = self.contract.functions.topUpBalance(client_address, amount, tx_block)
        tx_receipt = await self._send_transaction(function)
