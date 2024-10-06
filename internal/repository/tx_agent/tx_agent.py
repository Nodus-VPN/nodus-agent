from internal import model


class TxAgentRepository(model.ITxAgentRepository):

    def __init__(self, db: model.DBInterface):
        self.db = db

    async def last_processed_block(self) -> int:
        rows = await self.db.select(model.get_last_processed_block_query, {})
        return rows[0].last_processed_block

    async def set_last_processed_block(self, last_processed_block: int) -> None:
        query_params = {"last_processed_block": last_processed_block}
        await self.db.insert(model.set_last_processed_block_query, query_params)

    async def update_last_processed_block(self, last_processed_block: int) -> None:
        query_params = {"last_processed_block": last_processed_block}
        await self.db.update(model.update_last_processed_block_query, query_params)