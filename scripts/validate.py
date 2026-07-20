#!/usr/bin/env python3
"""Validate every n8n workflow file: JSON parses, required keys exist,
node names are unique, and every connection references a real node."""
import json
import pathlib
import sys

failures = 0


def fail(msg: str) -> None:
    global failures
    failures += 1
    print(f"FAIL  {msg}")


files = sorted(pathlib.Path("n8n").glob("*.n8n.json"))
if not files:
    fail("no workflow files found under n8n/")

for path in files:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        fail(f"{path}: invalid JSON ({e})")
        continue

    nodes = data.get("nodes")
    connections = data.get("connections")
    if not isinstance(nodes, list) or not nodes:
        fail(f"{path}: 'nodes' must be a non-empty list")
        continue
    if not isinstance(connections, dict):
        fail(f"{path}: 'connections' must be an object")
        continue

    names = [n.get("name") for n in nodes]
    if len(set(names)) != len(names):
        fail(f"{path}: node names must be unique")
    for n in nodes:
        for key in ("name", "type", "typeVersion", "position"):
            if key not in n:
                fail(f"{path}: node {n.get('name', '?')} missing '{key}'")

    name_set = set(names)
    for source, outputs in connections.items():
        if source not in name_set:
            fail(f"{path}: connection source '{source}' is not a node")
        for branch in outputs.get("main", []):
            for target in branch:
                if target.get("node") not in name_set:
                    fail(
                        f"{path}: connection {source} → "
                        f"{target.get('node')} targets a missing node"
                    )

    print(f"ok    {path}")

if failures:
    print(f"\n{failures} problem(s).")
    sys.exit(1)
print(f"\nAll {len(files)} workflow files valid.")
