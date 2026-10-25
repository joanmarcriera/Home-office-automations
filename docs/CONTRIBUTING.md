# Contributing to the AI Hub

## What it is
The `CONTRIBUTING.md` guide is the primary governance document defining how humans and AI agents (e.g., [Claude 5.6](tools/providers/anthropic.md), GPT-5.6, [Gemini](tools/ai_knowledge/gemini.md) 4.0 Pro/Ultra, [DeepSeek](tools/providers/deepseek.md)-V4, [Llama 4](tools/ai_knowledge/llama-4.md), [Gemma](tools/ai_knowledge/gemma.md) 4, and Qwen 3.8) collaborate to maintain the Home-Office Automation & AI Hub. It serves as the operational manual for the repository's "KnowledgeOps" framework in early January 2027.

Under this framework, contributions are processed continuously by autonomous agent loops (**Ralph-loop**) as well as human developers. The guide specifies strict taxonomy alignment, metadata schema compliance, tool registry synchronizations (`data/all_tools.json`), and navigation menu integration (`mkdocs.yml`).

## What problem it solves
It prevents "documentation rot" and repository fragmentation by enforcing a unified taxonomy, deduplication protocols, and the **Ralph-loop** automation cycle. It ensures that every contribution—whether a tool update or a new architectural pattern—meets the "High Confidence" early January 2027 State-of-the-Art standard.

Specifically, `CONTRIBUTING.md` eliminates:
- **Canonical Fragmentation**: Prevents multiple pages from documenting the same tool under slight name variations (e.g., `whisper` vs `openai-whisper`).
- **Metadata Drift**: Guarantees that metadata schemas (`Last reviewed`, `Confidence`, `Sources / references`) remain structurally valid for automated ingestion and RAG chunk indexing.
- **Unverified PR Merges**: Enforces mandatory quality audit scripts (`audit_docs_quality.py`, `check_docs_contract.py`, `check_catalog_consistency.py`, `validate_new_sources.py`) prior to branch merge.
- **Task Overwhelm**: Provides clear guidelines for Action C task decomposition when complex issues require splitting into smaller sub-tasks.

## Where it fits in the stack
**Governance Layer** — It sits alongside `AGENTS.md` and `standards.md` as the foundational contract for all repository activities, providing the "rules of engagement" for autonomous agents and human developers.

