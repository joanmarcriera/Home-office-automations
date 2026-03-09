#!/usr/bin/env python3
"""
Monthly Reddit -> intake bridge (OpenRouter assisted).

Fetches top Reddit posts from a target subreddit, asks an OpenRouter model to
extract high-signal AI ecosystem items, and appends a bounded number of rows to
docs/new-sources/YYYY-MM-DD.md.

Designed to keep PRs small: at most two files are touched per run:
  - docs/new-sources/YYYY-MM-DD.md
  - docs/new-sources.md
"""

from __future__ import annotations

import base64
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


REPO_ROOT = Path(".")
NEW_SOURCES_DIR = REPO_ROOT / "docs" / "new-sources"
NEW_SOURCES_INDEX = REPO_ROOT / "docs" / "new-sources.md"
ALL_TOOLS_PATH = REPO_ROOT / "data" / "all_tools.json"

ALLOWED_TAGS = {
    "tool",
    "framework",
    "provider",
    "paper/article",
    "tutorial/guide",
    "benchmark/eval",
    "infrastructure",
    "analysis",
}


@dataclass
class Candidate:
    title: str
    url: str
    tags: str
    notes: str


def env_required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def strip_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def load_existing_urls() -> set[str]:
    urls: set[str] = set()
    url_re = re.compile(r"https?://[^\s)]+", re.IGNORECASE)

    if NEW_SOURCES_DIR.exists():
        for md in NEW_SOURCES_DIR.glob("*.md"):
            for match in url_re.findall(md.read_text(encoding="utf-8")):
                urls.add(match.rstrip("|").strip().lower())

    if ALL_TOOLS_PATH.exists():
        data = json.loads(ALL_TOOLS_PATH.read_text(encoding="utf-8"))
        for tool in data.get("tools", []):
            for field in ("homepage", "url", "website"):
                val = str(tool.get(field, "")).strip()
                if val.startswith("http://") or val.startswith("https://"):
                    urls.add(val.lower())

    return urls


def reddit_oauth_token() -> str:
    client_id = env_required("REDDIT_CLIENT_ID")
    client_secret = env_required("REDDIT_CLIENT_SECRET")
    user_agent = env_required("REDDIT_USER_AGENT")

    payload = urlencode({"grant_type": "client_credentials"}).encode("utf-8")
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")

    req = Request(
        "https://www.reddit.com/api/v1/access_token",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Basic {basic}",
            "User-Agent": user_agent,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    with urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    data = json.loads(body)
    token = data.get("access_token")
    if not token:
        raise RuntimeError("Could not obtain Reddit OAuth token.")
    return token


def fetch_top_posts(token: str, subreddit: str, timeframe: str, limit: int) -> list[dict[str, Any]]:
    user_agent = env_required("REDDIT_USER_AGENT")
    url = f"https://oauth.reddit.com/r/{subreddit}/top?{urlencode({'t': timeframe, 'limit': limit})}"

    req = Request(
        url,
        method="GET",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": user_agent,
        },
    )
    with urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    payload = json.loads(body)

    posts: list[dict[str, Any]] = []
    for child in payload.get("data", {}).get("children", []):
        p = child.get("data", {})
        posts.append(
            {
                "title": p.get("title", ""),
                "url": p.get("url", ""),
                "permalink": f"https://www.reddit.com{p.get('permalink', '')}",
                "selftext": p.get("selftext", ""),
                "score": p.get("score", 0),
                "comments": p.get("num_comments", 0),
                "created_utc": p.get("created_utc", 0),
            }
        )
    return posts


