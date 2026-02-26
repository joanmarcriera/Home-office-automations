#!/usr/bin/env python3
"""
Digest-to-Intake Bridge

Reads the latest AI daily digest, extracts tool/library/framework mentions,
deduplicates against existing catalog, and appends new rows to today's
intake log in docs/new-sources/YYYY-MM-DD.md.

Runs daily at 01:00 UTC, one hour after the digest workflow.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DIGEST_DIR = Path("ai-daily-digest/daily")
NEW_SOURCES_DIR = Path("docs/new-sources")
NEW_SOURCES_INDEX = Path("docs/new-sources.md")
ALL_TOOLS_PATH = Path("data/all_tools.json")
SOURCE_SCORES_PATH = Path("data/source-scores.json")

MODEL_STRING = os.environ.get(
    "OPENROUTER_MODEL",
    "meta-llama/llama-3.3-70b-instruct:free,deepseek/deepseek-r1:free,qwen/qwen-2-7b-instruct:free",
)
MODELS = [m.strip() for m in MODEL_STRING.split(",")]

MAX_ITEMS_PER_DAY = 15  # cap to avoid overwhelming Jules

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_existing_urls() -> set[str]:
    """Collect all URLs already in intake logs and the tool catalog."""
    urls: set[str] = set()

    # From all_tools.json
    if ALL_TOOLS_PATH.exists():
        data = json.loads(ALL_TOOLS_PATH.read_text(encoding="utf-8"))
        for tool in data.get("tools", []):
            name_lower = tool.get("name", "").lower()
            urls.add(name_lower)

    # From existing daily logs
    for log_file in NEW_SOURCES_DIR.glob("*.md"):
        for line in log_file.read_text(encoding="utf-8").splitlines():
            match = re.search(r"https?://[^\s)]+", line)
            if match:
                urls.add(match.group(0).rstrip("|").strip())

    return urls


def load_source_scores() -> dict:
    """Load source prioritisation scores."""
    if SOURCE_SCORES_PATH.exists():
        return json.loads(SOURCE_SCORES_PATH.read_text(encoding="utf-8"))
    return {"sources": {}, "updated": ""}


def extract_links_from_digest(digest_path: Path) -> list[dict]:
    """Extract all markdown links from a digest file."""
    text = digest_path.read_text(encoding="utf-8")
    items = []
    for title, url in LINK_RE.findall(text):
        # Skip reddit discussion links and generic blog homepages
        if "/comments/" in url and "reddit.com" in url:
            # Keep reddit links — they sometimes point to tools
            pass
        items.append({"title": title.strip(), "url": url.strip()})
    return items


def classify_with_llm(items: list[dict]) -> list[dict]:
    """Call OpenRouter to classify which items are tools/frameworks/providers."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Warning: OPENROUTER_API_KEY not set; skipping LLM classification.")
        return []

    from openai import OpenAI

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    system_prompt = """You are an AI tools curator. Given a list of items from a daily AI digest,
identify ONLY items that are specific, named tools, libraries, frameworks, platforms, or providers
in the AI/LLM/ML space. Exclude: general news articles, opinion pieces, discussions, job posts,
hardware announcements without a software tool, and generic blog posts.

For each qualifying item, output a JSON array of objects:
{"title": "Tool Name", "url": "https://...", "tags": "tool, framework", "notes": "One-line description"}

Tags must be from: tool, framework, provider, paper/article, benchmark/eval, infrastructure, analysis
If nothing qualifies, return an empty array: []
Return ONLY valid JSON. No markdown wrapping."""

    items_text = "\n".join(f"- [{it['title']}]({it['url']})" for it in items)
    user_prompt = f"Classify these items:\n\n{items_text}"

    for model in MODELS:
        try:
            print(f"Classifying with {model}...")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=1500,
            )
            content = response.choices[0].message.content.strip()
            # Strip markdown code fences if present
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON parse error from {model}: {e}")
            continue
        except Exception as e:
            if "429" in str(e).lower() or "rate limit" in str(e).lower():
                print(f"Rate limited on {model}, trying next...")
                continue
            print(f"Error with {model}: {e}")
            return []

    print("All models failed.")
    return []


