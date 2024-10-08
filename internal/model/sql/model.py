create_uptime_table_query = """
CREATE TABLE IF NOT EXISTS uptime (
id SERIAL PRIMARY KEY,

node_ip TEXT NOT NULL,
response_count INTEGER DEFAULT 0,
failed_count INTEGER DEFAULT 0,
traffic INTEGER DEFAULT 0,
unique_clients INTEGER DEFAULT 0,
client_hours INTEGER DEFAULT 0,


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

on_update_uptime_query = """
CREATE TRIGGER update_updated_at_trigger
BEFORE UPDATE ON uptime
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at();
"""

drop_uptime_table_query = """
DROP TABLE IF EXISTS uptime;
"""

drop_on_update_txs_trigger_query = """
DROP TRIGGER IF EXISTS update_updated_at_trigger ON uptime;
"""

create_queries = [
    create_uptime_table_query,
    create_on_update_table_func_query,
    on_update_uptime_query
]

drop_queries = [
    drop_uptime_table_query,
    drop_on_update_txs_trigger_query
]
