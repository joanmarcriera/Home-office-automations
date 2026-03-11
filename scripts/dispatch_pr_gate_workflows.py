#!/usr/bin/env python3
"""
Dispatch gate workflows for automation-created PR branches.

This works around the fact that PRs created by GitHub Actions with GITHUB_TOKEN
do not automatically emit pull_request-triggered workflow runs.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import PurePosixPath


WORKFLOWS = [
    {
        "file": "docs-quality-gates.yml",
        "always": True,
        "inputs": ("base_sha", "head_sha"),
    },
    {
        "file": "docs-link-health.yml",
        "always": True,
        "inputs": (),
    },
    {
        "file": "catalog-quality-gates.yml",
        "patterns": (
            "mkdocs.yml",
            "data/all_tools.json",
            "docs/services/*.md",
            "docs/tools/**/*.md",
            "scripts/check_catalog_consistency.py",
            ".github/workflows/catalog-quality-gates.yml",
        ),
        "inputs": (),
    },
    {
        "file": "intake-quality-gates.yml",
        "patterns": (
            "docs/new-sources.md",
            "docs/new-sources/*.md",
            "scripts/validate_new_sources.py",
            ".github/workflows/intake-quality-gates.yml",
        ),
        "inputs": (),
    },
    {
        "file": "generated-content-gates.yml",
        "patterns": (
            "docs/knowledge_base/api_pricing_free_tiers.md",
            "scripts/update_api_pricing_capability_summary.py",
            "scripts/check_doc_freshness.py",
            ".github/workflows/generated-content-gates.yml",
        ),
        "inputs": (),
    },
]


def run(cmd: list[str]) -> str:
    completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "command failed")
    return completed.stdout


def changed_files(base_sha: str, head_sha: str) -> list[str]:
    output = run(["git", "diff", "--name-only", f"{base_sha}...{head_sha}"])
    return [line.strip() for line in output.splitlines() if line.strip()]


def matches_any(path: str, patterns: tuple[str, ...]) -> bool:
    posix = PurePosixPath(path)
    return any(posix.match(pattern) for pattern in patterns)


def should_dispatch(workflow: dict, files: list[str]) -> bool:
    if workflow.get("always"):
        return True
    patterns = workflow.get("patterns", ())
    return any(matches_any(path, patterns) for path in files)


def dispatch(repo: str | None, workflow_file: str, ref: str, base_sha: str, head_sha: str, inputs: tuple[str, ...]) -> None:
    cmd = ["gh", "workflow", "run", workflow_file, "--ref", ref]
    if repo:
        cmd.extend(["--repo", repo])
    for input_name in inputs:
        if input_name == "base_sha":
            cmd.extend(["-f", f"base_sha={base_sha}"])
        elif input_name == "head_sha":
            cmd.extend(["-f", f"head_sha={head_sha}"])
    run(cmd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=False)
    parser.add_argument("--ref", required=True, help="PR branch ref to run workflows on.")
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--head-sha", required=True)
    args = parser.parse_args()

    files = changed_files(args.base_sha, args.head_sha)
    print(f"Detected {len(files)} changed file(s) between {args.base_sha} and {args.head_sha}.")
    for path in files:
        print(f"  - {path}")

    dispatched = 0
    for workflow in WORKFLOWS:
        if not should_dispatch(workflow, files):
            continue

        dispatch(
            repo=args.repo,
            workflow_file=workflow["file"],
            ref=args.ref,
            base_sha=args.base_sha,
            head_sha=args.head_sha,
            inputs=workflow.get("inputs", ()),
        )
        print(f"Triggered {workflow['file']} on {args.ref}.")
        dispatched += 1

    print(f"Triggered {dispatched} workflow(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