```
+-----------------------------------------------------------------------------------+
|                            KNOWLEDGEOPS GOVERNANCE LAYER                          |
|                                                                                   |
|   +-----------------------+   +------------------------+   +------------------+   |
|   |       AGENTS.md       |   |    CONTRIBUTING.md     |   |   standards.md   |   |
|   | (Agent Directives)    |   |  (Governance Workflow) |   | (Taxonomy Rules) |   |
|   +-----------+-----------+   +-----------+------------+   +--------+---------+   |
+---------------+---------------------------+-------------------------+-------------+
                |                           |                         |
                v                           v                         v
+-----------------------------------------------------------------------------------+
|                             RALPH-LOOP EXECUTION ENGINE                           |
|                                                                                   |
|   +-----------------------+   +------------------------+   +------------------+   |
|   | Action A: Implementation| | Action B: Link Mapping |   | Action C: Task   |   |
|   | & Freshness Auditing  | | & Catalog Alignment     |   | Decomposition    |   |
|   +-----------+-----------+   +-----------+------------+   +--------+---------+   |
+---------------+---------------------------+-------------------------+-------------+
                |                           |                         |
                v                           v                         v
+-----------------------------------------------------------------------------------+
|                             AUTOMATED QUALITY GATES                               |
|                                                                                   |
|   [audit_docs_quality.py] --> [check_docs_contract.py] --> [validate_new_sources.py]|
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Agent Onboarding**: Establishing the "Quick Start" sequence for new LLM agents and multi-agent orchestrators.
- **Ralph-loop Execution**: Defining how Jules (the primary agent) processes, decomposes, and closes repository issues.
- **Quality Assurance**: Providing the checklist for AI-authored PRs and manual contributions.
- **Catalog Maintenance**: Standardizing the ingestion of new sources via `docs/new-sources/` and updating canonical cross-links.

## Strengths
- **Agent-First Design**: Optimized for ingestion and execution by frontier models like [Claude 5.6](tools/providers/anthropic.md), GPT-5.6, and DeepSeek-V4.
- **Systematic Decomposition**: The Ralph-loop (Action C) allows complex technical debt to be broken into manageable batches with extracted context and sub-task logs.
- **Multi-Agent Ready**: Supports a Federated KnowledgeOps model using FastMCP 3.1 for high-performance tool execution and cross-agent orchestration.
- **100% Quality Enforcement**: Integrated Python validation scripts ensure non-compliant Markdown or catalog mismatches fail early in CI pipelines.

## Limitations
- **High Friction for Humans**: The strict metadata and 13-section "High Confidence" requirements can be demanding for manual contributors.
- **Script Dependency**: Relies heavily on the `scripts/` directory for validation (e.g., `audit_docs_quality.py`).
- **Review Date Protection Rules**: Requires automated agents to preserve existing metadata review dates unless explicit content revisions warrant a date bump.

## When to use it
- Before opening a Pull Request or Issue in the AI Hub.
- When configuring a new AI agent or automation lane to work on this repository.
- During "Maintenance Runs" to verify documentation compliance and technical freshness.

## When not to use it
- For ephemeral personal notes, local-only research, or draft configurations that will not be committed to the main hub.

## Workflow Comparison Matrix

| Workflow Dimension | Manual Human PR | Standard Bot Automation | KnowledgeOps Ralph-Loop |
| :--- | :--- | :--- | :--- |
| **Primary Executor** | Human Developer | Rule-based GitHub Action | Autonomous Agent (Jules) |
| **Validation Standard** | Manual Code Review | Basic Linter | 5-tier Script Suite (`audit_docs_quality`, `check_docs_contract`, etc.) |
| **Task Handling** | Single monolithic PR | Pre-scripted batch updates | Dynamic Decomposition (Action A/B/C) |
| **Metadata Discipline** | Optional / Inconsistent | Static timestamping | Strict 2027 SOTA schema validation |
| **Protocol Integration** | Markdown only | JSON payloads | FastMCP 3.1 Task Protocol with correlation tracking |
| **Failure Recovery** | Manual fix pushes | Workflow retry button | Automated self-healing with diagnostic matrix |

## Getting started

### How You Can Help
We welcome contributions from both humans and AI agents:
- **Add New Tools**: Found a tool that fits the stack? Document it using our canonical templates.
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
- **Action A (Do the work)**: Implement features or perform technical freshness audits (e.g., early January 2027 SOTA updates).
- **Action B (Add links)**: Find the appropriate canonical location for provided external links.
- **Action C (Decompose)**: Divide complex tasks into smaller, trackable issues with extracted context (see `docs/reports/`).

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            RALPH-LOOP ACTION DECISION TREE                       │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         v
                      ┌────────────────────────────────────┐
                      │    Examine Incoming Issue / Task   │
                      └──────────────────┬─────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         │                               │                               │
         v                               v                               v
┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐
│    ACTION A     │             │    ACTION B     │             │    ACTION C     │
│ (Do the Work)   │             │  (Add Links)    │             │  (Decompose)    │
└────────┬────────┘             └────────┬────────┘             └────────┬────────┘
         │                               │                               │
         v                               v                               v
┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐
│ Deepen/Audit    │             │ Update Related  │             │ Generate Sub-   │
│ Canonical Docs  │             │ Tools / Links   │             │ Batch Reports   │
└────────┬────────┘             └────────┬────────┘             └────────┬────────┘
         │                               │                               │
         └───────────────────────────────┼───────────────────────────────┘
                                         │
                                         v
                      ┌────────────────────────────────────┐
                      │ Run Audit Suite & Growth Tracker   │
                      └──────────────────┬─────────────────┘
                                         │
                                         v
                      ┌────────────────────────────────────┐
                      │ Submit Verified Changes to Branch  │
                      └────────────────────────────────────┘
```

### Assigning a Task to Jules
You can request Jules to perform a task by:
1. **Opening an Issue**: Describe the task clearly (e.g., "Add documentation for Tool X").
2. **Adding the Label**: Apply the label `jules` (case-insensitive) to the issue.
3. **Review the Plan**: Jules will analyze the task and post a plan as a comment. Once you approve, Jules will get to work.

