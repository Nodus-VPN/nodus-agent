import time

from internal import model


async def NewMetricsAgent(
        node_service: model.INodeService
):
    while True:
        ok_responses = []
        failed_responses = []

        nodes_ip = await node_service.nodes_ip()
        for node_ip in nodes_ip:

            # UPTIME
            health = await node_service.health_check(node_ip)
            if health:
                ok_responses.append(1)
                failed_responses.append(0)
            else:
                ok_responses.append(0)
                failed_responses.append(1)


        await node_service.update_node_metrics(
            nodes_ip,
            ok_responses,
            failed_responses,
        )
        time.sleep(20)
