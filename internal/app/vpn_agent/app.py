import time
import logging

from internal import model


async def NewVPNAgent(
        node_service: model.INodeService,
        logger: logging.Logger,
):
    logger.info("VPN agent started")
    while True:
        try:
            wg_package_losses = []
            wg_pings = []
            wg_download_speeds = []
            wg_upload_speeds = []

            nodes_ip = await node_service.nodes_ip()
            for node_ip in nodes_ip:
                try:
                    logger.info(f"Start check metrics {node_ip}")
                    node_service.download_vpn_config(node_ip)

                    node_service.connect_to_vpn()

                    wg_package_loss, wg_avg_ping = node_service.check_ping(node_ip)
                    wg_package_losses.append(int(wg_package_loss * 100))
                    wg_pings.append(int(wg_avg_ping * 100))

                    wg_download_speed, wg_upload_speed = node_service.check_speed()
                    wg_download_speeds.append(int(wg_download_speed * 100))
                    wg_upload_speeds.append(int(wg_upload_speed * 100))

                    node_service.disconnect_vpn()
                    logger.info(f"End check metrics {node_ip}")
                except Exception as e:
                    node_service.disconnect_vpn()
                    logger.error(e)

            await node_service.update_node_metrics(
                nodes_ip,
                wg_package_losses,
                wg_pings,
                wg_download_speeds,
                wg_upload_speeds,
            )
            logger.info("Node metrics updated")

            time.sleep(60)
        except Exception as e:
            node_service.disconnect_vpn()
            logger.error("Restart VPN agent")
            logger.error(e)
            continue
