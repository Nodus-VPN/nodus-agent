import subprocess
import requests

import speedtest
from ping3 import ping

from internal import model


class NodeService(model.INodeService):
    wg_config_path = "/etc/wireguard/wg3.conf"

    def __init__(
            self,
            vpn_contract: model.IContractVPN,
            node_client: model.INodeClient,
            admin_address: str,
    ):
        self.vpn_contract = vpn_contract
        self.node_client = node_client
        self.admin_address = admin_address

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

    async def delete_client_config(self, node_ip: str, client_address: str) -> None:
        await self.node_client.delete_client_config(node_ip, client_address)

    async def update_node_status(self, nodes_ip: list[str], status: str):
        await self.vpn_contract.update_node_status(nodes_ip, status)

    async def update_node_uptime(self, nodes_ip: list[str], ok_responses: list[int], failed_responses: list[int]):
        await self.vpn_contract.update_node_uptime(nodes_ip, ok_responses, failed_responses)

    async def update_node_metrics(
            self,
            nodes_ip: list[str],
            package_losses: list[int],
            pings: list[int],
            download_speeds: list[int],
            upload_speeds: list[int]
    ):
        await self.vpn_contract.update_node_metrics(
            nodes_ip,
            package_losses,
            pings,
            download_speeds,
            upload_speeds,
        )

    async def delete_node(self, nodes_ip: list[str]) -> None:
        await self.vpn_contract.delete_node(nodes_ip)

    # WG
    def download_vpn_config(self, node_ip: str):
        config_url = f"http://{node_ip}:7000/config/wg/{self.admin_address}"

        response = requests.get(config_url, json={"client_secret_key": "admin"})
        with open(self.wg_config_path, "wb") as file:
            file.write(response.content)

    def connect_to_vpn(self):
        subprocess.run(["sudo", "wg-quick", "up", "wg3"], check=True)

    def disconnect_vpn(self):
        subprocess.run(["sudo", "wg-quick", "down", "wg3"], check=True)
