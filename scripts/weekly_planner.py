#!/usr/bin/env python3
"""
Weekly Growth Planner

Reads data/growth-metrics.json and creates targeted GitHub issues for Jules:
1. A deepening issue: add code examples to the 5 shallowest docs
2. A gap-filling issue: discover tools for the most underdeveloped category

Runs on days 1,7,13,19,25 of the month via weekly-planner.yml, chained from
odd-day-pipeline.yml.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from render_issue_template import run_date_banner, utc_today

METRICS_PATH = Path("data/growth-metrics.json")

# Category display names and search hints for gap-filling
CATEGORY_HINTS = {
    "frameworks": "LLM application frameworks (Haystack, Semantic Kernel, Spring AI, DSPy, etc.)",
    "providers": "LLM API providers (Anthropic, Cohere, Mistral, Together AI, Fireworks, Groq, etc.)",
    "agents": "AI agent frameworks (AutoGen, CrewAI, LangGraph, Smolagents, Agency Swarm, etc.)",
    "orchestration": "AI workflow orchestration (Temporal, Prefect, Dagster, Airflow ML, etc.)",
    "infrastructure": "LLM inference infrastructure (vLLM, TGI, SGLang, ExLlamaV2, Aphrodite, etc.)",
    "benchmarking": "AI evaluation (MMLU, HellaSwag, TruthfulQA, BigBench, AgentBench, etc.)",
    "ai_knowledge": "AI knowledge tools (Notion AI, Mem, Khoj, Quivr, AnythingLLM, etc.)",
    "process_understanding": "Document processing (Unstructured, Docling, Marker, Surya, etc.)",
}


# Identity this lane creates its issues with (GITHUB_TOKEN). Only issues from it
# count for dedupe: titles and labels of issues opened by anyone else are not
# trusted, otherwise an outsider could open "Weekly deepening: ..." and
# suppress the lane.
TRUSTED_AUTHOR = "app/github-actions"  # login as gh prints it in --json output
# Login as `gh issue list --author` must receive it: without --search/--label,
# gh filters with GraphQL createdBy, where "app/github-actions" silently matches
# NOTHING (so dedupe never fired); "github-actions[bot]" works on every path.
TRUSTED_AUTHOR_QUERY = "github-actions[bot]"
LOOKUP_LIMIT = 200

# Exit code when the dedupe lookup failed and issue creation was skipped. The
# lane step fails (so the watchdog sees and reruns it) after the rollup PR step
# has already run — non-fatal for the rest of the pipeline.
EXIT_LOOKUP_FAILED = 2


class LookupFailed(RuntimeError):
    """The open-issue lookup could not be trusted; do not create anything."""


def open_bot_issue_titles() -> list[str]:
    """Titles of open issues created by this lane's own bot identity.

    Fails CLOSED: any API error, unparsable or unexpected output, or a
    possibly-truncated result raises LookupFailed instead of returning [] —
    "unknown" must never be read as "nothing open, go ahead and create".
    """
    result = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--author", TRUSTED_AUTHOR_QUERY,
         "--limit", str(LOOKUP_LIMIT), "--json", "title,author"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise LookupFailed(f"gh issue list failed: {result.stderr.strip()[:300]}")
    try:
        issues = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise LookupFailed(f"unparsable gh output: {exc}") from exc
    if not isinstance(issues, list):
        raise LookupFailed("unexpected gh output (not a list)")
    if len(issues) >= LOOKUP_LIMIT:
        raise LookupFailed(f"{len(issues)} open bot issues — result may be truncated")
    titles = []
    for issue in issues:
        if not isinstance(issue, dict) or not isinstance(issue.get("title"), str):
            raise LookupFailed("unexpected issue record in gh output")
        # Defence in depth: keep only records really authored by the bot.
        if (issue.get("author") or {}).get("login") == TRUSTED_AUTHOR:
            titles.append(issue["title"])
    return titles


def already_open(titles: list[str], title_prefix: str) -> bool:
    return any(t.startswith(title_prefix) for t in titles)


def create_issue(title: str, body: str, labels: list[str]) -> bool:
    """Create a GitHub issue using gh CLI (body gets the run-date banner)."""
    body = run_date_banner(utc_today()) + "\n" + body
    cmd = ["gh", "issue", "create", "--title", title, "--body", body]
    for label in labels:
        cmd.extend(["--label", label])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Created issue: {result.stdout.strip()}")
        return True
    else:
        print(f"Failed to create issue: {result.stderr}")
        return False


def build_deepening_body(shallow_docs: list[str]) -> str:
    """Build the issue body for doc deepening."""
    targets = shallow_docs[:5]
    file_list = "\n".join(f"- `{doc}`" for doc in targets)

    return f"""## Weekly Doc Deepening

