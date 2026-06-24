#!/usr/bin/env python3
"""
Fix broken internal Markdown links deterministically and safely.

Lychee runs with `fail: false`, so broken relative links between docs (wrong
`../` depth, files that moved between taxonomy directories) accumulate silently.
This repairs only the UNAMBIGUOUS cases:

  A link target ending in `.md` that does NOT resolve from the source file's
  directory is rewritten ONLY when its basename exists at exactly ONE location
  under docs/. If the basename is missing (0 matches) or ambiguous (>1 match),
  the link is left untouched and reported, so a human/agent can decide.

This guarantees we never invent or mis-route a link. Anchors (`#section`) are
preserved.

Usage:
  python3 scripts/fix_internal_links.py            # dry run: report only
  python3 scripts/fix_internal_links.py --apply    # rewrite files in place
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+?)\)")


def build_basename_index() -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = defaultdict(list)
    for md in DOCS_DIR.rglob("*.md"):
        index[md.name].append(md)
    return index


def split_target(target: str) -> tuple[str, str]:
    """Split a link target into (path, '#anchor' or '')."""
    if "#" in target:
        path, _, anchor = target.partition("#")
        return path, "#" + anchor
    return target, ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair unambiguous broken internal .md links.")
    parser.add_argument("--apply", action="store_true", help="Rewrite files (default: dry run).")
    args = parser.parse_args()

    index = build_basename_index()
    fixed = 0
    skipped_missing = 0
    skipped_ambiguous = 0
    files_changed = 0

    for md in sorted(DOCS_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        original = text

        def replace(match: re.Match) -> str:
            nonlocal fixed, skipped_missing, skipped_ambiguous
            label, target = match.group(1), match.group(2)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                return match.group(0)
            path_part, anchor = split_target(target.strip())
            if not path_part.endswith(".md"):
                return match.group(0)

            resolved = (md.parent / path_part).resolve()
            if resolved.exists():
                return match.group(0)  # already valid

            candidates = index.get(Path(path_part).name, [])
            if len(candidates) == 1:
                correct = candidates[0]
                rel = Path(__import__("os").path.relpath(correct, md.parent)).as_posix()
                fixed += 1
                return f"[{label}]({rel}{anchor})"
            elif len(candidates) == 0:
                skipped_missing += 1
                print(f"  MISSING  {md.relative_to(REPO_ROOT)}: [{label}]({target}) — no such page")
            else:
                skipped_ambiguous += 1
                opts = ", ".join(str(c.relative_to(REPO_ROOT)) for c in candidates)
                print(f"  AMBIG    {md.relative_to(REPO_ROOT)}: [{label}]({target}) — candidates: {opts}")
            return match.group(0)

        text = LINK_RE.sub(replace, text)

        if text != original:
            files_changed += 1
            if args.apply:
                md.write_text(text, encoding="utf-8")

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"\n[{mode}] fixed={fixed} files_changed={files_changed} "
          f"skipped_missing={skipped_missing} skipped_ambiguous={skipped_ambiguous}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
