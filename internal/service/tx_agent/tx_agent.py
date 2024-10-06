from internal import model


class TxAgentService(model.ITxAgentService):
    def __init__(self, tx_agent_repo: model.ITxAgentRepository):
        self._tx_agent_repo = tx_agent_repo

    async def last_processed_block(self) -> int:
        return await self._tx_agent_repo.last_processed_block()

    async def update_last_processed_block(self, last_processed_block: int) -> None:
        await self._tx_agent_repo.update_last_processed_block(last_processed_block)

    async def set_last_processed_block(self, last_processed_block: int) -> int:
        await self._tx_agent_repo.set_last_processed_block(last_processed_block)
        return last_processed_block
