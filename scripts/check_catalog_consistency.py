#!/usr/bin/env python3
"""
Ensure canonical service/tool pages listed in MkDocs nav are present in data/all_tools.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MKDOCS_PATH = Path("mkdocs.yml")
TOOLS_JSON_PATH = Path("data/all_tools.json")
NAV_ENTRY_RE = re.compile(r":\s+((?:services|tools)/[^\s]+\.md)\s*$")
EXCLUDED_NAV_PATHS = {
    "services/README.md",
    "services/inventory.md",
}
EXCLUDED_BASENAMES = {"index.md", "README.md"}


def canonical_nav_paths() -> set[str]:
    paths: set[str] = set()
    for raw_line in MKDOCS_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        match = NAV_ENTRY_RE.search(line)
        if not match:
            continue
        rel_path = match.group(1)
        if rel_path in EXCLUDED_NAV_PATHS:
            continue
        if Path(rel_path).name in EXCLUDED_BASENAMES:
            continue
        paths.add(f"docs/{rel_path}")
    return paths


def tool_catalog_paths() -> set[str]:
    payload = json.loads(TOOLS_JSON_PATH.read_text(encoding="utf-8"))
    return {entry["doc_path"] for entry in payload.get("tools", [])}


def main() -> int:
    nav_paths = canonical_nav_paths()
    catalog_paths = tool_catalog_paths()

    missing = sorted(nav_paths - catalog_paths)
    extras = sorted(
        p for p in (catalog_paths - nav_paths)
        if p.startswith(("docs/tools/", "docs/services/"))
    )

    if missing:
        print("Catalog consistency check failed.")
        print("The following canonical pages are in mkdocs nav but missing from data/all_tools.json:")
        for path in missing:
            print(f"- {path}")
        return 1

    print(
        f"Catalog consistency check passed for {len(nav_paths)} canonical nav page(s)."
    )
    if extras:
        print("Note: these catalog entries are not currently in mkdocs nav:")
        for path in extras:
            print(f"- {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
