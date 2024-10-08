set_node_query = """
INSERT INTO nodes (node_ip)
VALUES (:node_ip)
RETURNING id;
"""