#!/usr/bin/env python3
"""
Audit all knowledge-base markdown docs for compliance with project standards.

Checks required sections, contribution metadata, sources with URLs, and
flags legacy-format pages.  Outputs a human-readable summary report.

Exit code is always 0 — this is an informational audit, not a CI gate.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

SCAN_DIRS = (
    "docs/tools/",
    "docs/services/",
    "docs/knowledge_base/",
    "docs/playbooks/",
    "docs/architecture/",
    "docs/reference-implementations/",
)

EXCLUDED_FILENAMES = {"README.md", "index.md"}
EXCLUDED_PREFIXES = ("docs/templates/",)

REQUIRED_SECTIONS = [
    "What it is",
    "What problem it solves",
    "Where it fits in the stack",
    "Typical use cases",
    "Strengths",
    "Limitations",
    "When to use it",
    "When not to use it",
    "Related tools / concepts",
    "Sources / references",
]

# Pre-compiled patterns
HEADING_RE = re.compile(r"^##\s+", re.MULTILINE)
SOURCE_HEADER_RE = re.compile(r"^##\s*Sources\s*/\s*References\s*$", re.IGNORECASE | re.MULTILINE)
LAST_REVIEWED_RE = re.compile(r"^\s*-\s*Last reviewed:\s*\d{4}-\d{2}-\d{2}", re.IGNORECASE | re.MULTILINE)
CONFIDENCE_RE = re.compile(r"^\s*-\s*Confidence:\s*(high|medium|low)", re.IGNORECASE | re.MULTILINE)
URL_RE = re.compile(r"https?://", re.IGNORECASE)
LEGACY_DESCRIPTION_RE = re.compile(r"^##\s+Description\s*$", re.IGNORECASE | re.MULTILINE)


def _section_regex(name: str) -> re.Pattern[str]:
    """Build a case-insensitive regex that matches ``## <name>``."""
    escaped = re.escape(name)
    return re.compile(rf"^##\s*{escaped}\s*$", re.IGNORECASE | re.MULTILINE)


SECTION_PATTERNS = {name: _section_regex(name) for name in REQUIRED_SECTIONS}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _category_for(path: Path) -> str:
    """Derive a human-friendly category from a doc's path."""
    rel = path.relative_to(REPO_ROOT).as_posix()
    for scan_dir in SCAN_DIRS:
        if rel.startswith(scan_dir):
            # e.g. "docs/tools/ai_knowledge/" -> "tools/ai_knowledge"
            remainder = rel[len(scan_dir):]
            first_segment = remainder.split("/")[0] if "/" in remainder else ""
            label = scan_dir.rstrip("/")
            if first_segment:
                label = f"{label}/{first_segment}"
            return label
    return "other"


def _extract_section_body(text: str, header_match: re.Match[str]) -> str:
    start = header_match.end()
    remainder = text[start:]
    next_heading = HEADING_RE.search(remainder)
    if not next_heading:
        return remainder
    return remainder[: next_heading.start()]


def should_scan(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    if path.name in EXCLUDED_FILENAMES:
        return False
    rel = path.relative_to(REPO_ROOT).as_posix()
    if any(rel.startswith(p) for p in EXCLUDED_PREFIXES):
        return False
    return any(rel.startswith(d) for d in SCAN_DIRS)


# ---------------------------------------------------------------------------
# Per-file audit
# ---------------------------------------------------------------------------

class FileReport:
    """Audit result for a single file."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.missing_sections: list[str] = []
        self.has_metadata = True
        self.has_source_url = True
        self.is_legacy = False

    @property
    def is_compliant(self) -> bool:
        return (
            not self.missing_sections
            and self.has_metadata
            and self.has_source_url
            and not self.is_legacy
        )


def audit_file(path: Path) -> FileReport:
    report = FileReport(path)
    text = path.read_text(encoding="utf-8")

    # Required sections
    for name, pattern in SECTION_PATTERNS.items():
        if not pattern.search(text):
            report.missing_sections.append(name)

    # Contribution metadata
    if not LAST_REVIEWED_RE.search(text) or not CONFIDENCE_RE.search(text):
        report.has_metadata = False

    # Source URL check
    source_match = SOURCE_HEADER_RE.search(text)
    if source_match:
        body = _extract_section_body(text, source_match)
        if not URL_RE.search(body):
            report.has_source_url = False
    else:
        report.has_source_url = False

    # Legacy format detection
    if LEGACY_DESCRIPTION_RE.search(text):
        report.is_legacy = True

    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def collect_files() -> list[Path]:
    files: list[Path] = []
    for scan_dir in SCAN_DIRS:
        target = REPO_ROOT / scan_dir
        if not target.is_dir():
            continue
        for md_path in sorted(target.rglob("*.md")):
            if should_scan(md_path):
                files.append(md_path)
    return files


def main() -> int:
    files = collect_files()
    if not files:
        print("No eligible docs found to audit.")
        return 0

    reports: list[FileReport] = [audit_file(f) for f in files]

    # ---- Aggregate ----
    total = len(reports)
    compliant = [r for r in reports if r.is_compliant]
    legacy = [r for r in reports if r.is_legacy]
    missing_meta = [r for r in reports if not r.has_metadata]

    # Per-category breakdown
    cat_total: dict[str, int] = defaultdict(int)
    cat_compliant: dict[str, int] = defaultdict(int)
    for r in reports:
        cat = _category_for(r.path)
        cat_total[cat] += 1
        if r.is_compliant:
            cat_compliant[cat] += 1

    # ---- Report ----
    pct = (len(compliant) / total * 100) if total else 0

    print("=" * 60)
    print("  Docs Quality Audit Report")
    print("=" * 60)
    print()
    print(f"Total docs scanned:  {total}")
    print(f"Compliant:           {len(compliant)} ({pct:.1f}%)")
    print(f"Legacy-format:       {len(legacy)}")
    print(f"Missing metadata:    {len(missing_meta)}")
    print()

    if legacy:
        print("--- Legacy-format docs (have '## Description') ---")
        for r in legacy:
            print(f"  {r.path.relative_to(REPO_ROOT).as_posix()}")
        print()

    if missing_meta:
        print("--- Docs missing contribution metadata ---")
        for r in missing_meta:
            print(f"  {r.path.relative_to(REPO_ROOT).as_posix()}")
        print()

    print("--- Per-category breakdown ---")
    for cat in sorted(cat_total):
        c = cat_compliant.get(cat, 0)
        t = cat_total[cat]
        cat_pct = (c / t * 100) if t else 0
        print(f"  {cat:45s}  {c}/{t}  ({cat_pct:.0f}%)")
    print()

    # Non-compliant details
    non_compliant = [r for r in reports if not r.is_compliant]
    if non_compliant:
        print("--- Non-compliant doc details ---")
        for r in sorted(non_compliant, key=lambda r: r.path.as_posix()):
            rel = r.path.relative_to(REPO_ROOT).as_posix()
            issues: list[str] = []
            if r.missing_sections:
                issues.append(f"missing sections: {', '.join(r.missing_sections)}")
            if not r.has_metadata:
                issues.append("missing contribution metadata")
            if not r.has_source_url:
                issues.append("no URL in Sources / References")
            if r.is_legacy:
                issues.append("legacy format (## Description)")
            print(f"  {rel}")
            for issue in issues:
                print(f"    - {issue}")
        print()

    print("=" * 60)
    print("  Audit complete.")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
