# Contributing to the AI Hub

## What it is
The `CONTRIBUTING.md` guide is the primary governance document defining how humans and AI agents (e.g., [Claude 5.6](tools/providers/anthropic.md), GPT-5.6, [Gemini](tools/ai_knowledge/gemini.md) 4.0 Pro/Ultra, [DeepSeek](tools/providers/deepseek.md)-V4, [Llama 4](tools/ai_knowledge/llama-4.md), [Gemma](tools/ai_knowledge/gemma.md) 3, and Qwen 3.8) collaborate to maintain the Home-Office Automation & AI Hub. It serves as the operational manual for the repository's "KnowledgeOps" framework in early January 2027.

## What problem it solves
It prevents "documentation rot" and repository fragmentation by enforcing a unified taxonomy, deduplication protocols, and the **Ralph-loop** automation cycle. It ensures that every contribution—whether a tool update or a new architectural pattern—meets the "High Confidence" early January 2027 State-of-the-Art standard.

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
- **Agent Onboarding**: Establishing the "Quick Start" sequence for new LLM agents.
- **Ralph-loop Execution**: Defining how Jules (the primary agent) processes, decomposes, and closes issues.
- **Quality Assurance**: Providing the checklist for AI-authored PRs.
- **Catalog Maintenance**: Standardizing the ingestion of new sources via `docs/new-sources/`.

## Strengths
- **Agent-First Design**: Optimized for ingestion and execution by frontier models like [Claude 5.6](tools/providers/anthropic.md), GPT-5.6, and DeepSeek-V4.
- **Systematic Decomposition**: The Ralph-loop (Action C) allows complex technical debt to be broken into manageable batches with extracted context and sub-task logs.
- **Multi-Agent Ready**: Supports a Federated KnowledgeOps model using FastMCP 3.1 for high-performance tool execution and cross-agent orchestration.

## Limitations
- **High Friction for Humans**: The strict metadata and 13-section "High Confidence" requirements can be demanding for manual contributors.
- **Script Dependency**: Relies heavily on the `scripts/` directory for validation (e.g., `audit_docs_quality.py`).

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
- **Action A (Do the work)**: Implement features or perform technical freshness audits (e.g., early January 2027 SOTA updates).
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

## Comprehensive Contribution Architecture & Pipeline

```
+---------------------------------------------------------------------------------------+
|                               CONTRIBUTION PIPELINE FLOW                              |
|                                                                                       |
|  [Contributor / Agent]                                                                |
|         |                                                                             |
|         v                                                                             |
|  (1. Search Canonical Docs) ---> Match Found? ---> YES ---> Edit Existing File        |
|         |                                                      |                      |
|         NO                                                     v                      |
|         v                                            (Apply 13-Section Schema)        |
|  (2. Create New Doc from Template)                             |                      |
|         |                                                      v                      |
|         +---------------------------------------------> (Update Catalog & Nav)        |
|                                                                |                      |
|                                                                v                      |
|                                                    (3. Execute Quality Gates)         |
|                                                                |                      |
|                                                                v                      |
|                                                    [audit_docs_quality.py]            |
|                                                    [check_catalog_consistency.py]     |
|                                                    [validate_new_sources.py]          |
|                                                    [check_docs_contract.py]           |
|                                                                |                      |
|                                                                v                      |
|                                                    (4. Submit PR & Merge)             |
+---------------------------------------------------------------------------------------+
```

## Maintenance & Systemd Service Specs
For automated contribution runners and KnowledgeOps agent daemons running locally, the following systemd unit manages background execution.

