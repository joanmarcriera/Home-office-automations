#!/usr/bin/env python3
"""
Report starred GitHub repositories that are not yet represented anywhere in the repo.

This is intended as a local maintainer workflow because reading a user's stars requires
GitHub auth with user scope. It is not suitable for default CI without a personal token.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_GLOBS = [
    "docs/**/*.md",
    "data/all_tools.json",
    "mkdocs.yml",
]
AI_RE = re.compile(
    r"(?:\bai\b|\bagentic\b|\bllm\b|\bclaude\b|\bcodex\b|\bopenai\b|\banthropic\b|\bgemini\b|\bmcp\b|\brag\b|\blangchain\b|\blanggraph\b|\bcrewai\b|\bautogen\b|\bbrowser-use\b|\bflowise\b|\bmemory\b|\bcontext\b|\bmodels?\b)",
    re.IGNORECASE,
)


def run_gh_api() -> list[dict]:
    cmd = ["gh", "api", "user/starred?per_page=100", "--paginate"]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "gh api failed")
    return json.loads(result.stdout)


def load_repo_text() -> str:
    chunks: list[str] = []
    for pattern in SCAN_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            if path.is_file():
                try:
                    chunks.append(path.read_text(encoding="utf-8"))
                except UnicodeDecodeError:
                    continue
    return "\n".join(chunks)


def is_ai_repo(repo: dict) -> bool:
    text = " ".join(
        filter(
            None,
            [
                repo.get("full_name", ""),
                repo.get("description", ""),
            ],
        )
    )
    return bool(AI_RE.search(text))


def repo_known(repo: dict, corpus: str) -> bool:
    html_url = repo["html_url"]
    full_name = repo["full_name"]
    return html_url in corpus or f"https://github.com/{full_name}" in corpus


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find starred GitHub repositories not yet represented in this repo."
    )
    parser.add_argument(
        "--ai-only",
        action="store_true",
        help="Limit results to repos that look AI/agent-related based on name/description.",
    )
    parser.add_argument(
        "--min-stars",
        type=int,
        default=0,
        help="Only report repositories with at least this many stars.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of missing repos to print.",
    )
    args = parser.parse_args()

    try:
        starred = run_gh_api()
    except Exception as exc:  # noqa: BLE001
        print(f"Starred repo check failed: {exc}")
        return 1

    corpus = load_repo_text()
    missing: list[dict] = []

    for repo in starred:
        if repo.get("stargazers_count", 0) < args.min_stars:
            continue
        if args.ai_only and not is_ai_repo(repo):
            continue
        if not repo_known(repo, corpus):
            missing.append(repo)

    missing.sort(key=lambda item: item.get("stargazers_count", 0), reverse=True)

    if not missing:
        scope = "AI/agent" if args.ai_only else "starred"
        print(f"No missing {scope} repositories found.")
        return 0

    print(
        f"Missing repositories: showing {min(len(missing), args.limit)} of {len(missing)} total."
    )
    for repo in missing[: args.limit]:
        stars = repo.get("stargazers_count", 0)
        print(f"- {stars:>6}  {repo['full_name']}  {repo['html_url']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
