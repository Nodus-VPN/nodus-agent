import time
import logging as logger

from internal import model


async def NewUptimeAgent(
        node_service: model.INodeService
):
    logger.info('New uptime agent started')
    while True:
        ok_responses = []
        failed_responses = []

        nodes_ip = await node_service.nodes_ip()
        for node_ip in nodes_ip:
            logger.info(f'start checking uptime {node_ip}')
            health = await node_service.health_check(node_ip)
            if health:
                ok_responses.append(1)
                failed_responses.append(0)
            else:
                ok_responses.append(0)
                failed_responses.append(1)
            logger.info(f"end checking uptime {node_ip}")
        await node_service.update_node_uptime(
            nodes_ip,
            ok_responses,
            failed_responses,
        )
        logger.info('Node uptime updated')
        time.sleep(20)
