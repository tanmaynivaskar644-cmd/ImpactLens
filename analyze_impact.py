import argparse
import json

from app.impact import analyze_impact


def main():
    parser = argparse.ArgumentParser(
        description="Find potential code impact using FalkorDB."
    )
    parser.add_argument("function", help="Function name to investigate")
    parser.add_argument("--graph", default="sample_repo")
    parser.add_argument("--file", help="Exact indexed file path")
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    try:
        report = analyze_impact(
            function_name=args.function,
            graph_name=args.graph,
            file_path=args.file,
        )
    except ValueError as error:
        parser.exit(1, f"{error}\n")

    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"\nImpact analysis: {report['function']}")
    print(f"Source: {report['file']}")
    print(f"Graph: {report['graph']}\n")

    if not report["paths"]:
        print("No callers found within five steps in the indexed graph.")
        print("This does not prove the change is safe.")
        return

    callers = {
        (item["caller"], item["file"])
        for item in report["paths"]
    }
    print(f"Potentially affected functions: {len(callers)}\n")

    for item in report["paths"]:
        relationship = "direct" if item["distance"] == 1 else "indirect"
        print(f"- {item['caller']} ({relationship})")
        print(f"  File: {item['file']}")
        print(f"  Evidence: {' -> '.join(item['path'])}\n")

    print("Scope: up to five call steps and 100 paths.")
    print("Results describe indexed dependencies; no tests have been run.")


if __name__ == "__main__":
    main()