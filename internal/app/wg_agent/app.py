import time
import requests

from internal import model


async def NewWgAgent(
        node_service: model.INodeService
):
    while True:
        wg_package_losses = []
        wg_pings = []
        wg_download_speeds = []
        wg_upload_speeds = []

        nodes_ip = await node_service.nodes_ip()
        for node_ip in nodes_ip:
            node_service.download_wg_config(node_ip)

            node_service.connect_to_wg()

            wg_package_loss, wg_avg_ping = node_service.check_ping(node_ip)
            wg_package_losses.append(int(wg_package_loss * 100))
            wg_pings.append(int(wg_avg_ping * 100))

            wg_download_speed, wg_upload_speed = node_service.check_speed()
            wg_download_speeds.append(int(wg_download_speed * 100))
            wg_upload_speeds.append(int(wg_upload_speed * 100))

            node_service.disconnect_from_wg()

        await node_service.update_node_wg_metrics(
            nodes_ip,
            wg_package_losses,
            wg_pings,
            wg_download_speeds,
            wg_upload_speeds,
        )
        time.sleep(20)
