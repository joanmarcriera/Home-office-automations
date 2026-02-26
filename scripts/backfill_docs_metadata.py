#!/usr/bin/env python3
"""
Backfill Sources/Contribution metadata for high-priority docs in batches.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from collections import Counter
from pathlib import Path

import check_docs_contract as contract

DOCS_ROOT = Path("docs")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://[^\s)]+", re.IGNORECASE)
HEADING_RE = re.compile(r"^##\s+", re.MULTILINE)
META_HEADING_RE = re.compile(r"^##\s*Contribution Metadata\s*$", re.IGNORECASE | re.MULTILINE)
LAST_REVIEWED_LINE_RE = re.compile(r"^\s*-\s*Last reviewed:\s*\d{4}-\d{2}-\d{2}\s*$", re.IGNORECASE | re.MULTILINE)
CONFIDENCE_LINE_RE = re.compile(r"^\s*-\s*Confidence:\s*(high|medium|low)\s*$", re.IGNORECASE | re.MULTILINE)

DEFAULT_SOURCES = {
    "docs/tools/development_ops/aider.md": ["https://aider.chat/"],
    "docs/tools/development_ops/openhands.md": ["https://github.com/All-Hands-AI/OpenHands"],
    "docs/tools/ai_knowledge/openai.md": ["https://openai.com/index/"],
    "docs/architecture/ssh_execution_patterns.md": ["https://man.openbsd.org/ssh"],
    "docs/services/litellm.md": ["https://docs.litellm.ai/"],
    "docs/tools/ai_knowledge/anthropic.md": ["https://www.anthropic.com/news"],
    "docs/tools/ai_knowledge/openrouter.md": ["https://openrouter.ai/docs/overview/introduction"],
}


def eligible_docs() -> list[Path]:
    paths: list[Path] = []
    for p in DOCS_ROOT.rglob("*.md"):
        if contract.should_check(p):
            paths.append(p)
    return sorted(paths)


def inbound_link_counts(files: list[Path]) -> Counter[str]:
    counts: Counter[str] = Counter()
    root = Path(".").resolve()
    for source in files:
        text = source.read_text(encoding="utf-8", errors="ignore")
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip()
            if raw.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_raw = raw.split("#", 1)[0].split("?", 1)[0]
            if not target_raw:
                continue
            target = (source.parent / target_raw).resolve() if not target_raw.startswith("/") else (root / target_raw.lstrip("/")).resolve()
            try:
                rel = target.relative_to(root).as_posix()
            except ValueError:
                continue
            if rel.startswith("docs/") and rel.endswith(".md"):
                counts[rel] += 1
    return counts


def extract_urls(text: str, path: Path) -> list[str]:
    urls = []
    seen = set()
    for url in URL_RE.findall(text):
        if url not in seen:
            seen.add(url)
            urls.append(url)

    for fallback in DEFAULT_SOURCES.get(path.as_posix(), []):
        if fallback not in seen:
            urls.append(fallback)
            seen.add(fallback)

    return urls[:3]


def insert_into_section(text: str, header_re: re.Pattern[str], lines_to_add: list[str]) -> str:
    match = header_re.search(text)
    if not match:
        return text

    start = match.end()
    remainder = text[start:]
    next_heading = HEADING_RE.search(remainder)
    end = start + next_heading.start() if next_heading else len(text)

    section_body = text[start:end]
    insertion = "\n" + "\n".join(lines_to_add) + "\n"
    return text[:end] + insertion + text[end:]


def ensure_sources_section(text: str, urls: list[str]) -> str:
    if not urls:
        urls = ["https://github.com/joanmarcriera/Home-office-automations"]

    source_match = contract.SOURCE_HEADER_RE.search(text)
    source_lines = [f"- [Reference]({url})" for url in urls]

    if not source_match:
        addition = "\n\n## Sources / References\n\n" + "\n".join(source_lines) + "\n"
        return text.rstrip() + addition

    source_body = contract.extract_section_body(text, source_match)
    if contract.URL_RE.search(source_body):
        return text

    return insert_into_section(text, contract.SOURCE_HEADER_RE, source_lines)


def ensure_metadata_section(text: str, today: str) -> str:
    has_last = bool(LAST_REVIEWED_LINE_RE.search(text))
    has_conf = bool(CONFIDENCE_LINE_RE.search(text))
    if has_last and has_conf:
        return text

    if not META_HEADING_RE.search(text):
        addition = "\n\n## Contribution Metadata\n"
        if not has_last:
            addition += f"\n- Last reviewed: {today}"
        if not has_conf:
            addition += "\n- Confidence: medium"
        addition += "\n"
        return text.rstrip() + addition

    lines = []
    if not has_last:
        lines.append(f"- Last reviewed: {today}")
    if not has_conf:
        lines.append("- Confidence: medium")
    return insert_into_section(text, META_HEADING_RE, lines)


def backfill(paths: list[Path], dry_run: bool) -> list[Path]:
    touched: list[Path] = []
    today = dt.date.today().isoformat()

    for path in paths:
        original = path.read_text(encoding="utf-8")
        updated = ensure_sources_section(original, extract_urls(original, path))
        updated = ensure_metadata_section(updated, today)
        if updated != original:
            touched.append(path)
            if not dry_run:
                path.write_text(updated, encoding="utf-8")
    return touched


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill docs metadata in priority order.")
    parser.add_argument("--limit", type=int, default=20, help="Number of files to backfill.")
    parser.add_argument("--dry-run", action="store_true", help="Show files that would be changed.")
    args = parser.parse_args()

    files = eligible_docs()
    counts = inbound_link_counts(files)

    non_compliant = [p for p in files if contract.validate_file(p)]
    non_compliant.sort(key=lambda p: (-counts[p.as_posix()], p.as_posix()))
    targets = non_compliant[: args.limit]

    touched = backfill(targets, args.dry_run)
    action = "Would update" if args.dry_run else "Updated"
    print(f"{action} {len(touched)} file(s).")
    for path in touched:
        print(path.as_posix())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
