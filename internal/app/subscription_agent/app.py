import time
import logging

from internal import model

expired_subscriptions = {}


async def NewSubscriptionAgent(
        client_service: model.IClientService,
        node_service: model.INodeService,
        logger: logging.Logger,
):
    logger.info("New subscription agent")
    while True:
        nodes_ip = await node_service.nodes_ip()
        all_client_address = await client_service.all_client_address()

        for client_address in all_client_address:
            logger.info(f"Check {client_address}")
            client = await client_service.get_client(client_address)

            # Клиент был помечен, но продлил подписку
            if (expired_subscriptions.get(client_address) is not None
                    and client.subscription_expiration_date > int(time.time())):
                del expired_subscriptions[client_address]
                logger.info(f"{client_address} renew subscription")
                continue

            if client.subscription_expiration_date < int(time.time()):
                # Клиент помечен, его конфиги уже удалены
                if expired_subscriptions.get(client_address):
                    logger.info(f"{client_address} already checked")
                    continue

                for node_ip in nodes_ip:
                    await node_service.delete_client_config(node_ip, client_address)

                # Помечаем, что конфиги со всех серверов удалены
                expired_subscriptions[client_address] = client.subscription_expiration_date
                logger.info(f"{client_address} delete all config")

        logger.info("All client checked. W8")
        time.sleep(60)
