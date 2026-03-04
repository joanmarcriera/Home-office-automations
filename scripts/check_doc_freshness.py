#!/usr/bin/env python3
"""
Check freshness of knowledge docs by their "Last reviewed" metadata date.

Usage examples:
  python3 scripts/check_doc_freshness.py docs/knowledge_base/api_pricing_free_tiers.md
  python3 scripts/check_doc_freshness.py docs/knowledge_base/api_pricing_free_tiers.md --max-days 21 --github-output "$GITHUB_OUTPUT"
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

LAST_REVIEWED_RE = re.compile(r"^\s*-\s*Last reviewed:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def extract_last_reviewed(path: Path) -> dt.date | None:
    text = path.read_text(encoding="utf-8")
    match = LAST_REVIEWED_RE.search(text)
    if not match:
        return None
    try:
        return dt.date.fromisoformat(match.group(1))
    except ValueError:
        return None


def write_github_output(output_path: str, stale_any: bool, report: str) -> None:
    with open(output_path, "a", encoding="utf-8") as fh:
        fh.write(f"stale_any={'true' if stale_any else 'false'}\n")
        fh.write("freshness_report<<EOF\n")
        fh.write(report.rstrip() + "\n")
        fh.write("EOF\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Last reviewed freshness for docs.")
    parser.add_argument("paths", nargs="+", help="Markdown files to inspect.")
    parser.add_argument("--max-days", type=int, default=30, help="Maximum allowed age in days.")
    parser.add_argument(
        "--fail-on-stale",
        action="store_true",
        help="Exit non-zero if any file exceeds --max-days.",
    )
    parser.add_argument(
        "--github-output",
        help="Path to $GITHUB_OUTPUT to emit stale_any/freshness_report outputs.",
    )
    args = parser.parse_args()

    today = dt.date.today()
    stale_any = False
    report_lines: list[str] = []

    for raw in args.paths:
        path = Path(raw)
        if not path.exists():
            report_lines.append(f"{raw}: missing file")
            stale_any = True
            continue

        reviewed = extract_last_reviewed(path)
        if reviewed is None:
            report_lines.append(f"{raw}: missing or invalid Last reviewed metadata")
            stale_any = True
            continue

        age_days = (today - reviewed).days
        if age_days > args.max_days:
            report_lines.append(
                f"{raw}: STALE ({age_days} days old, last reviewed {reviewed.isoformat()})"
            )
            stale_any = True
        else:
            report_lines.append(
                f"{raw}: fresh ({age_days} days old, last reviewed {reviewed.isoformat()})"
            )

    report = "\n".join(report_lines)
    print(report)

    if args.github_output:
        write_github_output(args.github_output, stale_any, report)

    if stale_any and args.fail_on_stale:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
