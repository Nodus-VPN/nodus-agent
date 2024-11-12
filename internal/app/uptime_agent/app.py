import time
from datetime import datetime, timedelta
import logging

from internal import model

inactive_nodes: dict[str, datetime] = {}


async def NewUptimeAgent(
        node_service: model.INodeService,
        logger: logging.Logger,
):
    logger.info('New uptime agent started')
    while True:
        ok_responses = []
        failed_responses = []

        new_active_nodes = []
        new_inactive_nodes = []
        new_deleted_nodes = []

        nodes_ip = await node_service.nodes_ip()
        for node_ip in nodes_ip:
            logger.info(f'start checking uptime {node_ip}')

            health = await node_service.health_check(node_ip)
            if health:

                if inactive_nodes.get(node_ip):
                    del inactive_nodes[node_ip]
                    new_inactive_nodes.append(node_ip)

                ok_responses.append(1)
                failed_responses.append(0)
            else:
                ok_responses.append(0)
                failed_responses.append(1)

                if inactive_nodes.get(node_ip) is None:
                    inactive_nodes[node_ip] = datetime.now() + timedelta(days=2)
                    new_inactive_nodes.append(node_ip)
                else:
                    if datetime.now() < inactive_nodes.get(node_ip):
                        new_deleted_nodes.append(new_active_nodes)

            logger.info(f"end checking uptime {node_ip}")

        await node_service.update_node_uptime(
            nodes_ip,
            ok_responses,
            failed_responses,
        )
        if new_inactive_nodes:
            await node_service.update_node_status(new_active_nodes, "inactive")

        if new_active_nodes:
            await node_service.update_node_status(new_active_nodes, "active")

        if new_deleted_nodes:
            await node_service.delete_node(nodes_ip)

        logger.info('Node uptime updated')

        time.sleep(60)