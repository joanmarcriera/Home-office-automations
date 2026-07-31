# Contributing to the AI Hub

## What it is
The `CONTRIBUTING.md` guide is the primary governance document defining how humans and AI agents (e.g., [Claude 5.1](tools/providers/anthropic.md), GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, and Qwen 3.6) collaborate to maintain the Home-Office Automation & AI Hub. It serves as the operational manual for the repository's "KnowledgeOps" framework.

## What problem it solves
It prevents "documentation rot" and repository fragmentation by enforcing a unified taxonomy, deduplication protocols, and the **Ralph-loop** automation cycle. It ensures that every contribution—whether a tool update or a new architectural pattern—meets the "High Confidence" late October / November 2026 standard.

## Where it fits in the stack
**Governance Layer** — It sits alongside `AGENTS.md` and `standards.md` as the foundational contract for all repository activities, providing the "rules of engagement" for autonomous agents and human developers.

## Typical use cases
- **Agent Onboarding**: Establishing the "Quick Start" sequence for new LLM agents.
- **Ralph-loop Execution**: Defining how Jules (the primary agent) processes, decomposes, and closes issues.
- **Quality Assurance**: Providing the checklist for AI-authored PRs.
- **Catalog Maintenance**: Standardizing the ingestion of new sources via `docs/new-sources/`.

## Strengths
- **Agent-First Design**: Optimized for ingestion and execution by frontier models like [Claude 5.1](tools/providers/anthropic.md) and GPT-5.5.
- **Systematic Decomposition**: The Ralph-loop (Action C) allows complex technical debt to be broken into manageable batches with extracted context.
- **Multi-Agent Ready**: Supports a Federated KnowledgeOps model using MCP 3.1 for tool-use and cross-agent orchestration.

## Limitations
- **High Friction for Humans**: The strict metadata and 13-section "High Confidence" requirements can be demanding for manual contributors.
- **Script Dependency**: Relies heavily on the `scripts/` directory for validation (e.g., `audit_docs_quality.py`).

## When to use it
- Before opening a Pull Request or Issue in the AI Hub.
- When configuring a new AI agent or automation lane to work on this repository.
- During "Maintenance Runs" to verify documentation compliance and technical freshness.

## When not to use it
- For ephemeral personal notes, local-only research, or draft configurations that will not be committed to the main hub.

## Getting started

### How You Can Help
We welcome contributions from both humans and AI agents:
- **Add New Tools**: Found a tool that fits the stack? Document it using our templates.
- **Refine Playbooks**: Improve our existing automation guides with more technical detail or new variants.
- **Update Services**: Ensure the documentation for self-hosted services remains accurate as versions change.
- **Improve Prompts**: Optimize our LLM prompt templates for better extraction and classification results.

### LLM Agent Quick Start
Before changing files, agents must read these in order:
1. [AGENTS.md](../AGENTS.md) — Repository operating contract, checklists, and quality bar.
2. [skills.md](../skills.md) — Reusable task patterns for intake, docs updates, and branch hygiene.
3. [Standards](standards.md) — Taxonomy, metadata rules, and canonical-page requirements.

### The Ralph-loop Protocol
This repository implements the **Ralph-loop**, a systematic directive for AI agents (primarily **Google Jules**) to close issues by performing one of three actions:
- **Action A (Do the work)**: Implement features or perform technical freshness audits (e.g., November 2026 updates).
- **Action B (Add links)**: Find the appropriate canonical location for provided external links.
- **Action C (Decompose)**: Divide complex tasks into smaller, trackable issues with extracted context (see `docs/reports/`).

### Assigning a Task to Jules
You can request Jules to perform a task by:
1.  **Opening an Issue**: Describe the task clearly (e.g., "Add documentation for Tool X").
2.  **Adding the Label**: Apply the label `jules` (case-insensitive) to the issue.
3.  **Review the Plan**: Jules will analyze the task and post a plan as a comment. Once you approve, Jules will get to work.