def select_with_openrouter(posts: list[dict[str, Any]], max_items: int) -> list[Candidate]:
    api_key = env_required("OPENROUTER_API_KEY")
    model = os.environ.get("OPENROUTER_MODEL", "").strip() or "qwen/qwen-2.5-7b-instruct:free"

    # Imported lazily to keep script import-safe without dependency pre-install.
    from openai import OpenAI

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    posts_snippet = []
    for idx, post in enumerate(posts[:40], start=1):
        title = str(post.get("title", "")).replace("\n", " ").strip()
        url = str(post.get("url", "")).strip()
        permalink = str(post.get("permalink", "")).strip()
        score = int(post.get("score", 0))
        comments = int(post.get("comments", 0))
        posts_snippet.append(
            f"{idx}. title={title} | url={url} | permalink={permalink} | score={score} | comments={comments}"
        )

    system = (
        "You curate AI tooling sources for a technical documentation repository.\n"
        "Select up to {max_items} high-signal items from Reddit post metadata.\n"
        "Prefer concrete tools/frameworks/providers and practical ecosystem resources.\n"
        "Avoid generic opinion/news-only links unless strategically important.\n"
        "Output ONLY strict JSON array objects with keys: title,url,tags,notes.\n"
        "tags must be comma-separated and use this vocabulary only: "
        "tool, framework, provider, paper/article, tutorial/guide, benchmark/eval, infrastructure, analysis.\n"
        "Each notes value must be <= 140 chars."
    ).format(max_items=max_items)

    user = "Candidate posts:\n" + "\n".join(posts_snippet)

    resp = client.chat.completions.create(
        model=model,
        temperature=0.1,
        max_tokens=1200,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    content = strip_fences(resp.choices[0].message.content or "[]")
    parsed = json.loads(content)
    if not isinstance(parsed, list):
        raise RuntimeError("OpenRouter output is not a JSON array.")

    candidates: list[Candidate] = []
    for obj in parsed[:max_items]:
        if not isinstance(obj, dict):
            continue
        title = str(obj.get("title", "")).strip()
        url = str(obj.get("url", "")).strip()
        tags = str(obj.get("tags", "")).strip().lower()
        notes = str(obj.get("notes", "")).strip()

        if not title or not (url.startswith("http://") or url.startswith("https://")):
            continue

        # Sanitize tags to allowed vocabulary.
        tag_tokens = [t.strip() for t in tags.split(",") if t.strip()]
        filtered = [t for t in tag_tokens if t in ALLOWED_TAGS]
        if not filtered:
            filtered = ["analysis"]
        tags_clean = ", ".join(filtered[:3])

        candidates.append(Candidate(title=title, url=url, tags=tags_clean, notes=notes[:140]))

    return candidates


def ensure_daily_file(date_str: str) -> Path:
    NEW_SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    path = NEW_SOURCES_DIR / f"{date_str}.md"
    if not path.exists():
        path.write_text(
            f"# New Sources Log — {date_str}\n\n"
            "| Title | URL | Tags | Status | Canonical Page | Notes |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- |\n",
            encoding="utf-8",
        )
    return path


def append_daily_rows(path: Path, items: list[Candidate]) -> None:
    lines = []
    for it in items:
        title = it.title.replace("|", "/")
        notes = it.notes.replace("|", "/").replace("\n", " ")
        row = f"| {title} | [{it.url}]({it.url}) | {it.tags} | new | - | {notes} |"
        lines.append(row)
    with path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def upsert_index_row(date_str: str, added_count: int) -> None:
    if not NEW_SOURCES_INDEX.exists():
        raise RuntimeError(f"Missing index file: {NEW_SOURCES_INDEX}")

    text = NEW_SOURCES_INDEX.read_text(encoding="utf-8")
    lines = text.splitlines()

    row_prefix = f"| {date_str} |"
    row_notes = "Monthly Reddit OpenClaw intake"
    found = False

    for i, line in enumerate(lines):
        if line.startswith(row_prefix):
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            # Date | Log File | New | Integrated | Notes
            if len(cols) >= 5:
                try:
                    current_new = int(cols[2])
                except ValueError:
                    current_new = 0
                try:
                    integrated = int(cols[3])
                except ValueError:
                    integrated = 0
                link = cols[1]
                lines[i] = (
                    f"| {date_str} | {link} | {current_new + added_count} | {integrated} | {row_notes} |"
                )
                found = True
                break

    if not found:
        insert_idx = None
        for i, line in enumerate(lines):
            if line.strip().startswith("| :---"):
                insert_idx = i + 1
                break
        if insert_idx is None:
            raise RuntimeError("Could not find Daily Log Files table header separator in index.")
        lines.insert(
            insert_idx,
            f"| {date_str} | [{date_str}](/new-sources/{date_str}/) | {added_count} | 0 | {row_notes} |",
        )

    NEW_SOURCES_INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    subreddit = os.environ.get("REDDIT_SUBREDDIT", "openclaw").strip()
    timeframe = os.environ.get("REDDIT_TIMEFRAME", "month").strip()
    post_limit = int(os.environ.get("REDDIT_POST_LIMIT", "60"))
    max_items = int(os.environ.get("MAX_INTAKE_ITEMS", "5"))

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        token = reddit_oauth_token()
        posts = fetch_top_posts(token, subreddit=subreddit, timeframe=timeframe, limit=post_limit)
    except Exception as exc:
        print(f"Failed to fetch Reddit posts: {exc}")
        return 1

    if not posts:
        print("No posts returned from Reddit.")
        return 0

    try:
        selected = select_with_openrouter(posts, max_items=max_items)
    except Exception as exc:
        print(f"OpenRouter selection failed: {exc}")
        return 1

    if not selected:
        print("No candidate items selected.")
        return 0

    existing_urls = load_existing_urls()
    deduped: list[Candidate] = []
    seen_run: set[str] = set()
    for item in selected:
        u = item.url.lower()
        if u in existing_urls or u in seen_run:
            continue
        seen_run.add(u)
        deduped.append(item)

    if not deduped:
        print("All selected items are already present.")
        return 0

    deduped = deduped[:max_items]
    daily_path = ensure_daily_file(today)
    append_daily_rows(daily_path, deduped)
    upsert_index_row(today, added_count=len(deduped))

    print(f"Added {len(deduped)} monthly Reddit intake items to {daily_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
