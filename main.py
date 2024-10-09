import asyncio
from pkg.api.node import NodeClient

from pkg.contracts import ContractVPN

from internal.app.metrics_agent.app import NewMetricsAgent
from internal.app.subscription_agent.app import NewSubscriptionAgent

from internal.service.node.node import NodeService
from internal.service.client.client import ClientService

from internal.config.config import Config as cfg
import argparse

parser = argparse.ArgumentParser(description='For choice app')
parser.add_argument(
    'app',
    type=str,
    help='Option: "metrics_agent, subscription_agent"'
)

vpn_contract = ContractVPN(
    owner_address=cfg.owner_address,
    owner_private_key=cfg.owner_private_key,
    contract_abi=cfg.vpn_contract_abi,
    contract_address=cfg.vpn_contract_address
)

node_client = NodeClient(cfg.node_metric_port)
node_service = NodeService(vpn_contract, node_client)

client_service = ClientService(vpn_contract)

if __name__ == '__main__':
    args = parser.parse_args()

    if args.app == "metrics_agent":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(NewMetricsAgent(node_service))

    if args.app == "subscription_agent":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(NewSubscriptionAgent(client_service, node_service))
