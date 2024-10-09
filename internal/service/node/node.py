import subprocess
import time

import speedtest
from ping3 import ping

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

    def connect_to_vpn(self, config_path: str):
        subprocess.run(["sudo", "wg-quick", "up", config_path], check=True)

    def disconnect_from_vpn(self, config_path: str):
        subprocess.run(["sudo", "wg-quick", "down", config_path], check=True)

    def check_speed(self) -> tuple[float, float]:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000  # В Мбит/с
        upload_speed = st.upload() / 1_000_000  # В Мбит/с
        return download_speed, upload_speed

    def check_ping(self, host) -> tuple[float, float]:
        lost_packets = 0
        response_times = []
        count = 50

        for _ in range(count):
            response_time = ping(host, timeout=1)
            if response_time is None:
                lost_packets += 1
            else:
                response_times.append(response_time * 1000)

        packet_loss = (lost_packets / count) * 100
        avg_ping = sum(response_times) / len(response_times) if response_times else 0

        return packet_loss, float(avg_ping)

    async def update_node_metrics(
            self,
            nodes_ip: list[str],
            ok_responses: list[int],
            failed_responses: list[int],
            package_losses: list[int],
            pings: list[int],
            download_speeds: list[int],
            upload_speeds: list[int]
    ):
        await self.vpn_contract.update_node_metrics(
            nodes_ip,
            ok_responses,
            failed_responses,
            package_losses,
            pings,
            download_speeds,
            upload_speeds,
        )
