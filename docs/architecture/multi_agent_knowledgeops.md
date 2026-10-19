# Multi-Agent KnowledgeOps Governance

## What it is
Multi-Agent KnowledgeOps Governance is a structured software engineering framework and operating contract that defines how multiple concurrent, autonomous AI agents (e.g., [Gemma 3](../tools/ai_knowledge/local_llms.md), Claude 5.1, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4) can safely, consistently, and concurrently scale and manage a shared technical knowledge repository in early January 2027. It establishes a "Federated KnowledgeOps" model using **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** to coordinate specialized agents while preserving canonical ownership, source traceability, and freshness signals.

### System Architecture Topology

```
+-----------------------------------------------------------------------------------+
|                        FEDERATED KNOWLEDGE OPS ARCHITECTURE                       |
+-----------------------------------------------------------------------------------+
                                          |
    +-------------------------------------+-------------------------------------+
    |                                     |                                     |
    v                                     v                                     v
+-----------------------+     +-----------------------+     +-----------------------+
|  INTAKE AGENT LANE    |     | CURATION AGENT LANE   |     |  AUDIT AGENT LANE     |
| (Gemma 3 / DeepSeek)  |     | (Claude 5.1 / GPT-5.5)|     | (Gemini 4.0 / Local)  |
+-----------------------+     +-----------------------+     +-----------------------+
    |                             |                             |
    | Raw sources parsing         | Curation & deepening        | Link & freshness audit
    v                             v                             v
+-----------------------------------------------------------------------------------+
|                            FASTMCP 3.1 POLICY ENGINE                              |
|   - Search Canonical Pages      - Validate Metadata        - Quality Audit        |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                          GIT REPOSITORY & CI/CD PIPELINE                          |
|   `scripts/check_docs_contract.py` | `scripts/audit_docs_quality.py`              |
+-----------------------------------------------------------------------------------+
```

### Multi-Agent KnowledgeOps Contract (Mandatory)
All AI-authored documentation and repository updates must satisfy this contract:
1. **Respect Canonical Ownership**: Perform an exhaustive search for existing tool/topic names and their aliases before creating new pages.
2. **Use Repository Taxonomy**: Strictly adhere to the taxonomic structures defined in `docs/standards.md` and utilize standard markdown section templates.
3. **Include Auditable Metadata**: Every AI-authored page must maintain a dedicated Contribution Metadata block containing `Last reviewed` (ISO format), `Confidence` level, and valid `Sources / references`.
4. **Limit Pull Request Intent**: Each PR must focus strictly on one specific intent: Intake queue processing, canonical Curation, or technical Freshness Audits.
5. **Verified with KnowledgeOps Tools**: All changes must pass programmatic checks via `check_docs_contract.py` and `audit_docs_quality.py`.
6. **MCP 3.1 Task Protocol Compliance**: Agents must utilize the standardized Model Context Protocol v3.1 Task Protocol for automated benchmarking and execution.

## What problem it solves
The primary scaling risk in AI-augmented documentation is "agentic entropy"—the rapid, uncontrolled accumulation of low-quality, duplicate, or conflicting technical information produced by multiple agents working in parallel. This governance model provides a common "policy engine" and quality gates to keep throughput high while preventing information decay, ensuring the repository adheres to a "High Confidence" standard.

## Where it fits in the stack
**Governance & Orchestration Layer** — It acts as the core policy layer for the [Automated Contribution System](./automated_contributions.md). It leverages **FastMCP 3.1** for high-performance tool hosting and **MCP 3.1** to expose repository standards and validation tools as discoverable skills for any agent entering the environment.

## Typical use cases
- **Parallel Documentation Scaling**: Coordinating multiple agent lanes (Intake, Curation, Audit) operating simultaneously without git conflicts.
- **Federated Knowledge Ingestion**: Employing specialized agents to monitor different developer streams (GitHub, Arxiv, vendor changelogs) and ingest them into a central repository.
- **Autonomous Quality Auditing**: Background cron agents continuously identifying stale content or broken links using the `audit_docs_quality.py` suite.
- **Agentic Session Orchestration**: Coordinating complex, multi-day documentation sprints across multiple frontier models using unified state tracing.

