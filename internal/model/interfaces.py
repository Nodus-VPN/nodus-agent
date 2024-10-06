from abc import abstractmethod
from typing import Protocol, Any, Sequence
from internal import model


class ITxService(Protocol):
    # INSERT
    @abstractmethod
    async def set_last_processed_block(self, last_processed_block: int) -> int: pass

    @abstractmethod
    async def set_tx(self, client_address: str, tx_hash: str, tx_block: int): pass

    # UPDATE
    @abstractmethod
    async def update_last_processed_block(self, last_processed_block: int) -> None: pass

    @abstractmethod
    async def update_client_balance(self, client_address: str, amount: int, tx_block: int) -> None: pass

    # SELECT
    @abstractmethod
    async def last_processed_block(self) -> int: pass

    # OTHER
    @abstractmethod
    async def is_tx_processed(self, client_address: str, tx_hash: str, tx_block: int) -> bool: pass

    @abstractmethod
    async def parse_tx(self, tx: dict) -> tuple[str, str, int, int]: pass


class ITxRepository(Protocol):
    @abstractmethod
    async def set_last_processed_block(self, last_processed_block: int) -> None: pass

    @abstractmethod
    async def update_last_processed_block(self, last_processed_block: int) -> None: pass

    @abstractmethod
    async def last_processed_block(self) -> int: pass

    @abstractmethod
    async def set_tx(self, client_address: str, tx_hash: str, tx_block: int): pass

    @abstractmethod
    async def all_tx(self) -> list[model.Tx]: pass


class IContractNDS(Protocol):
    @abstractmethod
    def txs(
            self,
            last_processed_block: int,
            current_block: int,
            vpn_contract_address: str
    ) -> list: pass

    @abstractmethod
    def current_block(self) -> int: pass


class IContractVPN(Protocol):
    @abstractmethod
    def update_client_balance(self, client_address: str, amount: int, tx_block: int): pass


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
