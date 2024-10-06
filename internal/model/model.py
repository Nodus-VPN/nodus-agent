from dataclasses import dataclass
from datetime import datetime


@dataclass
class Tx:
    id: int
    client_address: str
    tx_hash: str
    tx_block: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def serialize(
            cls,
            rows
    ):
        return [cls(
            id=row.id,
            client_address=row.client_address,
            tx_hash=row.tx_hash,
            tx_block=row.tx_block,
            created_at=row.created_at,
            updated_at=row.updated_at
        ) for row in rows]