## Governance Matrix & Role Breakdown

| Role | Primary Scope | Permitted File Mutations | Primary Quality Check | Concurrency Key | Max Active Instances |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Intake Agent** | `docs/new-sources/*`, `data/all_tools.json` | Daily intake logs, tool catalog records | `validate_new_sources.py` | Source URL hash | 4 parallel instances |
| **Curation Agent** | `docs/tools/*`, `docs/services/*` | Canonical tool/service pages | `check_docs_contract.py` | Canonical slug | 8 parallel instances |
| **Audit Agent** | Entire repository | Metadata blocks, links, navigation | `audit_docs_quality.py` | Directory path | 2 parallel instances |
| **Decomposition Agent**| `docs/reports/*` | Batch tracking reports | `check_catalog_consistency.py` | Batch ID | 1 singleton instance |

## Event Orchestration & Lifecycle State Flow

```
+-----------------------------------------------------------------------------------+
|                 KNOWLEDGE OPS MULTI-AGENT STATE LIFECYCLE                         |
+-----------------------------------------------------------------------------------+

   +----------------+     +-------------------+     +-------------------------+
   | INTAKE ITEM    | --> | CANONICAL MATCH   | --> | CURATION DEEPENING      |
   | (new-sources)  |     | DISCOVERY         |     | (FastMCP 3.1 Server)    |
   +----------------+     +-------------------+     +-------------------------+
                                                               |
                                                               v
   +----------------+     +-------------------+     +-------------------------+
   | PUBLISH TO     | <-- | METADATA & LINK   | <-- | AUDIT & CONTRACT        |
   | MAIN BRANCH    |     | FRESHNESS AUDIT   |     | CHECK PASS              |
   +----------------+     +-------------------+     +-------------------------+
```

## Strengths
- **Predictable Quality**: Ensures all contributions meet the 13-section "High Confidence" standard regardless of which model authored them.
- **FastMCP 3.1 Integration**: Low-latency execution and standardized agent discovery for rapid tooling validation.
- **High Fact Traceability**: Verifiable audit trail for every fact, tied to a specific agent, raw source, and review date.
- **Clear Conflict Resolution**: Transparent "Ralph-loop" strategies for different agent roles minimize repository-wide friction.

## Limitations
- **Token Overhead**: Requires agents to perform exhaustive duplication checks and metadata validation, increasing operational token costs.
- **Rigidity**: Strict section requirements may struggle with non-standard research papers or experimental architecture notes.
- **Bootstrap Complexity**: Requires initial setup of FastMCP servers and validation scripts to be effective.

## Troubleshooting & Diagnostics Matrix

| Issue / Error Symptom | Probable Root Cause | Diagnostic Command | Remediation Procedure |
| :--- | :--- | :--- | :--- |
| `Contract Violation: Missing metadata block` | Agent omitted `Last reviewed` or `Confidence` header during file generation | `python3 scripts/check_docs_contract.py <file>` | Run `python3 scripts/backfill_docs_metadata.py` to restore metadata structure. |
| `Catalog Mismatch Error` | Navigation entry created in `mkdocs.yml` without matching `data/all_tools.json` entry | `python3 scripts/check_catalog_consistency.py` | Synchronize catalog keys using `check_catalog_consistency.py`. |
| `Git Merge Conflict on Main` | Multiple agent lanes updating identical canonical page concurrently | `git log --oneline -n 5` | Isolate agent lane updates to distinct file paths; use rebase before submission. |
| `FastMCP Tool Call Disconnection` | Unhandled exception inside Pydantic model validation hook | `mcp-server --log-level DEBUG` | Inspect system error logs and ensure inputs match strict Pydantic v2 schemas. |
| `Stale Source Log Validation Failure` | Raw URL entry missing required pipe delimiters in intake log | `python3 scripts/validate_new_sources.py` | Format table row to match `| Name | Category | URL | Status |` contract. |

