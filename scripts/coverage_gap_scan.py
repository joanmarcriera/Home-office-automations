#!/usr/bin/env python3
"""
Coverage Gap Scanner — self-evolution for the knowledge base.

Existing automation (cross_link_report.py) finds *unlinked mentions of tools we
already document*. This scanner finds the inverse and forward-looking gaps so the
bots can EXPAND coverage toward where the industry is going, not just re-audit
existing pages:

  1. Frontier gaps   — entries in data/frontier_watchlist.json (a curated,
                       version-controlled, OFFLINE list of industry-frontier and
                       offline-first tools/topics) that have no canonical page yet.
  2. Dangling refs   — tools named in "Related tools / concepts" sections that
                       link to a page which does not exist (broken forward refs).
  3. Thin categories — taxonomy buckets with conspicuously few canonical pages.

Everything it needs lives in the repo (catalog + watchlist + docs), so it runs
fully offline. With --create-issue it opens a single throttled `jules` issue
listing the highest-value gaps for an agent to fill.

Usage:
  python3 scripts/coverage_gap_scan.py                 # human-readable report
  python3 scripts/coverage_gap_scan.py --json          # machine-readable
  python3 scripts/coverage_gap_scan.py --create-issue  # open a gap-fill issue
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "data" / "all_tools.json"
WATCHLIST_PATH = REPO_ROOT / "data" / "frontier_watchlist.json"
DOCS_DIR = REPO_ROOT / "docs"

# Categories whose page count below this is flagged as "thin" (excludes meta
# buckets that are legitimately small).
THIN_CATEGORY_THRESHOLD = 5
META_CATEGORIES = {
    "Patterns",
    "Knowledge Base",
    "Reference Implementations",
    "Architecture",
    "Playbooks",
    "Services",
}


def normalize(name: str) -> str:
    """Lowercase and strip non-alphanumerics for tolerant name matching."""
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def _load_json(path: Path) -> dict:
    """Load JSON, degrading to {} with a warning instead of crashing a scheduled run."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"WARNING: could not parse {path}: {exc}", file=sys.stderr)
        return {}


def load_catalog() -> tuple[list[dict], set[str], dict[str, int]]:
    if not CATALOG_PATH.exists():
        return [], set(), {}
    data = _load_json(CATALOG_PATH)
    tools = data.get("tools", [])
    names = {normalize(t.get("name", "")) for t in tools if t.get("name")}
    category_counts: dict[str, int] = {}
    for t in tools:
        category_counts[t.get("category", "?")] = category_counts.get(t.get("category", "?"), 0) + 1
    return tools, names, category_counts


def load_watchlist() -> list[dict]:
    if not WATCHLIST_PATH.exists():
        return []
    return _load_json(WATCHLIST_PATH).get("entries", [])


def find_frontier_gaps(watchlist: list[dict], catalog_names: set[str]) -> list[dict]:
    """Watchlist entries not yet present in the catalog (by name or alias)."""
    gaps = []
    for entry in watchlist:
        candidates = [entry.get("name", "")] + entry.get("aliases", [])
        if any(normalize(c) in catalog_names for c in candidates if c):
            continue
        gaps.append(entry)
    # Highest priority first, then offline-capable first (offline is the repo's edge).
    priority = {"high": 0, "medium": 1, "low": 2}
    gaps.sort(key=lambda e: (priority.get(e.get("priority", "medium"), 1),
                             0 if e.get("offline_capable") else 1,
                             e.get("name", "")))
    return gaps


def find_thin_categories(category_counts: dict[str, int]) -> list[dict]:
    thin = []
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1]):
        if cat in META_CATEGORIES:
            continue
        if count < THIN_CATEGORY_THRESHOLD:
            thin.append({"category": cat, "count": count})
    return thin