> **Important**: Do NOT update `Last reviewed` dates or `Confidence` metadata unless you are also making substantive content changes to that file. The CI gate will reject PRs that only change metadata.

The following {len(targets)} docs are the shallowest in the knowledge base and need practical content added.

### Target docs
{file_list}

### Instructions
For each doc above:
1. Read the tool's official website/GitHub from its **Sources / References** section
2. Add a `## Getting started` section after `## When not to use it` with:
   - Installation command (`pip install`, `npm install`, `docker pull`, or equivalent)
   - A minimal working example in a fenced code block (Python, CLI, or config as appropriate)
3. If the tool has a CLI, add `## CLI examples` with 2-3 common commands
4. If the tool has an API/SDK, add `## API examples` with a Python or curl snippet
5. Keep all existing content unchanged
6. Ensure all code examples are **complete and runnable** — no placeholder `...` blocks

### Quality checks
- Verify: `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`
- Validate sources: `python3 scripts/validate_new_sources.py`
"""


def build_gap_filling_body(category: str, current_count: int) -> str:
    """Build the issue body for category gap filling."""
    hints = CATEGORY_HINTS.get(category, f"tools in the {category} category")

    return f"""## Category Gap Fill: {category}

The **{category}** category currently has only **{current_count} docs**, making it underdeveloped.

### Instructions
1. Research and identify **up to 8 tools** that belong in this category. Consider: {hints}
2. For each tool, create a doc using `docs/templates/tool_template.md`
3. Place in `docs/tools/{category}/`
4. Add to `data/all_tools.json` and `mkdocs.yml` navigation
5. Add an intake row to today's `docs/new-sources/YYYY-MM-DD.md` with `Status: integrated`
6. Do NOT create stub pages — every doc must have substantive content in all required sections

### Deduplication
Before creating any page, search the repo for the tool name and common aliases.
If it already exists elsewhere, update the existing page instead.

### Quality checks
- Verify: `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`
- Run: `python3 scripts/validate_new_sources.py`
"""


def _today() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def main() -> int:
    if not METRICS_PATH.exists():
        print(f"{METRICS_PATH} not found. Run growth_tracker.py first.")
        return 1

    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    shallow_docs = metrics.get("shallow_docs", [])
    underdeveloped = metrics.get("underdeveloped_categories", [])
    by_category = metrics.get("by_category", {})

    try:
        open_titles = open_bot_issue_titles()
    except LookupFailed as exc:
        print(f"::warning::Weekly planner skipped issue creation: open-issue lookup "
              f"failed ({exc}). Not creating anything to avoid duplicates.")
        return EXIT_LOOKUP_FAILED

    created = 0

    # Issue 1: Deepen shallow docs
    if shallow_docs and already_open(open_titles, "Weekly deepening:"):
        print("An open 'Weekly deepening:' issue already exists. Skipping.")
    elif shallow_docs:
        body = build_deepening_body(shallow_docs)
        title = f"Weekly deepening: add code examples to {min(5, len(shallow_docs))} docs"
        if create_issue(title, body, ["jules"]):
            created += 1

    # Issue 2: Fill the most underdeveloped category
    if underdeveloped and already_open(open_titles, "Category gap fill:"):
        print("An open 'Category gap fill:' issue already exists. Skipping.")
    elif underdeveloped:
        # Pick the category with fewest docs
        worst = min(underdeveloped, key=lambda c: by_category.get(c, 0))
        count = by_category.get(worst, 0)
        body = build_gap_filling_body(worst, count)
        title = f"Category gap fill: expand {worst} (currently {count} docs)"
        if create_issue(title, body, ["jules"]):
            created += 1

    # Issue 3: Cross-link report
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from cross_link_report import load_tool_pages, scan_for_unlinked, create_issue as create_crosslink_issue

    tools = load_tool_pages()
    if already_open(open_titles, "Weekly cross-link fix:"):
        print("An open 'Weekly cross-link fix:' issue already exists. Skipping.")
    elif tools:
        mentions = scan_for_unlinked(tools)
        if mentions:
            if create_crosslink_issue(mentions):
                created += 1

    print(f"Created {created} issue(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
