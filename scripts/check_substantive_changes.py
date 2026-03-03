#!/usr/bin/env python3
"""
Substantive-change gate for docs PRs.

Fails if ALL changed Markdown files under docs/ contain ONLY metadata updates
(Last reviewed date, Confidence level) with no real content changes.
This prevents PRs that just bump review dates from being merged.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

METADATA_PATTERNS = [
    re.compile(r"^\s*[-+]\s*-\s*Last reviewed:\s*\d{4}-\d{2}-\d{2}\s*$"),
    re.compile(r"^\s*[-+]\s*-\s*Confidence:\s*(high|medium|low)\s*$"),
]


def is_metadata_only_line(line: str) -> bool:
    """Return True if a diff line is purely a metadata change."""
    return any(p.match(line) for p in METADATA_PATTERNS)


def get_changed_docs(base_sha: str, head_sha: str) -> list[str]:
    """Return list of changed .md files under docs/."""
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_sha}...{head_sha}"],
        capture_output=True,
        text=True,
    )
    return [
        f
        for f in result.stdout.strip().splitlines()
        if f.startswith("docs/") and f.endswith(".md")
    ]


def has_substantive_diff(base_sha: str, head_sha: str, filepath: str) -> bool:
    """Check if a file has changes beyond metadata lines."""
    result = subprocess.run(
        ["git", "diff", f"{base_sha}...{head_sha}", "--", filepath],
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        # Only look at added/removed lines (not context or headers)
        if not line.startswith(("+", "-")):
            continue
        # Skip diff headers
        if line.startswith(("+++", "---")):
            continue
        # Skip empty diff lines
        stripped = line[1:].strip()
        if not stripped:
            continue
        # If this line is NOT metadata, it's substantive
        if not is_metadata_only_line(line):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: check_substantive_changes.py <base_sha> <head_sha>")
        return 1

    base_sha = sys.argv[1]
    head_sha = sys.argv[2]

    changed_docs = get_changed_docs(base_sha, head_sha)
    if not changed_docs:
        print("No docs changed; skipping substantive-change check.")
        return 0

    metadata_only_files = []
    substantive_files = []

    for filepath in changed_docs:
        if has_substantive_diff(base_sha, head_sha, filepath):
            substantive_files.append(filepath)
        else:
            metadata_only_files.append(filepath)

    if metadata_only_files:
        print("Metadata-only changes (no substantive content):")
        for f in metadata_only_files:
            print(f"  - {f}")

    if substantive_files:
        print(f"\nSubstantive changes found in {len(substantive_files)} file(s). OK.")
        return 0

    # ALL changes are metadata-only
    print(
        "\nError: ALL changed docs contain only metadata updates "
        "(Last reviewed / Confidence). No substantive content changes detected."
    )
    print("PRs must include real content changes alongside metadata updates.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