def find_dangling_related_refs(catalog: list[dict]) -> list[dict]:
    """Markdown links under a 'Related tools' heading that target a missing file."""
    known_paths = {t.get("doc_path", "").lstrip("/") for t in catalog}
    link_re = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)[^)]*\)")
    dangling: list[dict] = []
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        idx = lower.find("related tools")
        if idx == -1:
            continue
        section = text[idx:]
        for label, target in link_re.findall(section):
            if target.startswith(("http://", "https://")):
                continue
            # Resolve relative to the file's directory.
            resolved = (md_file.parent / target).resolve()
            if not resolved.exists():
                rel_target = target
                # Skip anchors/self-references that resolve fine elsewhere.
                if str(resolved).replace(str(REPO_ROOT) + "/", "") in known_paths:
                    continue
                dangling.append({"file": str(md_file.relative_to(REPO_ROOT)),
                                 "label": label, "target": rel_target})
    # De-dup
    seen = set()
    out = []
    for d in dangling:
        key = (d["file"], d["target"])
        if key not in seen:
            seen.add(key)
            out.append(d)
    return out


def build_report(frontier: list[dict], thin: list[dict], dangling: list[dict]) -> str:
    lines = ["# Coverage Gap Report", ""]

    lines.append(f"## Frontier gaps ({len(frontier)})")
    lines.append("Industry-frontier / offline-first tools on the watchlist with no canonical page yet.")
    lines.append("")
    if frontier:
        for e in frontier:
            tags = ", ".join(e.get("tags", []))
            offline = "🔌 offline" if e.get("offline_capable") else "☁️ cloud"
            lines.append(
                f"- **{e.get('name', '?')}** ({e.get('suggested_category', '?')}, {e.get('priority', 'medium')} priority, {offline})"
                f" — {e.get('why', '')}" + (f" _[{tags}]_" if tags else "")
            )
    else:
        lines.append("- None — watchlist fully covered. 🎉")
    lines.append("")

    lines.append(f"## Dangling 'Related tools' links ({len(dangling)})")
    if dangling:
        for d in dangling[:25]:
            lines.append(f"- `{d['file']}`: **{d['label']}** → missing `{d['target']}`")
    else:
        lines.append("- None.")
    lines.append("")

    lines.append(f"## Thin categories ({len(thin)})")
    if thin:
        for t in thin:
            lines.append(f"- **{t['category']}** — only {t['count']} page(s)")
    else:
        lines.append("- None below threshold.")
    lines.append("")
    return "\n".join(lines)


def create_issue(report: str, frontier: list[dict]) -> bool:
    # Throttle: don't stack coverage-gap issues.
    existing = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--search",
         "Coverage gap fill in:title", "--json", "number"],
        capture_output=True, text=True,
    )
    if existing.returncode == 0 and existing.stdout.strip() not in ("", "[]"):
        print("An open 'Coverage gap fill' issue already exists. Skipping (throttled).")
        return False

    if not frontier:
        print("No frontier gaps to fill. Skipping issue creation.")
        return False

    top = ", ".join(e.get("name", "?") for e in frontier[:5])
    title = f"Coverage gap fill: {top}"
    body = (
        report
        + "\n\n---\n\n"
        + "**For the agent:** create canonical pages for the highest-priority frontier "
        + "gaps above, following `docs/standards.md` (correct taxonomy directory + all "
        + "required sections). Prefer offline-capable tools first — offline usefulness is "
        + "this repo's differentiator. Use `/new-tool-doc <name> <category>` to scaffold. "
        + "Then add the new tool to `data/all_tools.json` and remove nothing from the watchlist "
        + "(the scanner stops flagging it automatically once catalogued)."
    )
    result = subprocess.run(
        ["gh", "issue", "create", "--title", title, "--body", body, "--label", "jules"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(f"Created issue: {result.stdout.strip()}")
        return True
    print(f"Failed to create issue: {result.stderr}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan the knowledge base for coverage gaps.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--create-issue", action="store_true", help="Open a throttled gap-fill issue.")
    args = parser.parse_args()

    catalog, catalog_names, category_counts = load_catalog()
    watchlist = load_watchlist()

    frontier = find_frontier_gaps(watchlist, catalog_names)
    thin = find_thin_categories(category_counts)
    dangling = find_dangling_related_refs(catalog)

    if args.json:
        print(json.dumps(
            {"frontier_gaps": frontier, "thin_categories": thin, "dangling_refs": dangling},
            indent=2,
        ))
    else:
        print(build_report(frontier, thin, dangling))

    if args.create_issue:
        create_issue(build_report(frontier, thin, dangling), frontier)

    return 0


if __name__ == "__main__":
    sys.exit(main())
