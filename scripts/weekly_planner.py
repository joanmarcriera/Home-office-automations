#!/usr/bin/env python3
"""
Weekly Growth Planner

Reads data/growth-metrics.json and creates targeted GitHub issues for Jules:
1. A deepening issue: add code examples to the 5 shallowest docs
2. A gap-filling issue: discover tools for the most underdeveloped category

Runs Monday 02:00 UTC via weekly-planner.yml.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

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


def create_issue(title: str, body: str, labels: list[str]) -> bool:
    """Create a GitHub issue using gh CLI."""
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
6. Update `- Last reviewed: {_today()}` in the Contribution Metadata section

### Quality checks
- Verify: `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`
- Ensure all code examples are complete and runnable (no placeholder `...` blocks)
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

    created = 0

    # Issue 1: Deepen shallow docs
    if shallow_docs:
        body = build_deepening_body(shallow_docs)
        title = f"Weekly deepening: add code examples to {min(5, len(shallow_docs))} docs"
        if create_issue(title, body, ["jules"]):
            created += 1

    # Issue 2: Fill the most underdeveloped category
    if underdeveloped:
        # Pick the category with fewest docs
        worst = min(underdeveloped, key=lambda c: by_category.get(c, 0))
        count = by_category.get(worst, 0)
        body = build_gap_filling_body(worst, count)
        title = f"Category gap fill: expand {worst} (currently {count} docs)"
        if create_issue(title, body, ["jules"]):
            created += 1

    print(f"Created {created} issue(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
