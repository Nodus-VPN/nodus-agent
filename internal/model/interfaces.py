from abc import abstractmethod
from typing import Protocol, Any, Sequence


class INodeService(Protocol):
    # INSERT
    @abstractmethod
    async def nodes_ip(self) -> list[str]: pass

    @abstractmethod
    async def health_check(self, node_ip: str) -> int: pass

    @abstractmethod
    async def update_node_metrics(
            self,
            nodes_ip: list[str],
            ok_responses: list[int],
            failed_responses: list[int],
            traffics: list[int]
    ): pass


class IContractVPN(Protocol):
    @abstractmethod
    async def nodes_ip(self) -> list[str]: pass

    @abstractmethod
    async def update_node_metrics(
            self,
            nodes_ip: list[str],
            ok_response: list[int],
            failed_response: list[int],
            traffic: list[int]
    ): pass


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


class INodeClient(Protocol):
    @abstractmethod
    async def health_check(self, node_ip: str): pass