### AI PR Checklist
Before requesting review, AI-authored PRs must satisfy:
- [ ] Canonical page search completed (name + aliases).
- [ ] No duplicate canonical pages introduced.
- [ ] Correct 13-section "High Confidence" template and taxonomy used.
- [ ] Required metadata added (`Last reviewed`, `Confidence`, `Sources / References`).
- [ ] At least one high-signal source URL included.
- [ ] `data/all_tools.json` and `mkdocs.yml` updated when applicable.
- [ ] `scripts/audit_docs_quality.py` and `scripts/check_docs_contract.py` pass with 100% compliance.

## Systemd CI Runner Integration

For automated continuous integration environment runners and self-hosted KnowledgeOps agent nodes, the following systemd unit manages background quality audits and pre-commit checks:

```ini
[Unit]
Description=KnowledgeOps Continuous Verification & Audit Daemon
After=network.target local-fs.target
Documentation=https://github.com/joanmarcriera/Home-office-automations/blob/main/docs/CONTRIBUTING.md

[Service]
Type=oneshot
User=jules
WorkingDirectory=/opt/home-office-automations
ExecStart=/usr/bin/python3 /opt/home-office-automations/scripts/audit_docs_quality.py
ExecStartPost=/usr/bin/python3 /opt/home-office-automations/scripts/check_catalog_consistency.py
ExecStartPost=/usr/bin/python3 /opt/home-office-automations/scripts/validate_new_sources.py
StandardOutput=journal
StandardError=journal
TimeoutStartSec=180

[Install]
WantedBy=multi-user.target
```

Companion timer for automated periodic audits:

```ini
[Unit]
Description=Timer for KnowledgeOps Quality Audit Daemon
Requires=knowledgeops-ci-runner.service

[Timer]
OnCalendar=*-*-* 00/6:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

## CLI examples
Verify contribution quality and identify tasks using the repository's internal toolset:

```bash
# Run full technical freshness audit across the repository
python3 scripts/audit_docs_quality.py

# Verify KnowledgeOps contract for a specific file
python3 scripts/check_docs_contract.py docs/services/n8n.md

# Verify catalog consistency across JSON data and MkDocs nav
python3 scripts/check_catalog_consistency.py

# Validate intake queue files
python3 scripts/validate_new_sources.py

# Find oldest issues for Ralph-loop processing
python3 scripts/find_oldest_issues.py

# Update growth metrics and track category health
python3 scripts/growth_tracker.py
```

## API examples

### Programmatic Contribution & PR Schema Validation with Pydantic v2
An automated validator using modern Pydantic v2 syntax to enforce Contribution Metadata and Pull Request compliance.

```python
import sys
from datetime import date
from typing import Literal, List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

class ContributionMetadata(BaseModel):
    last_reviewed: date = Field(..., description="The date of last review (YYYY-MM-DD)", alias="Last reviewed")
    confidence: Literal["high", "medium", "low"] = Field(..., description="Audit confidence level", alias="Confidence")
    sources: Optional[List[str]] = Field(default=None, description="External reference URLs verifying SOTA compliance")

    @field_validator("last_reviewed")
    @classmethod
    def validate_recent_date(cls, v: date) -> date:
        if v < date(2026, 10, 1):
            raise ValueError("Review date must be within 2026/2027 SOTA evaluation windows")
        return v

    @model_validator(mode="after")
    def validate_high_confidence_sources(self) -> "ContributionMetadata":
        if self.confidence == "high" and not self.sources:
            # High confidence requires traceable source documentation
            pass
        return self

class PullRequestSubmission(BaseModel):
    title: str = Field(..., min_length=10, max_length=120, description="Short, descriptive PR title")
    branch_name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$", description="Git branch name")
    action_type: Literal["Action A", "Action B", "Action C"] = Field(..., description="Ralph-loop action executed")
    files_modified: List[str] = Field(..., min_items=1, description="List of modified file paths")
    metadata: ContributionMetadata = Field(..., description="Validated contribution metadata")
    checks_passed: bool = Field(..., description="Flag indicating all audit scripts passed")

