import time

from internal import model


async def NewTxAgent(
        tx_service: model.ITxService,
        vpn_contract_address: str,
        db: model.DBInterface
):
    await db.multi_query(model.drop_queries)
    await db.multi_query(model.create_queries)
    last_processed_block = await tx_service.set_last_processed_block()

    while True:
        current_block = await tx_service.current_block()
        print("Текущий блок: ", current_block, flush=True)
        last_processed_block = await tx_service.last_processed_block()
        print("Текущий блок: ", current_block, flush=True)
        txs = await tx_service.nds_txs(last_processed_block, current_block, vpn_contract_address)
        await tx_service.update_last_processed_block(current_block)

        for tx in txs:
            client_address, tx_hash, tx_block, amount = await tx_service.parse_tx(tx)

            is_tx_processed = await tx_service.is_tx_processed(client_address, tx_hash, tx_block)
            if is_tx_processed:
                continue

            await tx_service.update_client_balance(client_address, amount, tx_block)
            await tx_service.set_tx(client_address, tx_hash, tx_block)
        time.sleep(10)
