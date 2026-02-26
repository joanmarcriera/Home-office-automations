#!/usr/bin/env python3
"""
Update source prioritisation scores.

Reads all docs/new-sources/*.md files, tallies per-source discovery and
integration counts, computes a score (integrated/discovered ratio), and
writes data/source-scores.json.

Sources with higher integration ratios are prioritised by the bridge script.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path("docs/new-sources")
OUTPUT_PATH = Path("data/source-scores.json")

URL_RE = re.compile(r"https?://(?:www\.)?([^/]+)")


def extract_domain(url: str) -> str:
    """Extract domain from a URL."""
    match = URL_RE.search(url)
    return match.group(1) if match else "unknown"


def main() -> int:
    if not LOG_DIR.exists():
        print(f"{LOG_DIR} not found.")
        return 1

    # Tally per-domain: discovered vs integrated
    stats: dict[str, dict[str, int]] = defaultdict(lambda: {"discovered": 0, "integrated": 0})

    for log_file in sorted(LOG_DIR.glob("*.md")):
        for line in log_file.read_text(encoding="utf-8").splitlines():
            if not line.strip().startswith("|") or line.strip().startswith("| :"):
                continue
            if line.strip().startswith("| Title"):
                continue

            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) < 4:
                continue

            url_cell = cols[1]
            status = cols[3].strip().lower()

            # Extract URL from markdown link or bare URL
            url_match = re.search(r"https?://[^\s)]+", url_cell)
            if not url_match:
                continue

            domain = extract_domain(url_match.group(0))
            stats[domain]["discovered"] += 1
            if status == "integrated":
                stats[domain]["integrated"] += 1

    # Compute scores
    sources = {}
    for domain, counts in sorted(stats.items()):
        discovered = counts["discovered"]
        integrated = counts["integrated"]
        score = round(integrated / discovered, 2) if discovered > 0 else 0.0
        sources[domain] = {
            "discovered": discovered,
            "integrated": integrated,
            "score": score,
        }

    output = {
        "sources": sources,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT_PATH} with {len(sources)} source scores.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
