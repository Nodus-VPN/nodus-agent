set_last_processed_block_query = """
INSERT INTO last_processed_block (last_processed_block)
VALUES (:last_processed_block)
RETURNING id;
"""

set_tx_query = """
INSERT INTO txs (client_address, tx_hash, tx_block)
VALUES (:client_address, :tx_hash, :tx_block)
RETURNING id;
"""

get_all_tx_query = """
SELECT * FROM txs;
"""

get_last_processed_block_query = """
SELECT * FROM last_processed_block
WHERE id = 1;
"""

update_last_processed_block_query = """
UPDATE last_processed_block
SET last_processed_block = :last_processed_block
WHERE id = 1;
"""