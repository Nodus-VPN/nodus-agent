set_last_processed_block_query = """
INSERT INTO last_processed_block (last_processed_block)
VALUES (:last_processed_block)
RETURNING id;
"""

get_last_processed_block_query = """
SELECT * FROM last_processed_block;
WHERE id = 1;
"""

update_last_processed_block_query = """
UPDATE last_processed_block
SET last_processed_block = :last_processed_block
WHERE id = 1;
"""