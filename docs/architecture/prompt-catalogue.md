# Prompt & Automation Catalogue

## What it is

The Prompt & Automation Catalogue is the central repository for every LLM prompt, GitHub Action workflow, and autonomous script used to keep this repository growing. As of early January 2027, it includes specialized system prompts for multi-agent KnowledgeOps, automated quality audits, and Model Context Protocol (FastMCP 3.1) Task Protocol compliance matrices.

## What problem it solves

Autonomous systems can often feel like "black boxes." This catalogue solves the problem of opacity by documenting the exact logic, schedules, and instructions used by agents like [Jules](../tools/ai_knowledge/jules.md). It allows for easier debugging, auditing of AI-generated content, and systematic tuning of prompt performance over time.

## Where it fits in the stack

**Category**: Architecture / Governance. It sits in the **metacognition and orchestration** layer, documenting the workflows that manage all other content in the repository.

## Typical use cases

- **Prompt Versioning**: Tracking changes to the system prompts used by the [Daily Jules Maintenance](#ga-3-daily-jules-maintenance) workflow.
- **Workflow Auditing**: Reviewing the schedule and logic of recurring GitHub Actions like the [Daily AI Digest](#ga-1-daily-ai-digest).
- **Agent Onboarding**: Providing a clear set of instructions and "mission statements" for new autonomous workers added to the repo.
- **Troubleshooting**: Identifying why a particular automated task failed by examining its input prompts and execution rules.

## Strengths

- **Transparency**: Makes the repository's automated processes understandable to human contributors.
- **Reproducibility**: Provides the exact prompts needed to replicate the automated workflows in other environments.
- **Centralization**: Collects disparate GitHub Actions and local scripts into a single, searchable document.
- **Standardization**: Enforces the use of "High Confidence" documentation standards across all automated outputs.

## Limitations

- **Maintenance Overhead**: Requires manual updates whenever a workflow or prompt is changed in the underlying code.
- **Complexity**: As the number of agents and workflows grows, the catalogue can become difficult to navigate.
- **Sensitivity**: Some prompts may contain logic that is specific to the current repository structure.

## When to use it

- When you need to understand *how* the repository is being maintained automatically.
- When you are designing a new automated workflow and want to ensure it follows existing patterns.
- During quality audits to verify that agents are operating within their defined "Allowed scope."

## When not to use it

- For documenting tool-specific features that are already covered in their respective canonical pages.
- For storing API keys or other secrets.

## Getting started

To use the catalogue, identify the automation type (Recurring GA, One-Shot Jules, or Recurring Jules) and locate its mission statement and prompt logic below.

### Overview

| ID | Name | Runner | Cadence | Type |
| :--- | :--- | :--- | :--- | :--- |
| **GA-1** | [Daily AI Digest](#ga-1-daily-ai-digest) | GitHub Actions | 2×/day | Recurring |
| **GA-2** | [Digest → Intake Bridge](#ga-2-digest-intake-bridge) | GitHub Actions + OpenRouter LLM | 2×/day | Recurring |
| **GA-3** | [Daily Jules Maintenance](#ga-3-daily-jules-maintenance) | GitHub Actions → Jules | 2×/day | Recurring |
| **GA-4** | [Weekly Growth Planner](#ga-4-weekly-growth-planner) | GitHub Actions → Jules | 2×/week | Recurring |
| **J-1** | [Fill Infrastructure Category](#j-1-fill-infrastructure-category) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-2** | [Fill Frameworks Category](#j-2-fill-frameworks-category) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-3** | [Fill Providers Category](#j-3-fill-providers-category) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-4** | [Fill Agents Category](#j-4-fill-agents-category) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-5** | [Add Code Examples (Batch 1)](#j-5-add-code-examples-batch-1) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-6** | [Add Code Examples (Batch 2)](#j-6-add-code-examples-batch-2) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-7** | [Essential Reading List](#j-7-essential-reading-list) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-8** | [RAG Pattern Deep Dive](#j-8-rag-pattern-deep-dive) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-9** | [MCP & Tool-Calling Pattern](#j-9-mcp-tool-calling-pattern) | Jules scheduled task | Once (Day 1) | One-shot |
| **J-10** | [Landscape Overview](#j-10-landscape-overview) | Jules scheduled task | Once (Day 1) | One-shot |
| **JR-1** | [Daily Intake Processing](#jr-1-daily-intake-processing) | Jules scheduled task | Daily | Recurring |
| **JR-2** | [Weekly Doc Deepening](#jr-2-weekly-doc-deepening) | Jules scheduled task | Weekly (Mon) | Recurring |
| **JR-3** | [Weekly Cross-Linking](#jr-3-weekly-cross-linking) | Jules scheduled task | Weekly (Mon) | Recurring |
| **JR-4** | [Monthly Landscape Refresh](#jr-4-monthly-landscape-refresh) | Jules scheduled task | Monthly (1st) | Recurring |
| **JR-5** | [Monthly Quality Audit](#jr-5-monthly-quality-audit) | Jules scheduled task | Monthly (1st) | Recurring |

---

## GitHub Actions — Recurring Workflows

### GA-1: Daily AI Digest

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/daily-digest.yml` |
| **Schedule** | `0 0 * * *` and `0 12 * * *` (00:00 & 12:00 UTC) |
| **Secrets** | `OPENROUTER_API_KEY` |
| **What it does** | Fetches RSS feeds from `ai-daily-digest/sources.yaml`, summarises new items via OpenRouter, and writes a digest to `ai-daily-digest/daily/YYYY-MM-DD.md`. Commits and pushes to `main`. |

---

### GA-2: Digest-Intake Bridge

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/digest-to-intake.yml` |
| **Schedule** | `0 1 * * *` and `0 13 * * *` (01:00 & 13:00 UTC) |
| **Script** | `scripts/digest_to_intake.py` |
| **Secrets** | `OPENROUTER_API_KEY` |
| **Models** | Llama 4 400B → Claude 5.1 → GPT-5.5 → Gemini 4.0 Pro → Qwen 3.8 (fallback chain) |

#### LLM System Prompt (FastMCP 3.1 & Early January 2027 Compatible)

```text
You are an AI tools curator. Given a list of items from a daily AI digest,
identify ONLY items that are specific, named tools, libraries, frameworks,
platforms, or providers in the AI/LLM/ML space. Exclude: general news
articles, opinion pieces, discussions, job posts, hardware announcements
without a software tool, and generic blog posts.

For each qualifying item, output a JSON array of objects following the FastMCP 3.1 schema:
{
  "title": "Tool Name",
  "url": "https://...",
  "tags": "tool, framework",
  "notes": "One-line description of capabilities and frontier compatibility"
}

Tags must be from: tool, framework, provider, paper/article,
benchmark/eval, infrastructure, analysis

If nothing qualifies, return an empty array: []
Return ONLY valid JSON. No markdown wrapping.
```

---

### GA-3: Daily Jules Maintenance

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/daily-jules-maintenance.yml` |
| **Schedule** | `0 7 * * *` and `0 19 * * *` (07:00 & 19:00 UTC) |
| **Issue template** | `.github/issue-templates/daily-jules-maintenance.md` |

#### Full Issue Prompt (Early January 2027 Version)

```markdown
## Daily Maintenance Run - @jules

This is an automated daily maintenance task. Please complete the steps
below **in order**, stopping at the first step that produces meaningful
work. Do not attempt all three steps in a single PR. Optimize reasoning
using frontier capabilities (Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.8, Gemini 4.0 Pro).

---

### Step 1 - Process the intake queue

Use the daily inbox format:
- index file: `docs/new-sources.md`
- daily logs: `docs/new-sources/YYYY-MM-DD.md`
- index links format: `/new-sources/YYYY-MM-DD/`

Find all rows with `Status` = `new` across daily logs.

For each row:
1. Check `data/all_tools.json`, `docs/tools/`, and `docs/services/` for existing page.
2. Classify the entry using the tags in `docs/standards.md`.
3. Create the page using templates.
4. Add to `data/all_tools.json` and `mkdocs.yml` nav.
5. Mark the row as `integrated`.

---

### Step 2 - Doc quality audit (only if Step 1 found nothing to do)

Find up to **3 tool docs** in `docs/tools/` that are missing one or
more sections or lack early January 2027 SOTA context.

---

### Step 3 - Broken internal links (only if Steps 1 and 2 found nothing)

Scan all Markdown files in `docs/` for internal links. Fix or remove broken ones automatically.
```

---

### GA-4: Weekly Growth Planner

| | |
| :--- | :--- |
| **Workflow** | `.github/workflows/weekly-planner.yml` |
| **Schedule** | `0 2 * * 1` and `0 2 * * 4` (Monday & Thursday 02:00 UTC) |
| **Script** | `scripts/weekly_planner.py` |

---

## Jules Scheduled Tasks — One-Shot (Day 1 Seed)

### J-1 to J-10: Seeding Prompts
These prompts (J-1 to J-10) are used to rapidly seed the knowledge base with infrastructure, frameworks, providers, agents, and code examples. Each prompt defines a specific set of tools and target directories.

---

## Jules Scheduled Tasks — Recurring

### JR-1: Daily Intake Processing
```text
Open the most recent file in docs/new-sources/ and process all rows
with Status: new. Create tool docs, update catalog, and mkdocs.yml.
```

### JR-2: Weekly Doc Deepening
```text
Read data/growth-metrics.json and find the shallow_docs list. Add
Getting started, CLI, and API examples to the 5 shortest docs.
```

### JR-3: Weekly Cross-Linking
```text
Scan all tool docs in docs/tools/ and add 3-5 related tools to the
## Related tools / concepts section.
```

### JR-4: Monthly Landscape Refresh
```text
Update docs/knowledge_base/landscape-overview.md with current tool
counts, most-connected tools, and new additions.
```

### JR-5: Monthly Quality Audit
```text
Run CI checks and scan for empty sections or broken links.
```

## CLI examples
Automations can be triggered or inspected using the GitHub CLI (`gh`).

```bash
# Trigger the Daily AI Digest workflow manually
gh workflow run daily-digest.yml

# List recent runs of the Daily Jules Maintenance workflow
gh run list --workflow daily-jules-maintenance.yml

# View the log for a specific workflow run
gh run view <run-id> --log
```

## API examples
Workflows can be triggered programmatically via the GitHub API.

```python
import requests

# Example: Triggering a repository dispatch event to start an automation
def trigger_workflow(token, owner, repo, event_type):
    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"event_type": event_type}
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

# trigger_workflow("YOUR_TOKEN", "joanmarcriera", "Home-office-automations", "daily-audit")
```

### Prompt & Tool Configuration Validation (Pydantic v2)
The following Python script defines and validates complex system prompts and tools registry items for Multi-Agent KnowledgeOps workflows:

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, HttpUrl

class CatalogueTool(BaseModel):
    title: str = Field(..., min_length=2)
    url: HttpUrl
    tags: List[str]
    notes: str = Field(..., max_length=500)

class PromptConfiguration(BaseModel):
    workflow_id: str
    target_models: List[str] = Field(..., min_items=1)
    system_prompt: str = Field(..., min_length=20)
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    tools: List[CatalogueTool] = Field(default_factory=list)

class PromptCatalogueRegistry(BaseModel):
    version: str = Field(..., pattern="^v\\d+\\.\\d+$")
    catalogue: Dict[str, PromptConfiguration]

# Self-validation example
if __name__ == "__main__":
    test_registry = {
        "version": "v3.1",
        "catalogue": {
            "GA-2": {
                "workflow_id": "digest-to-intake",
                "target_models": ["Claude-5.1", "GPT-5.5", "Gemini-4.0-Pro"],
                "system_prompt": "You are an AI tools curator. Given a list of items...",
                "temperature": 0.1,
                "tools": [
                    {
                        "title": "Tavily",
                        "url": "https://tavily.com",
                        "tags": ["provider", "search"],
                        "notes": "Direct search tool with FastMCP integration."
                    }
                ]
            }
        }
    }

    validated_registry = PromptCatalogueRegistry.model_validate(test_registry)
    print(f"Catalogue verified successfully! Schema version: {validated_registry.version}")
```

## Related tools / concepts

- [Jules](../tools/ai_knowledge/jules.md)
- [Multi-Agent KnowledgeOps](multi_agent_knowledgeops.md)
- [Automated Contributions](automated_contributions.md)
- [GitHub Actions](https://github.com/features/actions)
- [OpenRouter](../tools/ai_knowledge/openrouter.md)
- [Standards & Conventions](../../standards-and-conventions.md)
- [RAG Pattern](../knowledge_base/patterns/rag-pattern.md)
- [MCP](../knowledge_base/patterns/data-copilot-mcp-tooling.md)

## Sources / References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Automated Contributions (Jules setup)](automated_contributions.md)
- [Multi-Agent KnowledgeOps Governance](multi_agent_knowledgeops.md)

## Contribution Metadata

- Last reviewed: 2027-01-05
- Confidence: high
