from internal import model


class TxService(model.ITxService):
    def __init__(
            self,
            tx_repo: model.ITxRepository,
            vpn_contract: model.IContractVPN,
            nds_contract: model.IContractNDS,
    ):
        self.tx_repo = tx_repo
        self.vpn_contract = vpn_contract
        self.nds_contract = nds_contract

    # INSERT
    async def set_tx(self, client_address: str, tx_hash: str, tx_block: int):
        await self.tx_repo.set_tx(client_address, tx_hash, tx_block)

    async def set_last_processed_block(self) -> int:
        current_block = await self.nds_contract.current_block()
        await self.tx_repo.set_last_processed_block(current_block)
        return current_block

    # UPDATE
    async def update_last_processed_block(self, last_processed_block: int) -> None:
        await self.tx_repo.update_last_processed_block(last_processed_block)

    async def update_client_balance(self, client_address: str, amount: int, tx_block: int) -> None:
        await self.vpn_contract.update_client_balance(client_address, amount, tx_block)

    # GET
    async def last_processed_block(self) -> int:
        return await self.tx_repo.last_processed_block()

    async def nds_txs(self, last_processed_block: int, current_block: int, vpn_contract_address: str) -> list:
        return self.nds_contract.txs(last_processed_block, current_block, vpn_contract_address)

    # OTHER
    async def is_tx_processed(self, client_address: str, tx_hash: str, tx_block: int) -> bool:
        txs = await self.tx_repo.all_tx()
        for tx in txs:
            if (tx.client_address == client_address
                    and tx.tx_hash == tx_hash
                    and tx.tx_block >= tx_block):
                return True
        return False

    async def parse_tx(self, tx: dict) -> tuple[str, str, int, int]:
        tx_hash = tx['transactionHash'].hex()
        client_address = tx['args']['from']
        tx_block = tx['blockNumber']
        amount = tx['args']['value']
        return client_address, tx_hash, tx_block, amount