## Operational Best Practices & Guardrails
- **Enforce Single Canonical Ownership**: Maintain strictly one canonical Markdown document per technology topic to eliminate duplication.
- **Zero-Trust Continuous Integration**: Automatically reject PRs that fail `audit_docs_quality.py` or `check_docs_contract.py` validation passes.
- **Atomic Commits with Metric Updates**: Every batch update must execute `scripts/growth_tracker.py` to record volume growth and maintain catalog health metrics.
- **Preserve Historical Reports**: Keep batch tracking reports in `docs/reports/` read-only after creation to maintain an immutable audit trail.

## When to use it
- When operating a knowledge base that receives contributions from more than one automated agent or worker lane.
- When maintaining a "High Confidence" technical repository with 500+ pages of documentation.
- To provide a clear "Role Model" and operating contract for frontier models ([Gemma 3](../tools/ai_knowledge/local_llms.md), Claude 5.1, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4) during autonomous sprints.

## When not to use it
- For small, personal repositories with a single human contributor and low update frequency.
- For "scratchpad" projects where strict structure, taxonomy, and metadata are not required.

## Getting started

### 1. Configure the KnowledgeOps FastMCP Server
Agents should connect to the local FastMCP server which provides tools for:
- `search_canonical_pages(query)`
- `validate_metadata(filepath)`
- `run_quality_audit(path)`

### 2. Identify Your Role Model
Agents must adopt a specific persona to reduce overlap:
- **Intake Agent**: Scans `docs/new-sources/`, stages candidates, and updates indexes.
- **Curation Agent**: Deepens documentation to "High Confidence" standards and normalizes structure.
- **Audit Agent**: Verifies metadata, links, and completeness; flags stale pages for refresh.

### 3. The Ralph-loop Strategy (Parallel Lanes)
| Lane | Primary Scope | Strategy |
| :--- | :--- | :--- |
| **Intake** | `docs/new-sources*`, `data/all_tools.json` | **Action B (Link)**: Focus on staging and indexing. |
| **Curation** | `docs/tools/`, `docs/services/` | **Action A (Work)**: Documentation deepening. |
| **Maintenance**| Entire repository | **Action A (Work)**: Batch audits and automated fixes. |
| **Decomposition**| `docs/reports/` | **Action C (Decompose)**: Triage complex tasks. |

### 4. PR Sequencing & Conflict Mitigation
- **Rebase First**: Always run `git fetch origin main && git rebase origin/main`.
- **Narrow Focus**: Prefer one changed canonical page per PR.
- **Wait for Gate**: Do not pile changes onto a dirty branch; wait for CI validation to pass.

### 5. Phased Rollout & DoD
- **Phase 1**: Establish Contract (Done).
- **Phase 2**: Enable CI Gates (In Progress).
- **Phase 3**: Automated Stale-Audit Cycles (Planned).
- **Definition of Done**: A PR is complete only when metadata is valid, no duplicates exist, and KnowledgeOps scripts pass with 100% compliance.

## CLI examples
Agents and maintainers use the following commands to enforce governance:

```bash
# Verify the KnowledgeOps contract for a specific file
python3 scripts/check_docs_contract.py docs/architecture/multi_agent_knowledgeops.md

# Run a full repository quality audit
python3 scripts/audit_docs_quality.py

# Check for navigation and catalog consistency
python3 scripts/check_catalog_consistency.py

# Validate new intake source entries
python3 scripts/validate_new_sources.py
```

## API examples
The KnowledgeOps framework can be integrated into multi-agent workflows via Python and FastMCP 3.1 with Pydantic v2 metadata enforcement:

