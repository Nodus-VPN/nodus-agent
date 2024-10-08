from internal import model


class NodeService(model.INodeService):
    def __init__(
            self,
            vpn_contract: model.IContractVPN,
            node_client: model.INodeClient,
    ):
        self.vpn_contract = vpn_contract
        self.node_client = node_client

    # INSERT
    async def nodes_ip(self) -> list[str]:
        return await self.vpn_contract.nodes_ip()

    async def health_check(self, node_ip: str) -> int:
        try:
            response = await self.node_client.health_check(node_ip)
            if response["health"]:
                return True
            else:
                return False
        except:
            return False

    async def update_node_metrics(
            self,
            nodes_ip: list[str],
            ok_responses: list[int],
            failed_responses: list[int],
            traffics: list[int]
    ):
        await self.vpn_contract.update_node_metrics(
            nodes_ip,
            ok_responses,
            failed_responses,
            traffics
        )
