create_txs_table_query = """
CREATE TABLE IF NOT EXISTS txs (
id SERIAL PRIMARY KEY,

client_address TEXT NOT NULL,
tx_hash TEXT NOT NULL,
tx_block INTEGER NOT NULL,

created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

create_last_processed_block_table_query = """
CREATE TABLE IF NOT EXISTS last_processed_block (
id SERIAL PRIMARY KEY,

last_processed_block INTEGER NOT NULL,

created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

create_on_update_table_func_query = """
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';
"""

on_update_txs_query = """
CREATE TRIGGER update_updated_at_trigger
BEFORE UPDATE ON txs
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at();
"""
on_update_last_processed_block_query = """
CREATE TRIGGER update_updated_at_trigger
BEFORE UPDATE ON last_processed_block
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at();
"""

drop_txs_table_query = """
DROP TABLE IF EXISTS txs;
"""

drop_last_processed_block_table_query = """
DROP TABLE IF EXISTS last_processed_block;
"""

drop_on_update_txs_trigger_query = """
DROP TRIGGER IF EXISTS update_updated_at_trigger ON txs;
"""
drop_on_update_last_processed_block_trigger_query = """
DROP TRIGGER IF EXISTS update_updated_at_trigger ON last_processed_block;
"""

create_queries = [
    create_txs_table_query,
    create_last_processed_block_table_query,
    create_on_update_table_func_query,
    on_update_txs_query,
    on_update_last_processed_block_query
]

drop_queries = [
    drop_txs_table_query,
    drop_last_processed_block_table_query,
    drop_on_update_txs_trigger_query,
    drop_on_update_last_processed_block_trigger_query
]
