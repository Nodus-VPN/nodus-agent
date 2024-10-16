import time

from internal import model

expired_subscriptions = {}


async def NewSubscriptionAgent(
        client_service: model.IClientService,
        node_service: model.INodeService,
):
    while True:
        nodes_ip = await node_service.nodes_ip()
        all_client_address = await client_service.all_client_address()

        for client_address in all_client_address:
            client = await client_service.get_client(client_address)

            # Клиент был помечен, но продлил подписку
            if (expired_subscriptions.get(client_address) is not None
                    and client.subscription_expiration_date > int(time.time())):
                del expired_subscriptions[client_address]
                continue

            if client.subscription_expiration_date < int(time.time()):
                # Клиент помечен, его конфиги уже удалены
                if expired_subscriptions.get(client_address):
                    continue

                for node_ip in nodes_ip:
                    await node_service.delete_client_config(node_ip, client_address)

                # Помечаем, что конфиги со всех серверов удалены
                print("Истекла подписка ", client_address)
                expired_subscriptions[client_address] = client.subscription_expiration_date
        print("Проверили подписки")
        time.sleep(5)
