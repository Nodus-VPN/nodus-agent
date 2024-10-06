from web3 import AsyncWeb3, Web3

from internal import model


class ContractNDS(model.IContractNDS):
    def __init__(
            self,
            contract_address: str,
            contract_abi: list | str,
    ):
        self.w3 = Web3(Web3.HTTPProvider('https://rpc.cardona.zkevm-rpc.com'))
        self.checksum_address = Web3.to_checksum_address(contract_address)
        self.contract = self.w3.eth.contract(self.checksum_address, abi=contract_abi)

    def txs(
            self,
            last_processed_block: int,
            current_block: int,
            vpn_contract_address: str
    ) -> list:
        logs = self.contract.events.Transfer().get_logs(
            from_block=last_processed_block + 1,
            to_block=current_block,
            argument_filters={'to': vpn_contract_address}
        )
        return logs

    def current_block(self) -> int:
        return self.w3.eth.block_number


