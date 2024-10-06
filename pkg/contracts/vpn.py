from web3 import AsyncWeb3, Web3

from internal import model


class ContractVPN(model.IContractVPN):
    def __init__(
            self,
            contract_address: str,
            contract_abi: list | str,
            owner_address: str,
            owner_private_key: str,
    ):
        self.w3 = Web3(Web3.HTTPProvider('https://rpc.cardona.zkevm-rpc.com'))
        self.checksum_address = Web3.to_checksum_address(contract_address)
        self.contract = self.w3.eth.contract(self.checksum_address, abi=contract_abi)
        self.owner_address = owner_address
        self.owner_private_key = owner_private_key

    def _send_transaction(self, function):
        gas_estimate = function.estimate_gas({'from': self.owner_address})
        gas_price = self.w3.eth.gas_price
        transaction = function.build_transaction({
            'from': self.owner_address,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': self.w3.eth.get_transaction_count(Web3.to_checksum_address(self.owner_address))
        })
        signed_tx = self.w3.eth.account.sign_transaction(transaction, self.owner_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def cost_for_set_node_ip(self, node_ip: str) -> int:
        function = self.contract.functions.setNodeIP(node_ip)
        gas_estimate = function.estimate_gas({'from': self.owner_address})
        gas_price = self.w3.eth.gas_price
        transaction_cost = gas_estimate * gas_price
        return transaction_cost

    def owner_balance(self) -> int:
        return self.w3.eth.get_balance(Web3.to_checksum_address(self.owner_address))

    def all_node(self) -> list[str]:
        return self.contract.functions.getAllNode().call()

    def set_node_ip(self, node_ip: str):
        function = self.contract.functions.setNodeIP(node_ip)
        tx_receipt = self._send_transaction(function)
        return tx_receipt

    def client_balance(self, client_address: str):
        client_address = Web3.to_checksum_address(client_address)
        return self.contract.functions.getClientBalance(client_address).call()
