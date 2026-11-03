#!/usr/bin/env python3
"""Report backtick-quoted ``scripts/...`` paths in docs that do not exist.

Usage:
    python3 scripts/check_doc_script_refs.py [--root DIR] [--docs-dir REL]

Scans every ``*.md`` file directly under ``<root>/<docs-dir>`` (default
``docs/services``) for inline-code spans such as `scripts/foo.py` or
`python3 scripts/foo.py --flag`, and prints ``file:line: missing <path>`` for
each referenced path that is absent under ``<root>``. Fenced code blocks are
skipped (they hold illustrative snippets, not repository references).

Exit status: 0 when every reference resolves, 1 when any is missing.
Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CODE_SPAN = re.compile(r"`([^`\n]+)`")
SCRIPT_PATH = re.compile(r"(?<![\w./-])(scripts/[\w./-]*[\w-])")
FENCE = re.compile(r"^\s*(```|~~~)")


def find_missing(root: Path, docs_dir: str = "docs/services") -> list[tuple[str, int, str]]:
    """Return (relative file, line number, script path) for each dangling reference."""
    missing = []
    for md in sorted((root / docs_dir).glob("*.md")):
        in_fence = False
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for span in CODE_SPAN.findall(line):
                for path in SCRIPT_PATH.findall(span):
                    if not (root / path).exists():
                        missing.append((md.relative_to(root).as_posix(), lineno, path))
    return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=Path(__file__).resolve().parent.parent, type=Path,
                        help="repository root (default: parent of scripts/)")
    parser.add_argument("--docs-dir", default="docs/services",
                        help="docs directory to scan, relative to --root")
    args = parser.parse_args(argv)
    missing = find_missing(args.root, args.docs_dir)
    for rel, lineno, path in missing:
        print(f"{rel}:{lineno}: missing {path}")
    print(f"{len(missing)} dangling scripts/ reference(s)", file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
