#!/usr/bin/env python3
"""
Growth Metrics Tracker

Scans the knowledge base and produces data/growth-metrics.json with:
- Total tool docs and count per category
- Docs with/without code examples
- Shallow docs (< 1500 chars)
- Underdeveloped categories (< 8 docs)
- Weekly additions delta (compared to previous snapshot)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS_DIR = Path("docs/tools")
SERVICES_DIR = Path("docs/services")
KB_DIR = Path("docs/knowledge_base")
OUTPUT_PATH = Path("data/growth-metrics.json")


def count_docs(base: Path) -> dict[str, list[str]]:
    """Return {category: [file_paths]} for all .md files (excluding index files)."""
    result: dict[str, list[str]] = {}
    if not base.exists():
        return result
    for category_dir in sorted(base.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        docs = []
        for md in sorted(category_dir.glob("*.md")):
            if md.name in ("index.md", "README.md"):
                continue
            docs.append(str(md))
        if docs:
            result[category] = docs
    return result


def has_code_examples(path: str) -> bool:
    """Check if a doc contains fenced code blocks."""
    text = Path(path).read_text(encoding="utf-8")
    return "```" in text


def is_shallow(path: str, threshold: int = 1500) -> bool:
    """Check if a doc is shorter than threshold characters."""
    text = Path(path).read_text(encoding="utf-8")
    return len(text) < threshold


def count_intake_activity() -> tuple[int, int]:
    """Count intake items and integrated items from the last 7 days of daily logs."""
    import re
    sources_dir = Path("docs/new-sources")
    if not sources_dir.exists():
        return 0, 0

    cutoff = datetime.now(timezone.utc) - __import__("datetime").timedelta(days=7)
    total = 0
    integrated = 0

    for log_file in sources_dir.glob("*.md"):
        # Parse date from filename (YYYY-MM-DD.md)
        match = re.match(r"(\d{4}-\d{2}-\d{2})\.md$", log_file.name)
        if not match:
            continue
        file_date = datetime.strptime(match.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
        if file_date < cutoff:
            continue

        text = log_file.read_text(encoding="utf-8")
        # Count table rows (lines starting with |, excluding header/separator)
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Status"):
                continue
            cells = [c.strip() for c in line.split("|")]
            if len(cells) < 3:
                continue
            total += 1
            status = cells[1].lower() if len(cells) > 1 else ""
            if "integrated" in status:
                integrated += 1

    return total, integrated


def load_previous() -> dict:
    """Load previous snapshot for delta calculation."""
    if OUTPUT_PATH.exists():
        return json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    by_category = count_docs(TOOLS_DIR)

    all_docs: list[str] = []
    for docs in by_category.values():
        all_docs.extend(docs)

    # Also count services
    service_docs = [str(p) for p in SERVICES_DIR.glob("*.md") if p.name not in ("README.md", "inventory.md")]
    all_docs.extend(service_docs)

    docs_with_code = [d for d in all_docs if has_code_examples(d)]
    docs_without_code = [d for d in all_docs if not has_code_examples(d)]
    shallow = [d for d in all_docs if is_shallow(d)]

    category_counts = {cat: len(docs) for cat, docs in by_category.items()}
    underdeveloped = [cat for cat, count in category_counts.items() if count < 8]

    # Sort shallow docs by file size (smallest first) for prioritisation
    shallow.sort(key=lambda p: Path(p).stat().st_size)

    previous = load_previous()
    prev_total = previous.get("total_docs", len(all_docs))

    # Intake conversion metrics
    intake_items_7d, intake_integrated_7d = count_intake_activity()

    snapshot = {
        "snapshot_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "total_docs": len(all_docs),
        "tool_docs": len(all_docs) - len(service_docs),
        "service_docs": len(service_docs),
        "by_category": category_counts,
        "docs_with_code_examples": len(docs_with_code),
        "docs_without_code_examples": len(docs_without_code),
        "shallow_docs": shallow[:20],  # top 20 shallowest
        "underdeveloped_categories": underdeveloped,
        "weekly_additions": len(all_docs) - prev_total,
        "intake_items_7d": intake_items_7d,
        "intake_integrated_7d": intake_integrated_7d,
        "intake_conversion_rate": round(intake_integrated_7d / intake_items_7d * 100, 1) if intake_items_7d else 0.0,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"Growth snapshot: {len(all_docs)} total docs, {len(docs_with_code)} with code, {len(shallow)} shallow.")
    print(f"Underdeveloped categories: {', '.join(underdeveloped) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
