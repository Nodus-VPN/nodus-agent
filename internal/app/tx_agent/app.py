import time

from internal import model


async def NewTxAgent(
        nds_contract: model.IContractNDS,
        tx_service: model.ITxService,
        vpn_contract_address: str,
):
    last_processed_block = await tx_service.set_last_processed_block()

    while True:
        current_block = nds_contract.current_block()
        last_processed_block = await tx_service.last_processed_block()
        txs = nds_contract.txs(last_processed_block, current_block, vpn_contract_address)
        await tx_service.update_last_processed_block(current_block)

        for tx in txs:
            client_address, tx_hash, tx_block, amount = await tx_service.parse_tx(tx)

            is_tx_processed = await tx_service.is_tx_processed(client_address, tx_hash, tx_block)
            if is_tx_processed:
                continue

            await tx_service.update_client_balance(client_address, amount, tx_block)
            await tx_service.set_tx(client_address, tx_hash, tx_block)
        time.sleep(10)