### AI PR Checklist
Before requesting review, AI-authored PRs must satisfy:
- [ ] Canonical page search completed (name + aliases).
- [ ] No duplicate canonical pages introduced.
- [ ] Correct 13-section "High Confidence" template and taxonomy used.
- [ ] Required metadata added (`Last reviewed`, `Confidence`, `Sources / References`).
- [ ] At least one high-signal source URL included.
- [ ] `data/all_tools.json` and `mkdocs.yml` updated when applicable.
- [ ] `scripts/audit_docs_quality.py` and `scripts/check_docs_contract.py` pass with 100% compliance.

## CLI examples
Verify contribution quality and identify tasks using the repository's internal toolset:

```bash
# Run full technical freshness audit across the repository
python3 scripts/audit_docs_quality.py

# Verify KnowledgeOps contract for a specific file
python3 scripts/check_docs_contract.py docs/services/n8n.md

# Find oldest issues for Ralph-loop processing
python3 scripts/find_oldest_issues.py
```

## API examples

### Programmatic Contribution Metadata Validation with Pydantic v2 (Python)
An automated validator using modern Pydantic v2 syntax to enforce Contribution Metadata compliance.

```python
import sys
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class ContributionMetadata(BaseModel):
    last_reviewed: date = Field(..., description="The date of last review (YYYY-MM-DD)", alias="Last reviewed")
    confidence: Literal["high", "medium", "low"] = Field(..., description="Audit confidence level", alias="Confidence")

    @field_validator("last_reviewed")
    @classmethod
    def validate_recent_date(cls, v: date) -> date:
        if v < date(2026, 1, 1):
            raise ValueError("Review date must be within calendar year 2026 or later")
        return v

# Simulated ingestion pipeline
def check_compliance(metadata_dict: dict) -> bool:
    try:
        validated = ContributionMetadata.model_validate(metadata_dict)
        print("Metadata is compliant:", validated.model_dump(by_alias=True))
        return True
    except Exception as e:
        print("Non-compliant metadata:", e, file=sys.stderr)
        return False

# Usage
test_meta = {"Last reviewed": "2026-11-05", "Confidence": "high"}
check_compliance(test_meta)
```

### Programmatic Integration with MCP 3.1 Task Protocol
Under MCP 3.1, a verification tool standardizes reports using the Task Protocol schemas.

```python
import json
import urllib.request

def submit_standards_verification(task_id: str, file_path: str, passed: bool):
    url = "http://localhost:8000/tasks/v1/verify"
    payload = {
        "task_id": task_id,
        "step_name": f"standards-verification-{file_path}",
        "status": "passed" if passed else "failed",
        "metadata": {
            "standards_version": "2026.11",
            "enforcing_model": "Claude 5.1"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

## Related tools / concepts
- [AGENTS.md](../AGENTS.md) — Core agent contract and operating rules.
- [Standards](standards.md) — Repository taxonomy and metadata conventions.
- [Jules Agent](tools/ai_knowledge/local_llms.md) — The primary Ralph-loop executor and maintainer.
- [Multi-Agent KnowledgeOps](architecture/multi_agent_knowledgeops.md) — The federated governance model.
- [Automated Contributions](architecture/multi_agent_knowledgeops.md) — Deep dive into the Ralph-loop implementation.
- [Model Context Protocol](tools/automation_orchestration/chronos-mcp.md) — Standard for tool integration in late 2026.
- [Gemma 3](tools/ai_knowledge/local_llms.md) — Canonical local LLM guide.
- [Claude Code](tools/development_ops/claude-code-setup.md) — Recommended agentic development tool for the hub.

## Sources / references
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [KnowledgeOps Manifesto](https://github.com/joanmarcriera/Home-office-automations/blob/main/docs/architecture/multi_agent_knowledgeops.md)
- [Ralph-loop Documentation](https://github.com/joanmarcriera/Home-office-automations/blob/main/docs/architecture/multi_agent_knowledgeops.md)

---
## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
