#!/usr/bin/env python3
"""
Render a Jules issue template with the real run date.

Why: the agent that works these issues (Google Jules) runs in a sandbox whose
clock has been observed months ahead of real time — Oct 2026 PRs arrived as
"daily knowledge expansion 2027-01-07" and stamped ~1000 docs with
`Last reviewed: 2027-01-07`. Future review dates are not just cosmetic: the
freshness checks then treat those docs as fresh until 2027. The templates used
to be copied verbatim (`cp`), so their `$TODAY` placeholders reached the agent
unexpanded and it fell back to its own clock.

This substitutes `$TODAY` / `${TODAY}` with the runner's UTC date and prepends
a banner telling the agent to use that date for every date it writes.

Usage:
  python3 scripts/render_issue_template.py TEMPLATE.md OUT.md [--date YYYY-MM-DD]

Also importable: `run_date_banner(date)` for issue bodies built in Python.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


def utc_today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def run_date_banner(date: str) -> str:
    return (
        f"> **Run date (UTC): {date}.** Use exactly this date for every date you write — "
        f"`Last reviewed:` metadata, `docs/new-sources/{date}.md`, branch names and PR "
        "titles. Do NOT take the date from your sandbox clock (it has run months ahead "
        "of real time); a `Last reviewed` date later than this one is wrong.\n"
    )


def render(template: str, date: str) -> str:
    body = template.replace("${TODAY}", date).replace("$TODAY", date)
    return run_date_banner(date) + "\n" + body


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an issue template with the run date.")
    parser.add_argument("template", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--date", default=None, help="Override the date (default: today, UTC).")
    args = parser.parse_args()
    date = args.date or utc_today()
    args.output.write_text(render(args.template.read_text(encoding="utf-8"), date), encoding="utf-8")
    print(f"Rendered {args.template} for {date} -> {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
