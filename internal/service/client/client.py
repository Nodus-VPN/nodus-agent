from internal import model


class ClientService(model.IClientService):
    def __init__(self, vpn_contract: model.IContractVPN):
        self._vpn_contract = vpn_contract

    async def all_client_address(self) -> list[str]:
        return await self._vpn_contract.all_client_address()

    async def get_client(self, client_address: str) -> model.Client:
        return await self._vpn_contract.get_client(client_address)