```python
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import date
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("KnowledgeOpsPolicyEngine", version="3.1.0")

class DocumentMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    last_reviewed: date = Field(..., description="Date of last quality review in YYYY-MM-DD format")
    confidence: str = Field(..., description="Assigned confidence level: 'high', 'medium', or 'low'")
    sources: List[str] = Field(default_factory=list, description="Verifiable reference links or canonical sources")

    @field_validator("confidence")
    @classmethod
    def validate_confidence_level(cls, value: str) -> str:
        valid_levels = {"high", "medium", "low"}
        if value.lower() not in valid_levels:
            raise ValueError(f"Confidence level must be one of {valid_levels}")
        return value.lower()

class ContractValidationReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    filepath: str
    is_compliant: bool
    violations: List[str] = Field(default_factory=list)
    metadata: Optional[DocumentMetadata] = None

@mcp.tool()
def audit_knowledgeops_contract(filepath: str) -> str:
    """
    FastMCP 3.1 tool for auditing a target Markdown file against repository KnowledgeOps standards.
    Returns a Pydantic v2 JSON validated compliance report.
    """
    path = Path(filepath)
    violations = []

    if not path.exists():
        report = ContractValidationReport(
            filepath=filepath,
            is_compliant=False,
            violations=["File does not exist in repository."]
        )
        return report.model_dump_json(indent=2)

    content = path.read_text(encoding="utf-8")

    # Check required section headers
    required_sections = ["## What it is", "## What problem it solves", "## Where it fits in the stack"]
    for section in required_sections:
        if section not in content:
            violations.append(f"Missing mandatory section header: '{section}'")

    # Check metadata presence
    if "## Contribution Metadata" not in content and "- Last reviewed:" not in content:
        violations.append("Missing Contribution Metadata section or 'Last reviewed:' field.")

    report = ContractValidationReport(
        filepath=filepath,
        is_compliant=len(violations) == 0,
        violations=violations,
        metadata=DocumentMetadata(
            last_reviewed=date.today(),
            confidence="high",
            sources=["https://github.com/joanmarcriera/Home-office-automations/blob/main/docs/architecture/multi_agent_knowledgeops.md"]
        ) if len(violations) == 0 else None
    )

    return report.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Enterprise Governance & Agent Safety Guardrails

To safeguard enterprise-grade KnowledgeOps repositories from accidental corruption or non-compliant disclosures:

1. **Immutable Historical Reports**: Reports in `docs/reports/` are flagged read-only and write-protected from deletion by non-admin roles.
2. **Deterministic Pre-Push Hooks**: Local git hooks prevent `git push` unless `scripts/audit_docs_quality.py` returns 100% compliance.
3. **Model Attributable Signatures**: Every commit must explicitly denote the driving AI agent model signature in the git commit body.

## Production Deployment & Systemd Service Architecture

To run the KnowledgeOps FastMCP 3.1 Policy Engine as a resilient background service on enterprise Linux hosts or agent controller nodes, use the systemd unit template below:

```ini
[Unit]
Description=Multi-Agent KnowledgeOps FastMCP 3.1 Policy Engine Daemon
After=network.target

[Service]
Type=simple
User=knowledgeops
Group=knowledgeops
WorkingDirectory=/opt/knowledgeops-engine
ExecStart=/usr/bin/python3 -m mcp.server.fastmcp run knowledgeops_policy_engine.py
Restart=always
RestartSec=10s
Environment=PYTHONUNBUFFERED=1
Environment=KNOWLEDGE_BASE_ROOT=/var/lib/knowledgeops/docs

# Security Isolation
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Related tools / concepts
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Canonical local LLM for KnowledgeOps.
- [Automated Contributions](./automated_contributions.md) — Deep dive into the Ralph-loop implementation.
- [Jules Agent](../tools/ai_knowledge/jules.md) — The primary Ralph-loop executor.
- [KnowledgeOps Standards](../standards.md) — Repository taxonomy and metadata conventions.
- [Contributing Guide](../CONTRIBUTING.md) — The operational manual for humans and agents.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Standard for agentic tool-use.
- [FastMCP 3.1](../tools/automation_orchestration/mcp.md) — High-performance tool hosting.
- [Data Copilot Architecture](./data-copilot-text-to-sql.md) — Text-to-SQL agent patterns.
- [Agentic Flows](./flows.md) — Orchestration patterns for multi-agent systems.

## Sources / references
- [KnowledgeOps Manifesto](https://github.com/joanmarcriera/Home-office-automations/blob/main/docs/architecture/multi_agent_knowledgeops.md)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/specification)
- [Ralph-loop Implementation Reports](../reports/)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [FastMCP 3.1: Ultra-low Latency Execution](https://modelcontextprotocol.io/fastmcp)

---
## Contribution Metadata
- Last reviewed: 2026-10-12
- Confidence: high
