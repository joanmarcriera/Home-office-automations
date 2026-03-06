#!/usr/bin/env python3
"""
Generate capability-capacity summary tables for the API pricing matrix page.

The script parses model rows from:
docs/knowledge_base/api_pricing_free_tiers.md

It replaces (or inserts) the block between:
<!-- BEGIN AUTO-CAPABILITY-SUMMARY -->
<!-- END AUTO-CAPABILITY-SUMMARY -->
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

DOC_PATH = Path("docs/knowledge_base/api_pricing_free_tiers.md")

BEGIN_MARKER = "<!-- BEGIN AUTO-CAPABILITY-SUMMARY -->"
END_MARKER = "<!-- END AUTO-CAPABILITY-SUMMARY -->"

CAPABILITY_ORDER = ["CODE", "VERIFY", "REASON", "LONGCTX", "FAST", "BUDGET", "OPEN"]
CAPABILITY_LABELS = {
    "CODE": "Coding",
    "VERIFY": "Verification",
    "REASON": "Reasoning",
    "LONGCTX": "Long-context",
    "FAST": "Low-latency",
    "BUDGET": "Budget/free-value",
    "OPEN": "Open-model ecosystem",
}

TAG_RE = re.compile(r'<span class="cap-tag [^"]+">([^<]+)</span>')
TOKEN_RE = re.compile(r"(\d+(?:\.\d+)?)\s*([kmb])\b", re.IGNORECASE)

UNKNOWN_HINTS = (
    "tier",
    "credit",
    "n/p",
    "not published",
    "plan",
    "model",
    "provider",
    "endpoint",
    "varies",
    "higher",
    "mo",
)


@dataclass
class ModelRow:
    provider: str
    model: str
    verification: str
    capabilities: list[str]
    daily_tokens: float | None

    @property
    def label(self) -> str:
        return f"{self.provider} — {self.model}"


def parse_token_count(value: str) -> float | None:
    raw = value.strip().lower()
    if not raw:
        return None
    if any(hint in raw for hint in UNKNOWN_HINTS):
        return None
    match = TOKEN_RE.search(raw)
    if not match:
        return None
    amount = float(match.group(1))
    suffix = match.group(2).lower()
    scale = {"k": 1_000.0, "m": 1_000_000.0, "b": 1_000_000_000.0}[suffix]
    return amount * scale


def format_token_count(value: float) -> str:
    if value >= 1_000_000_000:
        v = value / 1_000_000_000
        return f"{v:.1f}B".replace(".0B", "B")
    if value >= 1_000_000:
        v = value / 1_000_000
        return f"{v:.1f}M".replace(".0M", "M")
    if value >= 1_000:
        v = value / 1_000
        return f"{v:.1f}K".replace(".0K", "K")
    return str(int(value))


def extract_daily_cap(quotas_cell: str) -> float | None:
    parts = [p.strip() for p in quotas_cell.split(" / ")]
    if len(parts) < 5:
        parts = [p.strip() for p in quotas_cell.split("/")]
    if not parts:
        return None
    return parse_token_count(parts[-1])


def parse_model_rows(markdown: str) -> list[ModelRow]:
    lines = markdown.splitlines()
    in_model_section = False
    provider = ""
    rows: list[ModelRow] = []

    for line in lines:
        if line.startswith("## Model-level quota tracker"):
            in_model_section = True
            continue
        if in_model_section and line.startswith("## Notes and caveats"):
            break
        if not in_model_section:
            continue

        if line.startswith("### "):
            provider = line[4:].strip()
            continue

        if not line.startswith("|"):
            continue
        stripped = line.strip()
        if stripped.startswith("| :---") or stripped.startswith("| Model "):
            continue

        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue

        model, quotas, verification, summary = cells[0], cells[1], cells[2], cells[3]
        capabilities = [tag.strip().upper() for tag in TAG_RE.findall(summary)]
        if not capabilities:
            continue

        rows.append(
            ModelRow(
                provider=provider or "Unknown",
                model=model,
                verification=verification,
                capabilities=capabilities,
                daily_tokens=extract_daily_cap(quotas),
            )
        )

    return rows


def build_capability_view(rows: list[ModelRow]) -> dict[str, list[ModelRow]]:
    caps: dict[str, list[ModelRow]] = {cap: [] for cap in CAPABILITY_ORDER}
    for row in rows:
        if row.daily_tokens is None:
            continue
        for cap in row.capabilities:
            if cap in caps:
                caps[cap].append(row)
    for cap in caps:
        caps[cap].sort(key=lambda r: r.daily_tokens or 0, reverse=True)
    return caps


def render_generated_block(rows: list[ModelRow]) -> str:
    caps = build_capability_view(rows)
    shortlist_cache: dict[str, tuple[list[ModelRow], float, float]] = {}

    out: list[str] = []
    out.append(BEGIN_MARKER)
    out.append("")
    out.append("### Capability Capacity Summary (auto-generated)")
    out.append("")
    out.append(
        "These summaries are generated from the model rows on this page "
        "using `scripts/update_api_pricing_capability_summary.py`."
    )
    out.append("Only rows with a numeric daily token cap are included in the capacity math.")
    out.append("")
    out.append("#### Leaderboard By Capability (known daily token caps)")
    out.append("")
    out.append("| Capability | Top models | Highest known daily cap | Known models |")
    out.append("| :--- | :--- | :--- | :--- |")

    for cap in CAPABILITY_ORDER:
        entries = caps[cap]
        if not entries:
            out.append(f"| {CAPABILITY_LABELS[cap]} | n/a | n/a | 0 |")
            continue
        top_items = "; ".join(
            f"{e.label} ({format_token_count(e.daily_tokens or 0)})" for e in entries[:3]
        )
        highest = format_token_count(entries[0].daily_tokens or 0)
        out.append(f"| {CAPABILITY_LABELS[cap]} | {top_items} | {highest} | {len(entries)} |")

    out.append("")
    out.append("#### 80% Shortlist (known-cap coverage)")
    out.append("")
    out.append("| Capability | Models to reach >=80% of known capacity | Coverage | Total known daily cap |")
    out.append("| :--- | :--- | :--- | :--- |")

    for cap in CAPABILITY_ORDER:
        entries = caps[cap]
        if not entries:
            out.append(f"| {CAPABILITY_LABELS[cap]} | n/a | n/a | n/a |")
            shortlist_cache[cap] = ([], 0.0, 0.0)
            continue

        total = sum(e.daily_tokens or 0 for e in entries)
        threshold = total * 0.8
        selected: list[ModelRow] = []
        running = 0.0
        for entry in entries:
            selected.append(entry)
            running += entry.daily_tokens or 0
            if running >= threshold:
                break

        picks = "; ".join(f"{e.label} ({format_token_count(e.daily_tokens or 0)})" for e in selected)
        coverage = (running / total) * 100 if total > 0 else 0
        shortlist_cache[cap] = (selected, coverage, total)
        out.append(
            f"| {CAPABILITY_LABELS[cap]} | {picks} | {coverage:.1f}% | {format_token_count(total)} |"
        )

    out.append("")
    out.append("#### Fast Recommendation (80% rule, known-cap data)")
    out.append("")
    out.append("| Goal | Recommended free-first models | Why this set |")
    out.append("| :--- | :--- | :--- |")
    for cap, goal in (
        ("CODE", "Coding"),
        ("VERIFY", "Verification"),
        ("REASON", "Reasoning"),
    ):
        selected, coverage, total = shortlist_cache.get(cap, ([], 0.0, 0.0))
        if not selected:
            out.append(f"| {goal} | n/a | No numeric daily-cap data available for this capability. |")
            continue
        picks = "; ".join(e.label for e in selected)
        out.append(
            f"| {goal} | {picks} | Reaches {coverage:.1f}% of known daily capacity "
            f"({format_token_count(total)} total known). |"
        )

    out.append("")
    out.append(END_MARKER)
    return "\n".join(out)


def replace_or_insert_block(markdown: str, generated_block: str) -> str:
    if BEGIN_MARKER in markdown and END_MARKER in markdown:
        pattern = re.compile(
            rf"{re.escape(BEGIN_MARKER)}.*?{re.escape(END_MARKER)}",
            flags=re.DOTALL,
        )
        return pattern.sub(generated_block, markdown)

    anchor = "\n### Google Gemini\n"
    if anchor in markdown:
        return markdown.replace(anchor, f"\n{generated_block}\n{anchor}", 1)

    raise RuntimeError("Could not find insertion anchor `### Google Gemini` in model section.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update auto-generated capability summary tables.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if the generated block is up-to-date without writing changes.",
    )
    args = parser.parse_args()

    markdown = DOC_PATH.read_text(encoding="utf-8")
    rows = parse_model_rows(markdown)
    generated = render_generated_block(rows)
    updated = replace_or_insert_block(markdown, generated)

    if args.check:
        if markdown != updated:
            print("Capability summary block is out of date.")
            return 1
        print("Capability summary block is up to date.")
        return 0

    if markdown != updated:
        DOC_PATH.write_text(updated, encoding="utf-8")
        print(f"Updated: {DOC_PATH}")
    else:
        print("No changes required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