def prioritise(items: list[dict], scores: dict) -> list[dict]:
    """If too many items, prioritise by source score. Keep all if under threshold."""
    if len(items) <= MAX_ITEMS_PER_DAY:
        return items

    source_data = scores.get("sources", {})
    scored = []
    for item in items:
        # Try to match source from URL domain
        domain = re.search(r"https?://(?:www\.)?([^/]+)", item.get("url", ""))
        domain_key = domain.group(1) if domain else "unknown"
        score_entry = source_data.get(domain_key, {})
        source_score = score_entry.get("score", 0.5)  # new sources get 0.5
        scored.append((source_score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:MAX_ITEMS_PER_DAY]]


def format_intake_row(item: dict) -> str:
    """Format a single item as a table row matching the required schema."""
    title = item.get("title", "Unknown").replace("|", "/")
    url = item.get("url", "")
    tags = item.get("tags", "tool").replace("|", ",")
    notes = item.get("notes", "").replace("|", ",")
    return f"| {title} | [{url}]({url}) | {tags} | new | - | {notes} |"


def ensure_daily_file(date_str: str) -> Path:
    """Create or return the daily log file with required header."""
    NEW_SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    daily_path = NEW_SOURCES_DIR / f"{date_str}.md"
    if not daily_path.exists():
        daily_path.write_text(
            f"# New Sources Log — {date_str}\n\n"
            "| Title | URL | Tags | Status | Canonical Page | Notes |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- |\n",
            encoding="utf-8",
        )
    return daily_path


def update_index(date_str: str) -> None:
    """Add today's date to the index if not already present."""
    if not NEW_SOURCES_INDEX.exists():
        return

    text = NEW_SOURCES_INDEX.read_text(encoding="utf-8")
    link_marker = f"[{date_str}](/new-sources/{date_str}/)"
    if date_str in text:
        return

    # Insert a new row after the table header separator
    lines = text.splitlines()
    insert_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("| :---"):
            insert_idx = i + 1
            break

    if insert_idx is None:
        return

    new_row = f"| {date_str} | {link_marker} | 0 | 0 | Bridge auto-discovery |"
    lines.insert(insert_idx, new_row)
    NEW_SOURCES_INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Find the latest digest file
    if not DIGEST_DIR.exists():
        print(f"Digest directory {DIGEST_DIR} not found.")
        return 1

    digest_files = sorted(DIGEST_DIR.glob("*.md"), reverse=True)
    if not digest_files:
        print("No digest files found.")
        return 0

    latest_digest = digest_files[0]
    print(f"Processing digest: {latest_digest}")

    # Extract links
    raw_items = extract_links_from_digest(latest_digest)
    print(f"Extracted {len(raw_items)} links from digest.")

    if not raw_items:
        print("No links found. Nothing to do.")
        return 0

    # Classify with LLM
    classified = classify_with_llm(raw_items)
    print(f"LLM classified {len(classified)} items as tools/frameworks/providers.")

    if not classified:
        print("No qualifying items after classification.")
        return 0

    # Deduplicate against existing catalog
    existing_urls = load_existing_urls()
    new_items = []
    for item in classified:
        url = item.get("url", "")
        title_lower = item.get("title", "").lower()
        if url not in existing_urls and title_lower not in existing_urls:
            new_items.append(item)
        else:
            print(f"  Skipping duplicate: {item.get('title')}")

    print(f"{len(new_items)} new items after deduplication.")

    if not new_items:
        print("All items already exist. Nothing to add.")
        return 0

    # Prioritise if too many
    scores = load_source_scores()
    new_items = prioritise(new_items, scores)

    # Write to daily log
    daily_path = ensure_daily_file(today)
    rows = "\n".join(format_intake_row(item) for item in new_items)
    with open(daily_path, "a", encoding="utf-8") as f:
        f.write(rows + "\n")

    # Update index
    update_index(today)

    print(f"Added {len(new_items)} new items to {daily_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
