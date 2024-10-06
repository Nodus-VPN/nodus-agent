from abc import abstractmethod
from typing import Protocol, Any, Sequence


class ITxAgentService(Protocol):
    @abstractmethod
    async def set_last_processed_block(self, last_processed_block: int) -> int: pass

    @abstractmethod
    async def update_last_processed_block(self, last_processed_block: int) -> None: pass

    @abstractmethod
    async def last_processed_block(self) -> int: pass


class ITxAgentRepository(Protocol):
    @abstractmethod
    async def set_last_processed_block(self, last_processed_block: int) -> None: pass

    @abstractmethod
    async def update_last_processed_block(self, last_processed_block: int) -> None: pass

    @abstractmethod
    async def last_processed_block(self) -> int: pass


class IContractNDS(Protocol):
    @abstractmethod
    def tx_logs(
            self,
            last_processed_block: int,
            current_block: int,
            vpn_contract_address: str
    ) -> list: pass

    @abstractmethod
    def current_block(self) -> int: pass


class DBInterface(Protocol):
    @abstractmethod
    async def insert(self, query: str, query_params: dict) -> int: pass

    @abstractmethod
    async def delete(self, query: str, query_params: dict) -> None: pass

    @abstractmethod
    async def update(self, query: str, query_params: dict) -> None: pass

    @abstractmethod
    async def select(self, query: str, query_params: dict) -> Sequence[Any]: pass

    @abstractmethod
    async def multi_query(self, queries: list[str]) -> None: pass
