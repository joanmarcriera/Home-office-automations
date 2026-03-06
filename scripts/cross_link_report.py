#!/usr/bin/env python3
"""
Cross-Link Report

Scans all Markdown files under docs/ for mentions of tool names (from
data/all_tools.json) that are NOT hyperlinked to their canonical page.
Creates a GitHub issue for Jules with the top 20 unlinked mentions.

Runs weekly via weekly-planner.yml.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ALL_TOOLS_PATH = Path("data/all_tools.json")
DOCS_DIR = Path("docs")
TEMPLATE_PATH = Path(".github/issue-templates/weekly-cross-link-fix.md")
MAX_MENTIONS = 20


def load_tool_pages() -> dict[str, str]:
    """Return {tool_name_lower: relative_path} for all catalogued tools."""
    if not ALL_TOOLS_PATH.exists():
        return {}
    data = json.loads(ALL_TOOLS_PATH.read_text(encoding="utf-8"))
    tools = {}
    for tool in data.get("tools", []):
        name = tool.get("name", "").strip()
        page = tool.get("page", "").strip()
        if name and page:
            tools[name.lower()] = page
    return tools


def scan_for_unlinked(tools: dict[str, str]) -> list[dict]:
    """Find mentions of tool names that lack a markdown link."""
    unlinked: list[dict] = []

    # Build regex: match tool name NOT inside []() markdown link syntax
    # We look for the name as a whole word, then check it's not already linked
    link_pattern = re.compile(r"\[([^\]]*)\]\([^)]*\)")

    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        if md_file.name in ("index.md", "README.md"):
            continue
        rel_path = str(md_file)
        text = md_file.read_text(encoding="utf-8")

        # Extract all linked text so we can skip already-linked mentions
        linked_texts = set()
        for match in link_pattern.finditer(text):
            linked_texts.add(match.group(1).lower())

        for tool_name, tool_page in tools.items():
            # Don't flag a tool's own page
            if tool_page and rel_path.endswith(tool_page.lstrip("/")):
                continue

            # Case-insensitive whole-word search
            pattern = re.compile(r"\b" + re.escape(tool_name) + r"\b", re.IGNORECASE)
            for match in pattern.finditer(text):
                matched_text = match.group(0)
                # Skip if this exact text is already inside a link
                if matched_text.lower() in linked_texts:
                    continue
                # Skip if inside a code block (rough check: count ``` before match)
                prefix = text[: match.start()]
                if prefix.count("```") % 2 == 1:
                    continue

                unlinked.append(
                    {
                        "file": rel_path,
                        "tool": tool_name,
                        "page": tool_page,
                        "line": text[: match.start()].count("\n") + 1,
                    }
                )
                break  # One mention per tool per file is enough

        if len(unlinked) >= MAX_MENTIONS * 3:
            break  # Enough candidates

    # Deduplicate and cap
    seen = set()
    deduped = []
    for item in unlinked:
        key = (item["file"], item["tool"])
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped[:MAX_MENTIONS]


def create_issue(mentions: list[dict]) -> bool:
    """Create a GitHub issue with the unlinked mentions list."""
    if not mentions:
        print("No unlinked mentions found. Skipping issue creation.")
        return False

    lines = []
    for m in mentions:
        lines.append(
            f"- `{m['file']}` line {m['line']}: **{m['tool']}** → link to `{m['page']}`"
        )
    mention_list = "\n".join(lines)

    # Read template and fill in the generated list
    if TEMPLATE_PATH.exists():
        body = TEMPLATE_PATH.read_text(encoding="utf-8")
        body = body.replace(
            "<!-- GENERATED_LIST: scripts/cross_link_report.py fills this section -->",
            mention_list,
        )
    else:
        body = f"## Weekly Cross-Link Fix\n\n{mention_list}"

    from datetime import datetime, timezone

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = f"Weekly cross-link fix: {len(mentions)} unlinked tool mentions ({today})"

    cmd = [
        "gh",
        "issue",
        "create",
        "--title",
        title,
        "--body",
        body,
        "--label",
        "jules",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Created issue: {result.stdout.strip()}")
        return True
    else:
        print(f"Failed to create issue: {result.stderr}")
        return False


def main() -> int:
    tools = load_tool_pages()
    if not tools:
        print("No tools found in catalog. Skipping.")
        return 0

    print(f"Scanning docs for unlinked mentions of {len(tools)} tools...")
    mentions = scan_for_unlinked(tools)
    print(f"Found {len(mentions)} unlinked mentions.")

    if os.environ.get("DRY_RUN"):
        for m in mentions:
            print(f"  {m['file']}:{m['line']} — {m['tool']} → {m['page']}")
        return 0

    create_issue(mentions)
    return 0


if __name__ == "__main__":
    sys.exit(main())
