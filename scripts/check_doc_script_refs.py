#!/usr/bin/env python3
"""Report references to ``scripts/...`` files in docs that do not exist.

Usage:
    python3 scripts/check_doc_script_refs.py [--root DIR] [--docs-dir REL]
                                             [--allowlist FILE]

Scans every ``*.md`` file under ``<root>/<docs-dir>`` recursively (default
``docs``; pass ``--docs-dir docs/services`` for the original scope) and prints
``file:line: missing <ref> (<class>)`` for each reference that does not
resolve under ``<root>``. Two classes are reported:

``inline``
    Inline-code spans outside fenced blocks, such as `scripts/foo.py`,
    `python3 scripts/foo.py --flag` or `python3 -m scripts.foo`.
``code-block``
    ``python3 -m scripts.<module>`` invocations inside fenced code blocks.
    Plain ``scripts/...`` paths in fenced blocks are still ignored: they are
    often container or remote-host paths in illustrative snippets.

A dotted module ``scripts.a.b`` resolves when ``scripts/a/b.py`` or the
package directory ``scripts/a/b/`` exists.

Intentional examples (design sketches that name scripts on purpose) go in the
allowlist file (default ``scripts/doc_script_refs_allowlist.txt`` under the
root, if present), one ``<doc path> <ref>`` pair per line; ``#`` starts a
comment. Allowlist entries that no longer match anything are warned about on
stderr so the list does not rot.

Exit status: 0 when every reference resolves or is allowlisted, 1 otherwise.
Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CODE_SPAN = re.compile(r"`([^`\n]+)`")
SCRIPT_PATH = re.compile(r"(?<![\w./-])(scripts/[\w./-]*[\w-])")
SCRIPT_MODULE = re.compile(r"(?<![\w.])-m\s+(scripts(?:\.\w+)+)")
FENCE = re.compile(r"^\s*(```|~~~)")
DEFAULT_ALLOWLIST = "scripts/doc_script_refs_allowlist.txt"


def load_allowlist(path: Path) -> set[tuple[str, str]]:
    """Parse ``<doc path> <ref>`` lines; blank lines and ``#`` comments are skipped."""
    entries = set()
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        fields = line.split()
        if len(fields) != 2:
            raise ValueError(f"{path}:{lineno}: expected '<doc path> <ref>', got {raw!r}")
        entries.add((fields[0], fields[1]))
    return entries


def _module_exists(root: Path, module: str) -> bool:
    rel = Path(*module.split("."))
    return (root / rel).with_suffix(".py").is_file() or (root / rel).is_dir()


def _scan(root: Path, docs_dir: str) -> list[tuple[str, int, str, str]]:
    found = []
    for md in sorted((root / docs_dir).rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        in_fence = False
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                for module in SCRIPT_MODULE.findall(line):
                    if not _module_exists(root, module):
                        found.append((rel, lineno, module, "code-block"))
                continue
            for span in CODE_SPAN.findall(line):
                for path in SCRIPT_PATH.findall(span):
                    if not (root / path).exists():
                        found.append((rel, lineno, path, "inline"))
                for module in SCRIPT_MODULE.findall(span):
                    if not _module_exists(root, module):
                        found.append((rel, lineno, module, "inline"))
    return found


def find_missing(root: Path, docs_dir: str = "docs",
                 allowlist: set[tuple[str, str]] | None = None) -> list[tuple[str, int, str, str]]:
    """Return (relative file, line, ref, class) for each dangling, non-allowlisted reference."""
    allow = allowlist or set()
    return [f for f in _scan(root, docs_dir) if (f[0], f[2]) not in allow]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=Path(__file__).resolve().parent.parent, type=Path,
                        help="repository root (default: parent of scripts/)")
    parser.add_argument("--docs-dir", default="docs",
                        help="docs directory to scan recursively, relative to --root "
                             "(default: docs; e.g. docs/services)")
    parser.add_argument("--allowlist", type=Path, default=None,
                        help=f"allowlist file (default: <root>/{DEFAULT_ALLOWLIST} if present)")
    args = parser.parse_args(argv)

    allow_path = args.allowlist or (args.root / DEFAULT_ALLOWLIST)
    allowlist = load_allowlist(allow_path) if allow_path.is_file() else set()

    scanned = _scan(args.root, args.docs_dir)
    missing = [f for f in scanned if (f[0], f[2]) not in allowlist]
    for rel, lineno, ref, kind in missing:
        print(f"{rel}:{lineno}: missing {ref} ({kind})")

    hit = {(f[0], f[2]) for f in scanned}
    for doc, ref in sorted(allowlist - hit):
        if doc.startswith(args.docs_dir.rstrip("/") + "/"):
            print(f"warning: stale allowlist entry: {doc} {ref}", file=sys.stderr)

    print(f"{len(missing)} dangling scripts reference(s)"
          f" ({len(scanned) - len(missing)} allowlisted)", file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
