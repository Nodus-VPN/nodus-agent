import aiohttp
from internal import model


class NodeClient(model.INodeClient):
    def __init__(
            self,
            node_metric_port,
    ):
        self.node_metric_port = node_metric_port

    async def __async_get(self, path: str, node_ip: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{node_ip}:{self.node_metric_port}{path}") as resp:
                return await resp.json()


    async def __async_delete(self, path: str, node_ip: str):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"http://{node_ip}:{7000}{path}") as resp:
                return await resp.json()

    async def health_check(self, node_ip: str):
        return await self.__async_get("/health", node_ip)

    async def delete_client_config(self, node_ip: str, client_address: str):
        return await self.__async_delete(f"/config/{client_address}", node_ip)
