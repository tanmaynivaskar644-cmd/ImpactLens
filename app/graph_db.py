from falkordb import FalkorDB


def get_graph(graph_name="impactlens_demo"):
    db = FalkorDB(host="localhost", port=6379)
    return db.select_graph(graph_name)