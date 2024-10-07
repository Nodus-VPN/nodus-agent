import asyncio
from infrasctructure.pg.pg import PG

from pkg.contracts import ContractVPN, ContractNDS

from internal.app.tx_agent.app import NewTxAgent

from internal.service.tx.tx import TxService
from internal.repository.tx.tx import TxRepository

from internal.config.config import Config as cfg
import argparse

parser = argparse.ArgumentParser(description='For choice app')
parser.add_argument(
    'app',
    type=str,
    help='Option: "tx_agent"'
)

vpn_contract = ContractVPN(
    owner_address=cfg.owner_address,
    owner_private_key=cfg.owner_private_key,
    contract_abi=cfg.vpn_contract_abi,
    contract_address=cfg.vpn_contract_address
)

nds_contract = ContractNDS(
    contract_abi=cfg.nds_contract_abi,
    contract_address=cfg.nds_contract_address
)

db = PG(cfg.db_user, cfg.db_pass, cfg.db_host, cfg.db_port, cfg.db_name)

tx_repo = TxRepository(db)
tx_service = TxService(tx_repo, vpn_contract, nds_contract)

if __name__ == '__main__':
    args = parser.parse_args()

    if args.app == "tx_agent":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(NewTxAgent(tx_service, cfg.vpn_contract_address, db))



