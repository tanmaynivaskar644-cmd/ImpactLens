from app.graph_db import get_graph


graph = get_graph()

# Create functions and their dependencies.
# MERGE avoids duplicates when you run this script again.
graph.query("""
    MERGE (order:Function {id: 'demo::place_order'})
    SET order.name = 'place_order'

    MERGE (checkout:Function {id: 'demo::checkout'})
    SET checkout.name = 'checkout'

    MERGE (tax:Function {id: 'demo::calculate_tax'})
    SET tax.name = 'calculate_tax'

    MERGE (order)-[:CALLS]->(checkout)
    MERGE (checkout)-[:CALLS]->(tax)
""")

print("Connected to FalkorDB. Sample graph created.")

# Find functions that directly or indirectly call calculate_tax.
result = graph.query(
    """
    MATCH (caller:Function)-[:CALLS*1..5]->
          (changed:Function {id: $function_id})
    WHERE caller.id <> changed.id
    RETURN DISTINCT caller.name
    ORDER BY caller.name
    """,
    params={"function_id": "demo::calculate_tax"},
)

print("\nPotentially affected by changing calculate_tax:")

for row in result.result_set:
    print(f"- {row[0]}")