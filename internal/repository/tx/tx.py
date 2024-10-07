from internal import model


class TxRepository(model.ITxRepository):

    def __init__(self, db: model.DBInterface):
        self.db = db

    # INSERT
    async def set_tx(self, client_address: str, tx_hash: str, tx_block: int):
        query_params = {"client_address": client_address, "tx_hash": tx_hash, "tx_block": tx_block}
        await self.db.insert(model.set_tx_query, query_params)

    async def set_last_processed_block(self, last_processed_block: int) -> None:
        query_params = {"last_processed_block": last_processed_block}
        await self.db.insert(model.set_last_processed_block_query, query_params)

    # UPDATE
    async def update_last_processed_block(self, last_processed_block: int) -> None:
        query_params = {"last_processed_block": last_processed_block}
        await self.db.update(model.update_last_processed_block_query, query_params)

    # GET
    async def last_processed_block(self) -> int:
        rows = await self.db.select(model.get_last_processed_block_query, {})
        return rows[0].last_processed_block

    async def all_tx(self) -> list[model.Tx]:
        rows = await self.db.select(model.get_all_tx_query, {})

        if rows:
            rows = model.Tx.serialize(rows)
        return rows
