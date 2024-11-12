import asyncio
import logging

from pkg.api.node import NodeClient

from pkg.contracts import ContractVPN

from internal.app.vpn_agent.app import NewVPNAgent
from internal.app.uptime_agent.app import NewUptimeAgent
from internal.app.subscription_agent.app import NewSubscriptionAgent

from internal.service.node.node import NodeService
from internal.service.client.client import ClientService

from internal.config.config import Config as cfg
import argparse

parser = argparse.ArgumentParser(description='For choice app')
parser.add_argument(
    'app',
    type=str,
    help='Option: "wg_agent, uptime_agent, subscription_agent"'
)

vpn_contract = ContractVPN(
    owner_address=cfg.owner_address,
    owner_private_key=cfg.owner_private_key,
    contract_abi=cfg.vpn_contract_abi,
    contract_address=cfg.vpn_contract_address
)

node_client = NodeClient(cfg.node_metric_port)
node_service = NodeService(vpn_contract, node_client, cfg.admin_address)

client_service = ClientService(vpn_contract)

if __name__ == '__main__':
    args = parser.parse_args()

    import logging
    import sys

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if args.app == "wg_agent":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(NewVPNAgent(node_service, logger))

    if args.app == "uptime_agent":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(NewUptimeAgent(node_service, logger))

    if args.app == "subscription_agent":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(NewSubscriptionAgent(client_service, node_service, logger))
