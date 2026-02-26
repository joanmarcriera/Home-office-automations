#!/usr/bin/env python3
"""
Validate changed knowledge docs against the Multi-Agent KnowledgeOps contract.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

TARGET_PREFIXES = (
    "docs/tools/",
    "docs/services/",
    "docs/knowledge_base/",
    "docs/architecture/",
    "docs/playbooks/",
    "docs/reference-implementations/",
)

EXCLUDED_PREFIXES = ("docs/templates/",)
EXCLUDED_FILENAMES = {"README.md", "index.md"}

SOURCE_HEADER_RE = re.compile(r"^##\s*Sources\s*/\s*References\s*$", re.IGNORECASE | re.MULTILINE)
LAST_REVIEWED_RE = re.compile(
    r"^\s*-\s*Last reviewed:\s*(\d{4}-\d{2}-\d{2})\s*$",
    re.IGNORECASE | re.MULTILINE,
)
CONFIDENCE_RE = re.compile(
    r"^\s*-\s*Confidence:\s*(high|medium|low)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
URL_RE = re.compile(r"https?://", re.IGNORECASE)
HEADING_RE = re.compile(r"^##\s+", re.MULTILINE)


def should_check(path: Path) -> bool:
    posix_path = path.as_posix()
    if not posix_path.endswith(".md"):
        return False
    if any(posix_path.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    if path.name in EXCLUDED_FILENAMES:
        return False
    return any(posix_path.startswith(prefix) for prefix in TARGET_PREFIXES)


def validate_date(value: str) -> bool:
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def extract_section_body(text: str, header_match: re.Match[str]) -> str:
    start = header_match.end()
    remainder = text[start:]
    next_heading = HEADING_RE.search(remainder)
    if not next_heading:
        return remainder
    return remainder[: next_heading.start()]


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    source_match = SOURCE_HEADER_RE.search(text)
    if not source_match:
        errors.append("Missing `## Sources / References` section.")
    else:
        source_body = extract_section_body(text, source_match)
        if not URL_RE.search(source_body):
            errors.append("`Sources / References` section must include at least one URL.")

    last_reviewed_match = LAST_REVIEWED_RE.search(text)
    if not last_reviewed_match:
        errors.append("Missing `- Last reviewed: YYYY-MM-DD` metadata line.")
    else:
        date_value = last_reviewed_match.group(1)
        if not validate_date(date_value):
            errors.append("`Last reviewed` must be a valid ISO date (YYYY-MM-DD).")

    if not CONFIDENCE_RE.search(text):
        errors.append("Missing `- Confidence: high|medium|low` metadata line.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate changed docs against the knowledge contract.")
    parser.add_argument("paths", nargs="*", help="Repository-relative file paths to check.")
    args = parser.parse_args()

    if not args.paths:
        print("No files provided; skipping.")
        return 0

    failures: dict[Path, list[str]] = {}
    checked = 0

    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists() or not path.is_file():
            continue
        if not should_check(path):
            continue
        checked += 1
        errors = validate_file(path)
        if errors:
            failures[path] = errors

    if checked == 0:
        print("No eligible knowledge pages changed; skipping.")
        return 0

    if failures:
        print("KnowledgeOps contract check failed:\n")
        for path, errors in sorted(failures.items(), key=lambda item: item[0].as_posix()):
            print(f"- {path.as_posix()}")
            for error in errors:
                print(f"  - {error}")
        return 1

    print(f"KnowledgeOps contract check passed for {checked} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
