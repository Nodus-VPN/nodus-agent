from web3 import AsyncWeb3

from internal import model


class ContractNDS(model.IContractNDS):
    def __init__(
            self,
            contract_address: str,
            contract_abi: str,
    ):
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider('https://rpc.cardona.zkevm-rpc.com'))
        self.checksum_address = AsyncWeb3.to_checksum_address(contract_address)
        self.contract = self.w3.eth.contract(self.checksum_address, abi=contract_abi)

    async def txs(
            self,
            last_processed_block: int,
            current_block: int,
            vpn_contract_address: str
    ) -> list:
        logs = await self.contract.events.Transfer().get_logs(
            from_block=last_processed_block + 1,
            to_block=current_block + 1,
            argument_filters={'to': vpn_contract_address}
        )
        return logs

    async def current_block(self) -> int:
        return await self.w3.eth.block_number


