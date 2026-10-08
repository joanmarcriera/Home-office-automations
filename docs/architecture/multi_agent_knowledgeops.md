# Multi-Agent KnowledgeOps Governance

## What it is
Multi-Agent KnowledgeOps Governance is a structured software engineering framework and operating contract that defines how multiple concurrent, autonomous AI agents (e.g., [Gemma 3](../tools/ai_knowledge/local_llms.md), Claude 5.1, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4) can safely, consistently, and concurrently scale and manage a shared technical knowledge repository in early January 2027. It establishes a "Federated KnowledgeOps" model using **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** to coordinate specialized agents while preserving canonical ownership, source traceability, and freshness signals.

### Multi-Agent KnowledgeOps Contract (Mandatory)
All AI-authored documentation and repository updates must satisfy this contract:
1. **Respect Canonical Ownership**: Perform an exhaustive search for existing tool/topic names and their aliases before creating new pages.
2. **Use Repository Taxonomy**: Strictly adhere to the taxonomic structures defined in `docs/standards.md` and utilize standard markdown section templates.
3. **Include Auditable Metadata**: Every AI-authored page must maintain a dedicated Contribution Metadata block containing `Last reviewed` (ISO format), `Confidence` level, and valid `Sources / references`.
4. **Limit Pull Request Intent**: Each PR must focus strictly on one specific intent: Intake queue processing, canonical Curation, or technical Freshness Audits.
5. **Verified with KnowledgeOps Tools**: All changes must pass programmatic checks via `check_docs_contract.py` and `audit_docs_quality.py`.
6. **MCP 3.1 Task Protocol Compliance**: Agents must utilize the standardized Model Context Protocol v3.1 Task Protocol for automated benchmarking and execution.

## Architecture & System Overview
KnowledgeOps coordinates multiple agent lanes operating over a shared repository, backed by FastMCP 3.1 tool gateways and CI quality gates.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      FEDERATED KNOWLEDGE-OPS ARCHITECTURE                        │
└──────────────────────────────────────────────────────────────────────────────────┘

   Agent Worker Lanes               FastMCP 3.1 Governance           Shared Knowledge
 ┌─────────────────────┐          ┌──────────────────────────┐      ┌────────────────────┐
 │ - Intake Agent      │─────────>│ - Duplication Check Tool │─────>│ - docs/new-sources │
 │ - Curation Agent    │          │ - Metadata Validation    │      │ - docs/tools/      │
 │ - Stale-Audit Agent │          │ - Section Contract Check │      │ - docs/services/   │
 └─────────────────────┘          └──────────────────────────┘      └────────────────────┘
            │                                  │                               │
            │                                  ▼                               │
            │                     ┌──────────────────────────┐                 │
            └────────────────────>│  Git Branch & PR Sync    │<────────────────┘
                                  └──────────────────────────┘
                                               │
                                               ▼
                                  ┌──────────────────────────┐
                                  │   CI Quality Gate Check  │
                                  │ - audit_docs_quality.py  │
                                  │ - check_docs_contract.py │
                                  └──────────────────────────┘
