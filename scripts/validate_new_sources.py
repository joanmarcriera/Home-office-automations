#!/usr/bin/env python3
"""
Validate daily new-sources intake logs.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

INDEX_PATH = Path("docs/new-sources.md")
LOG_DIR = Path("docs/new-sources")
FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
H1_RE = re.compile(r"^#\s+New Sources Log\s+[—-]\s+(\d{4}-\d{2}-\d{2})\s*$")
DATE_LINK_RE = re.compile(r"\[(\d{4}-\d{2}-\d{2})\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://", re.IGNORECASE)
REQUIRED_HEADERS = [
    "Title",
    "URL",
    "Tags",
    "Status",
    "Canonical Page",
    "Notes",
]
VALID_STATUSES = {"new", "integrated", "duplicate", "needs-more-info", "low-confidence"}


def parse_row(line: str) -> list[str]:
    if not line.strip().startswith("|"):
        return []
    content = line.strip().strip("|")
    return [col.strip() for col in content.split("|")]


def ensure_iso_date(value: str, context: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{context}: invalid ISO date `{value}`.")


def find_required_table(lines: list[str], path: Path, errors: list[str]) -> tuple[int, list[list[str]]]:
    for i, line in enumerate(lines):
        row = parse_row(line)
        if row == REQUIRED_HEADERS:
            if i + 1 >= len(lines) or not lines[i + 1].strip().startswith("|"):
                errors.append(f"{path}: table separator row missing after header.")
                return -1, []

            rows: list[list[str]] = []
            cursor = i + 2
            while cursor < len(lines):
                if not lines[cursor].strip().startswith("|"):
                    break
                parsed = parse_row(lines[cursor])
                if parsed:
                    rows.append(parsed)
                cursor += 1
            return i, rows
    errors.append(
        f"{path}: missing required table header `| {' | '.join(REQUIRED_HEADERS)} |`."
    )
    return -1, []


def validate_daily_file(path: Path, seen_urls: dict[str, Path], errors: list[str]) -> None:
    name = path.name
    if not FILENAME_RE.match(name):
        errors.append(f"{path}: filename must be YYYY-MM-DD.md.")
        return

    ensure_iso_date(name[:-3], str(path), errors)
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        errors.append(f"{path}: file is empty.")
        return

    h1_match = H1_RE.match(lines[0].strip())
    if not h1_match:
        errors.append(f"{path}: first line must be `# New Sources Log — YYYY-MM-DD`.")
    else:
        header_date = h1_match.group(1)
        if header_date != name[:-3]:
            errors.append(f"{path}: H1 date `{header_date}` does not match filename `{name[:-3]}`.")
        ensure_iso_date(header_date, str(path), errors)

    _, rows = find_required_table(lines, path, errors)
    for idx, row in enumerate(rows, start=1):
        if len(row) != len(REQUIRED_HEADERS):
            errors.append(f"{path}: row {idx} has {len(row)} columns; expected {len(REQUIRED_HEADERS)}.")
            continue

        title, url_cell, _tags, status, canonical_page, _notes = row
        if not title:
            errors.append(f"{path}: row {idx} is missing title.")

        if not URL_RE.search(url_cell):
            errors.append(f"{path}: row {idx} URL column must include an http(s) URL.")
        else:
            raw = re.sub(r"^\[.*?\]\((.*?)\)$", r"\1", url_cell).strip()
            if raw in seen_urls and seen_urls[raw] != path:
                errors.append(
                    f"{path}: row {idx} duplicates URL already present in {seen_urls[raw]}."
                )
            else:
                seen_urls[raw] = path

        status_normalized = status.strip().lower()
        if status_normalized not in VALID_STATUSES:
            errors.append(f"{path}: row {idx} has invalid status `{status}`.")

        if status_normalized in {"integrated", "duplicate"} and canonical_page in {"", "-"}:
            errors.append(
                f"{path}: row {idx} with status `{status}` must include a Canonical Page value."
            )


def validate_index(log_files: list[Path], errors: list[str]) -> None:
    if not INDEX_PATH.exists():
        errors.append(f"{INDEX_PATH}: file not found.")
        return

    text = INDEX_PATH.read_text(encoding="utf-8")
    linked_files: set[str] = set()
    for date_str, target in DATE_LINK_RE.findall(text):
        canonical_a = f"/new-sources/{date_str}"
        canonical_b = f"/new-sources/{date_str}/"
        if target not in {canonical_a, canonical_b}:
            continue
        linked_files.add(f"{date_str}.md")

    # Explicitly block the old relative link style that causes /new-sources/new-sources/ 404s.
    legacy = re.findall(r"\[\d{4}-\d{2}-\d{2}\]\(new-sources/\d{4}-\d{2}-\d{2}\.md\)", text)
    if legacy:
        errors.append(
            f"{INDEX_PATH}: use absolute links `/new-sources/YYYY-MM-DD/` in the Daily Log Files table; legacy `new-sources/YYYY-MM-DD.md` links are not allowed."
        )

    for log_file in log_files:
        if log_file.name not in linked_files:
            errors.append(f"{INDEX_PATH}: missing link to `{log_file.name}`.")

    for filename in sorted(linked_files):
        if not (LOG_DIR / filename).exists():
            errors.append(f"{INDEX_PATH}: links to missing daily file `{filename}`.")


def main() -> int:
    errors: list[str] = []
    seen_urls: dict[str, Path] = {}

    if not LOG_DIR.exists():
        errors.append(f"{LOG_DIR}: directory not found.")
        for err in errors:
            print(err)
        return 1

    log_files = sorted([p for p in LOG_DIR.glob("*.md") if p.is_file()])
    if not log_files:
        errors.append(f"{LOG_DIR}: no daily log files found.")

    for log_file in log_files:
        validate_daily_file(log_file, seen_urls, errors)

    validate_index(log_files, errors)

    if errors:
        print("New-sources validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"New-sources validation passed for {len(log_files)} daily log file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
