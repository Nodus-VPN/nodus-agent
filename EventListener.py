import os
import time
from web3 import Web3
import json
from dotenv import load_dotenv
load_dotenv()


# =============================== Web3 переменные
w3 = Web3(Web3.HTTPProvider("https://rpc.cardona.zkevm-rpc.com"))

admin_sender_address = Web3.to_checksum_address(os.getenv('ADMIN_WALLET_ADDRESS'))
admin_private_key = os.getenv('ADMIN_PRIVATE_KEY')

with open('abi/nds.json', 'r') as token_abi_file:
    token_abi = json.load(token_abi_file)
token_contract_address = Web3.to_checksum_address("0xcFC65cc3584456d8a7E541d8A18981E9C2889DC2")
token_contract = w3.eth.contract(address=token_contract_address, abi=token_abi)

with open('abi/vpn.json', 'r') as vpn_abi_file:
    vpn_abi = json.load(vpn_abi_file)
vpn_contract_address = Web3.to_checksum_address("0x21897F4cf796E0ea2109C428E86F84c4F2aa38e4")
vpn_contract = w3.eth.contract(address=vpn_contract_address, abi=vpn_abi)


# =============================== Ручной запрос событий
PROCESSED_TX_FILE = 'logs/processed_transactions.json'

# Инициализация файла при первом запуске
if not os.path.exists(PROCESSED_TX_FILE):
    with open(PROCESSED_TX_FILE, 'w') as f:
        json.dump({'transactions': [], 'last_processed_block': w3.eth.block_number}, f)

# Загрузка обработанных транзакций из файла
with open(PROCESSED_TX_FILE, 'r') as f:
    data = json.load(f)
    processed_transactions = data.get('transactions', [])
    last_processed_block = data.get('last_processed_block', w3.eth.block_number)


# Функция для сохранения обработанных транзакций и последнего блока
def save_processed_data():
    with open(PROCESSED_TX_FILE, 'w') as f:
        json.dump({
            'transactions': processed_transactions,
            'last_processed_block': last_processed_block
        }, f, indent=4)


# Функция для проверки, был ли уже обработана транзакция
def is_transaction_processed(user_address, tx_hash, tx_block):
    for record in processed_transactions:
        if (record['address'] == user_address
                and record['last_tx_hash'] == tx_hash
                and record['last_tx_block'] >= tx_block):
            return True
    return False


# Функция для обновления данных о последней транзакции
def update_last_transaction(user_address, tx_hash, tx_block):
    for record in processed_transactions:
        if record['address'] == user_address:
            record['last_tx_hash'] = tx_hash
            record['last_tx_block'] = tx_block
            break
    else:
        processed_transactions.append({
            'address': user_address,
            'last_tx_hash': tx_hash,
            'last_tx_block': tx_block
        })
    # Сохраняем обновленные данные
    save_processed_data()


# =============================== Отправка транзакции
def send_transaction(user_address, amount, block_number):

    # Nonce - количество транзакций от отправителя (для уникальности транзакции)
    nonce = w3.eth.get_transaction_count(admin_sender_address)

    gas_limit = vpn_contract.functions.topUpBalance(user_address, amount, block_number).estimate_gas({'from': admin_sender_address})
    gas_price = w3.eth.gas_price

    # Подготовка транзакции для вызова функции контракта
    transaction = vpn_contract.functions.topUpBalance(user_address, amount, block_number).build_transaction({
        'chainId': 2442,
        'gas': gas_limit,  # Лимит газа
        'gasPrice': gas_price,  # Цена газа
        'nonce': nonce,  # Nonce отправителя
        'from': admin_sender_address  # Адрес отправителя
    })

    # Подписание транзакции с помощью приватного ключа
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=admin_private_key)

    # Отправка подписанной транзакции в блокчейн
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # Получение хэша транзакции
    print(f'Транзакция отправляется: {txn_hash.hex()}')

    # Ожидание подтверждения транзакции
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print(f'Успешно! Данные транзакции: {txn_receipt}')


# Функция для проверки новых транзакций
def check_transactions():
    global last_processed_block
    while True:
        print("Поиск новых транзакций...")
        current_block = w3.eth.block_number

        # Получение и фильтрация событий Transfer по адресу VPN контракта
        manual_request_logs = []
        try:
            manual_request_logs = token_contract.events.Transfer().get_logs(
                from_block=last_processed_block + 1,
                to_block=current_block,
                argument_filters={'to': vpn_contract_address}
            )
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
            print(f"Перевод {w3.from_wei(log['args']['value'], 'ether')} NDS от {log['args']['from']} для {log['args']['to']}. Tx hash: {tx_hash} Block: {tx_block}")

            try:
                send_transaction(user_address, amount, tx_block)  # Отправляем в блокчейн
            except Exception as e:
                print(f"Произошла ошибка при отправке транзакции: {e}")

            # Обновляем хэш последней транзакции для этого адреса
            update_last_transaction(user_address, tx_hash, tx_block)
        # Задержка в 10 секунд перед следующей проверкой
        time.sleep(10)


if __name__ == '__main__':
    check_transactions()
