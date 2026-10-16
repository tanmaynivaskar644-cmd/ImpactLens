from app.graph_db import get_graph


def analyze_impact(function_name, graph_name="sample_repo", file_path=None):
    graph = get_graph(graph_name)

    # A function name may appear in multiple files.
    matches = graph.query(
        """
        MATCH (f:Function {name: $name})
        RETURN id(f), f.name, f.path
        """,
        params={"name": function_name},
    ).result_set

    if file_path is not None:
        matches = [row for row in matches if row[2] == file_path]

    if not matches:
        raise ValueError(
            f"No matching function '{function_name}' found in '{graph_name}'."
        )

    if len(matches) > 1:
        paths = "\n".join(f"  {row[2]}" for row in matches)
        raise ValueError(
            f"Multiple functions named '{function_name}' found.\n"
            f"Use --file with one of these exact paths:\n{paths}"
        )

    target_id, target_name, target_file = matches[0]

    # Use the ID only within this query session; do not save it
    # as a permanent identifier across re-indexing.
    rows = graph.query(
        """
        MATCH p = (caller:Function)-[:CALLS*1..5]->
                  (changed:Function)
        WHERE id(changed) = $target_id
          AND id(caller) <> id(changed)
        RETURN DISTINCT
            caller.name,
            caller.path,
            length(p),
            [node IN nodes(p) | node.name]
        ORDER BY length(p), caller.name
        LIMIT 100
        """,
        params={"target_id": target_id},
    ).result_set

    return {
        "function": target_name,
        "file": target_file,
        "graph": graph_name,
        "max_depth": 5,
        "path_limit": 100,
        "paths": [
            {
                "caller": row[0],
                "file": row[1],
                "distance": row[2],
                "path": row[3],
            }
            for row in rows
        ],
    }