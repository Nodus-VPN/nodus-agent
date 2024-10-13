import time
import requests

from internal import model


async def NewOVPNAgent(
        node_service: model.INodeService
):
    while True:
        ovpn_package_losses = []
        ovpn_pings = []
        ovpn_download_speeds = []
        ovpn_upload_speeds = []

        nodes_ip = await node_service.nodes_ip()
        for node_ip in nodes_ip:
            node_service.download_ovpn_config(node_ip)

            node_service.connect_to_ovpn()

            ovpn_package_loss, ovpn_avg_ping = node_service.check_ping(node_ip)
            ovpn_package_losses.append(int(ovpn_package_loss * 100))
            ovpn_pings.append(int(ovpn_avg_ping * 100))

            ovpn_download_speed, ovpn_upload_speed = node_service.check_speed()
            ovpn_download_speeds.append(int(ovpn_download_speed * 100))
            ovpn_upload_speeds.append(int(ovpn_upload_speed * 100))

            node_service.disconnect_from_ovpn()

        await node_service.update_node_ovpn_metrics(
            nodes_ip,
            ovpn_package_losses,
            ovpn_pings,
            ovpn_download_speeds,
            ovpn_upload_speeds,
        )
        time.sleep(20)
