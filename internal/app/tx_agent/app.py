from internal import model


async def NewTxAgent(
        nds_contract: model.IContractNDS,
        tx_service: model.ITxAgentService
):
    last_processed_block = await tx_service.set_last_processed_block(nds_contract.current_block())

    while True:
        current_block = nds_contract.current_block()

        # Получение и фильтрация событий Transfer по адресу VPN контракта
        manual_request_logs = []
        try:
            nds_contract.tx_logs(last_processed_block, current_block, vpn_contract_address)
            last_processed_block = current_block
            save_processed_data()  # Сохраняем после каждой проверки блоков
        except Exception as e:
            print(f"Произошла ошибка при запросе событий: {e}")

        # Обработка данных
        for log in manual_request_logs:
            tx_hash = log['transactionHash'].hex()  # Хэш транзакции
            user_address = log['args']['from']  # Адрес отправителя
            tx_block = log['blockNumber']
            amount = log['args']['value']

            # Проверяем, не была ли эта транзакция уже обработана
            if is_transaction_processed(user_address, tx_hash, tx_block):
                print(f"Транзакция {tx_hash} в блоке {tx_block} для адреса {user_address} уже обработана, пропускаю...")
                continue  # Пропускаем уже обработанную транзакцию

            # Если транзакция не была обработана, выполняем дальнейшие действия
            print(
                f"Перевод {w3.from_wei(log['args']['value'], 'ether')} NDS от {log['args']['from']} для {log['args']['to']}. Tx hash: {tx_hash} Block: {tx_block}")

            try:
                send_transaction(user_address, amount, tx_block)  # Отправляем в блокчейн
            except Exception as e:
                print(f"Произошла ошибка при отправке транзакции: {e}")

            # Обновляем хэш последней транзакции для этого адреса
            update_last_transaction(user_address, tx_hash, tx_block)
        # Задержка в 10 секунд перед следующей проверкой
        time.sleep(10)