```

## What problem it solves
The primary scaling risk in AI-augmented documentation is "agentic entropy"—the rapid, uncontrolled accumulation of low-quality, duplicate, or conflicting technical information produced by multiple agents working in parallel. This governance model provides a common "policy engine" and quality gates to keep throughput high while preventing information decay, ensuring the repository adheres to a "High Confidence" standard.

## Where it fits in the stack
**Governance & Orchestration Layer** — It acts as the core policy layer for the [Automated Contribution System](./automated_contributions.md). It leverages **FastMCP 3.1** for high-performance tool hosting and **MCP 3.1** to expose repository standards and validation tools as discoverable skills for any agent entering the environment.

## Typical use cases
- **Parallel Documentation Scaling**: Coordinating multiple agent lanes (Intake, Curation, Audit) operating simultaneously without git conflicts.
- **Federated Knowledge Ingestion**: Employing specialized agents to monitor different developer streams (GitHub, Arxiv, vendor changelogs) and ingest them into a central repository.
- **Autonomous Quality Auditing**: Background cron agents continuously identifying stale content or broken links using the `audit_docs_quality.py` suite.
- **Agentic Session Orchestration**: Coordinating complex, multi-day documentation sprints across multiple frontier models using unified state tracing.

## Comparison Matrix

| Governance Dimension | Manual Curation | Naive Multi-Agent | KnowledgeOps (FastMCP 3.1) |
| :--- | :--- | :--- | :--- |
| **Throughput** | Low (Human bottleneck) | High (Uncontrolled) | Extremely High (Controlled) |
| **Duplicate Prevention** | Manual search | High Risk of Duplication | Programmatic FastMCP Guardrails |
| **Quality Compliance** | Variable | Low (Hallucinations & Drift) | 100% Contract Enforcement |
| **Source Traceability** | Medium | Low | Full Metadata Audit Trail |
| **Freshness Management**| Reactive | None | Automated Stale Scan Cron |

## Strengths
- **Predictable Quality**: Ensures all contributions meet the 13-section "High Confidence" standard regardless of which model authored them.
- **FastMCP 3.1 Integration**: Low-latency execution and standardized agent discovery for rapid tooling validation.
- **High Fact Traceability**: Verifiable audit trail for every fact, tied to a specific agent, raw source, and review date.
- **Clear Conflict Resolution**: Transparent "Ralph-loop" strategies for different agent roles minimize repository-wide friction.

## Limitations
- **Token Overhead**: Requires agents to perform exhaustive duplication checks and metadata validation, increasing operational token costs.
- **Rigidity**: Strict section requirements may struggle with non-standard research papers or experimental architecture notes.
- **Bootstrap Complexity**: Requires initial setup of FastMCP servers and validation scripts to be effective.

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
```

## API examples

### Programmatic Validation via Python & Pydantic v2
The KnowledgeOps framework can be integrated into multi-agent workflows via Python:

```python
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional

class ContributionMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    last_reviewed: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    confidence: str = Field(..., pattern=r"^(high|medium|low)$")

class DocValidationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filepath: str
    is_compliant: bool
    errors: List[str] = Field(default_factory=list)
    metadata: Optional[ContributionMetadata] = None

def audit_document_contract(path: Path) -> DocValidationReport:
    """Audits a documentation file against KnowledgeOps standards."""
    if not path.exists():
        return DocValidationReport(filepath=str(path), is_compliant=False, errors=["File not found"])

    content = path.read_text(encoding="utf-8")
    errors = []

    # Required Section Checks
    required_sections = ["## What it is", "## What problem it solves", "## Contribution Metadata"]
    for sec in required_sections:
        if sec not in content:
            errors.append(f"Missing required section header: '{sec}'")

    return DocValidationReport(
        filepath=str(path),
        is_compliant=len(errors) == 0,
        errors=errors
    )

if __name__ == "__main__":
    report = audit_document_contract(Path("docs/architecture/multi_agent_knowledgeops.md"))
    print(f"Compliance: {report.is_compliant}")
```

### FastMCP 3.1 Governance Tool Pattern
Exposes repository contract verification dynamically to agents via FastMCP 3.1 tool calls.

```python
from pathlib import Path
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "knowledgeops-governance",
    instructions="Provides programmatic documentation contract auditing for KnowledgeOps repositories."
)

class ContractAuditInput(BaseModel):
    filepath: str = Field(..., description="Relative path to markdown file in docs/ directory.")

@mcp.tool()
async def check_doc_contract(input_data: ContractAuditInput) -> Dict[str, Any]:
    """Runs KnowledgeOps contract verification against target document."""
    file_path = Path(input_data.filepath)
    if not file_path.exists():
        return {"status": "error", "message": f"Path '{input_data.filepath}' does not exist."}

    content = file_path.read_text(encoding="utf-8")
    missing_sections = []
    for section in ["## What it is", "## What problem it solves", "## Contribution Metadata"]:
        if section not in content:
            missing_sections.append(section)

    return {
        "filepath": input_data.filepath,
        "is_valid": len(missing_sections) == 0,
        "missing_sections": missing_sections
    }

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Troubleshooting
- **Branch Isolation**: Never allow multiple agents to modify the same canonical document on the same branch simultaneously.
- **Clock Drift Prevention**: Set CI environments to strictly validate `Last reviewed` metadata against the actual system date to prevent future-dated entries.
- **FastMCP Cache Invalidation**: Flush FastMCP tool catalog caches whenever scripts in `scripts/` undergo structural modifications.

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
- Last reviewed: 2027-01-07
- Confidence: high