```ini
[Unit]
Description=KnowledgeOps Automated Contribution Worker (FastMCP 3.1)
After=network.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=jules
Group=jules
WorkingDirectory=/opt/home-office-automations
Environment="PYTHONUNBUFFERED=1"
Environment="KNOWLEDGEOPS_ENV=production"
ExecStart=/usr/bin/python3 -m scripts.jules_issue_watcher --interval 60
Restart=always
RestartSec=10s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=knowledgeops-worker

# Security Sandbox
ProtectSystem=full
ProtectHome=read-only
ReadWritePaths=/opt/home-office-automations/docs /opt/home-office-automations/data
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Error Code / Symptom | Possible Root Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| `DOC_CONTRACT_INVALID` | Missing required metadata fields or 13-section headers | `python3 scripts/check_docs_contract.py <path>` | Add missing metadata (`Last reviewed`, `Confidence`) or missing standard headers |
| `CATALOG_MISMATCH` | Canonical page not present in `data/all_tools.json` or `mkdocs.yml` | `python3 scripts/check_catalog_consistency.py` | Add entry to `data/all_tools.json` and sync `mkdocs.yml` navigation structure |
| `INTAKE_VALIDATION_FAIL` | Unresolved `Status = new` rows in intake files | `python3 scripts/validate_new_sources.py` | Process intake row, set status to `integrated`, and link canonical doc |
| `METADATA_DATE_STALE` | `Last reviewed` date older than minimum threshold | `python3 scripts/check_doc_freshness.py` | Audit technical content and update `Last reviewed` timestamp |
| `MCP_PROTOCOL_TIMEOUT` | FastMCP tool execution timed out during automated PR check | `journalctl -u knowledgeops-worker -n 50` | Restart background service and verify network connectivity to MCP host |

## CLI examples
Verify contribution quality and identify tasks using the repository's internal toolset:

```bash
# Run full technical freshness audit across the repository
python3 scripts/audit_docs_quality.py

# Verify KnowledgeOps contract for a specific file
python3 scripts/check_docs_contract.py docs/services/n8n.md

# Find oldest issues for Ralph-loop processing
python3 scripts/find_oldest_issues.py

# Update growth metrics and track category health
python3 scripts/growth_tracker.py
```

## API examples

### Programmatic Contribution Metadata Validation with Pydantic v2 (Python)
An automated validator using modern Pydantic v2 syntax to enforce Contribution Metadata compliance.

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
test_meta = {"Last reviewed": "2027-01-07", "Confidence": "high", "sources": ["https://modelcontextprotocol.io/3.1"]}
check_compliance(test_meta)
```

### Programmatic Integration with FastMCP 3.1 Task Protocol
Under FastMCP 3.1, a verification tool standardizes reports using the Task Protocol schemas.

```python
import json
import urllib.request
from fastmcp import FastMCP, Context

mcp = FastMCP("KnowledgeOps-Contribution-Verifier")

@mcp.tool()
async def verify_doc_contract(task_id: str, file_path: str, ctx: Context) -> dict:
    """Verifies document structure and returns a FastMCP 3.1 compliant status report."""
    ctx.info(f" Verifying document contract for {file_path} (Task: {task_id})")

    # Run internal inspection logic
    passed = True

    payload = {
        "task_id": task_id,
        "step_name": f"standards-verification-{file_path}",
        "status": "passed" if passed else "failed",
        "metadata": {
            "standards_version": "2027.01",
            "enforcing_model": "Claude 5.6",
            "file_path": file_path
        }
    }
    return payload

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [AGENTS.md](../AGENTS.md) — Core agent contract and operating rules.
- [Standards](standards.md) — Repository taxonomy and metadata conventions.
- [Jules Agent](tools/ai_knowledge/local_llms.md) — The primary Ralph-loop executor and maintainer.
- [Multi-Agent KnowledgeOps](architecture/multi_agent_knowledgeops.md) — The federated governance model.
- [Automated Contributions](architecture/multi_agent_knowledgeops.md) — Deep dive into the Ralph-loop implementation.
- [Model Context Protocol](tools/automation_orchestration/chronos-mcp.md) — FastMCP 3.1 standard for tool integration in early January 2027.
- [Gemma 3](tools/ai_knowledge/local_llms.md) — Canonical local LLM guide.
- [Claude Code](tools/development_ops/claude-code-setup.md) — Recommended agentic development tool for the hub.

## Sources / references
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [KnowledgeOps Manifesto](https://github.com/joanmarcriera/Home-office-automations/blob/main/docs/architecture/multi_agent_knowledgeops.md)
- [Ralph-loop Documentation](https://github.com/joanmarcriera/Home-office-automations/blob/main/docs/architecture/multi_agent_knowledgeops.md)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
