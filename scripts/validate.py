#!/usr/bin/env python3
"""Validate every workflow file. n8n: JSON parses, required keys exist,
node names are unique, and every connection references a real node.
Make: JSON parses, flow modules (including router routes) carry id,
module, and version, and module ids are unique. GitHub Actions: YAML
parses with triggers, jobs, and steps present (actionlint does the deep
linting in CI)."""
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
        # Check every connection group (main, ai_languageModel, ai_tool,
        # …), not just main.
        for group, branches in outputs.items():
            if not isinstance(branches, list):
                fail(f"{path}: connection group '{group}' of '{source}' is not a list")
                continue
            for branch in branches:
                for target in branch or []:
                    if target.get("node") not in name_set:
                        fail(
                            f"{path}: {group} connection {source} → "
                            f"{target.get('node')} targets a missing node"
                        )

    print(f"ok    {path}")

make_files = sorted(pathlib.Path("make").glob("*.make.json"))


def walk_modules(flow, path, seen_ids):
    for module in flow:
        for key in ("id", "module", "version"):
            if key not in module:
                fail(f"{path}: module {module.get('id', '?')} missing '{key}'")
        mid = module.get("id")
        if mid in seen_ids:
            fail(f"{path}: duplicate module id {mid}")
        seen_ids.add(mid)
        for route in module.get("routes", []):
            walk_modules(route.get("flow", []), path, seen_ids)


for path in make_files:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        fail(f"{path}: invalid JSON ({e})")
        continue
    if not data.get("name"):
        fail(f"{path}: 'name' is required")
    flow = data.get("flow")
    if not isinstance(flow, list) or not flow:
        fail(f"{path}: 'flow' must be a non-empty list")
        continue
    if "metadata" not in data:
        fail(f"{path}: 'metadata' is required")
    walk_modules(flow, path, set())
    print(f"ok    {path}")

gha_files = sorted(pathlib.Path("github-actions").glob("*.yml"))
try:
    import yaml  # provided by the CI step; on runners/dev machines with PyYAML

    for path in gha_files:
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError as e:
            fail(f"{path}: invalid YAML ({e})")
            continue
        if not isinstance(data, dict):
            fail(f"{path}: not a mapping")
            continue
        # PyYAML parses the `on:` key as boolean True (YAML 1.1).
        if "on" not in data and True not in data:
            fail(f"{path}: missing 'on' trigger")
        jobs = data.get("jobs")
        if not isinstance(jobs, dict) or not jobs:
            fail(f"{path}: 'jobs' must be a non-empty mapping")
        else:
            for job_name, job in jobs.items():
                steps = job.get("steps")
                if not isinstance(steps, list) or not steps:
                    fail(f"{path}: job '{job_name}' has no steps")
                    continue
                for step in steps:
                    if "run" not in step and "uses" not in step:
                        fail(
                            f"{path}: job '{job_name}' has a step with "
                            "neither 'run' nor 'uses'"
                        )
        print(f"ok    {path}")
except ImportError:
    fail("PyYAML is required to validate github-actions/*.yml (pip install pyyaml)")

total = len(files) + len(make_files) + len(gha_files)
if failures:
    print(f"\n{failures} problem(s).")
    sys.exit(1)
print(f"\nAll {total} workflow files valid.")