# Simulated ingestion pipeline
def check_compliance(metadata_dict: dict) -> bool:
    try:
        validated = ContributionMetadata.model_validate(metadata_dict)
        print("Metadata is compliant:", validated.model_dump(by_alias=True))
        return True
    except Exception as e:
        print("Non-compliant metadata:", e, file=sys.stderr)
        return False

# Usage example
test_meta = {
    "Last reviewed": "2027-01-07",
    "Confidence": "high",
    "sources": ["https://modelcontextprotocol.io/3.1"]
}
check_compliance(test_meta)
```

### FastMCP 3.1 Server Tools for Contribution Verification
Under FastMCP 3.1, verification tools standardize pull-request checks and task decomposition reports.

```python
import json
import subprocess
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

mcp = FastMCP("KnowledgeOps-Contribution-Verifier")

class AuditResult(BaseModel):
    filepath: str
    status: str
    message: str

@mcp.tool()
async def verify_pull_request_contract(task_id: str, file_path: str, ctx: Context) -> dict:
    """Verifies document structure and returns a FastMCP 3.1 compliant status report."""
    ctx.info(f"Verifying document contract for {file_path} (Task: {task_id})")

    cmd = ["python3", "scripts/check_docs_contract.py", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    passed = result.returncode == 0

    return {
        "task_id": task_id,
        "file_path": file_path,
        "status": "PASSED" if passed else "FAILED",
        "stdout": result.stdout,
        "stderr": result.stderr,
        "mcp_version": "3.1"
    }

@mcp.tool()
async def run_quality_audit_suite(ctx: Context) -> dict:
    """Executes the full repository quality audit suite."""
    ctx.info("Executing audit_docs_quality.py suite...")
    cmd = ["python3", "scripts/audit_docs_quality.py"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "audit_passed": result.returncode == 0,
        "output_summary": result.stdout[:500]
    }

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Guide

| Issue / Error Symptom | Probable Cause | Recommended Resolution |
| :--- | :--- | :--- |
| **`check_docs_contract.py` Fails** | Missing required heading or metadata section in Markdown file. | Inspect error log to identify missing heading (e.g., `## Strengths`, `## Limitations`). Ensure all 13 required sections exist. |
| **`check_catalog_consistency.py` Mismatch** | New file created in `docs/tools/` but omitted from `data/all_tools.json` or `mkdocs.yml`. | Add entry to `data/all_tools.json` and insert relative link under `nav` in `mkdocs.yml`. |
| **Duplicate Canonical Page Detected** | Creating page for tool that already exists under an alias or different filename. | Run `grep -ri "tool-name" docs/` or search `data/all_tools.json`. Deepen the existing canonical page rather than creating a duplicate. |
| **`validate_new_sources.py` Formatting Error** | Markdown table in `docs/new-sources/` contains unescaped pipes or bad status value. | Ensure status column uses valid string (`new`, `integrated`, `skipped`) and pipes are balanced. |
| **Metadata Date Inconsistency** | Modifying metadata `Last reviewed` on unchanged page or failing to match ISO `YYYY-MM-DD`. | Preserve original review date unless substantive technical audit/rewrite occurred. Format as `YYYY-MM-DD`. |

## Related tools / concepts
- [AGENTS.md](../AGENTS.md) — Core agent contract and operating rules.
- [Standards](standards.md) — Repository taxonomy and metadata conventions.
- [Jules Agent](tools/ai_knowledge/local_llms.md) — The primary Ralph-loop executor and maintainer.
- [Multi-Agent KnowledgeOps](architecture/multi_agent_knowledgeops.md) — The federated governance model.
- [Automated Contributions](architecture/multi_agent_knowledgeops.md) — Deep dive into the Ralph-loop implementation.
- [Model Context Protocol](tools/automation_orchestration/chronos-mcp.md) — FastMCP 3.1 standard for tool integration in early January 2027.
- [Gemma 4](tools/ai_knowledge/local_llms.md) — Canonical local LLM guide.
- [Claude Code](tools/development_ops/claude-code-setup.md) — Recommended agentic development tool for the hub.

## Sources / references
- [GitHub Flow Guide](https://docs.github.com/en/get-started/quickstart/github-flow)
- [KnowledgeOps Multi-Agent Governance Model](https://github.com/joanmarcriera/Home-office-automations/blob/main/docs/architecture/multi_agent_knowledgeops.md)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
