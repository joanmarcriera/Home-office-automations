# Standards and Conventions

## What it is
This document defines the technical standards, operational contracts, and governance conventions for the KnowledgeOps homelab automation stack. It establishes structural consistency across all documentation, guarantees inter-tool compatibility, and defines the operating protocols for autonomous engineering agents (such as Jules and Claude Code) and human maintainers alike.

Key standards updated for early 2027 include:
- **Multi-Model Engineering Alignment**: Unified taxonomy and contract alignment across frontier model architectures (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, **Qwen 3.6 VL**).
- **Schema & Type Enforcement**: Mandatory validation of all Python automation scripts, FastMCP servers, and metadata scrapers using **Pydantic v2**.
- **Model Context Protocol (FastMCP 3.1) Task Protocol**: Standardization of multi-agent execution pipelines, task tracking, tool parameters, and schema definitions on **FastMCP 3.1**.
- **Agentic Task Decomposition**: Protocol guidelines for decomposing large issues into predictable, auto-verifiable batches backed by JSON execution metrics.

```
+-----------------------------------------------------------------------------------+
|                         KnowledgeOps Governance Topology                          |
|                                                                                   |
|  +--------------------+     +---------------------+     +----------------------+  |
|  | KnowledgeOps       | --> | Continuous Audit &  | --> | FastMCP 3.1 Schema   |  |
|  | Standard (13 Secs) |     | Contract Validator  |     | & Pydantic v2 Gate   |  |
|  +--------------------+     +---------------------+     +----------------------+  |
|            |                                                       |              |
+------------|-------------------------------------------------------|--------------+
             |                                                       |
             v                                                       v
+--------------------------+                               +------------------------+
| Autonomous Agent Fleet   |                               | Version Control        |
| - Jules (Ralph-loop)     | ----------------------------> | - Clean PR Submissions |
| - Claude Code / OpenClaw |                               | - MkDocs Static Site   |
+--------------------------+                               +------------------------+
```

## What problem it solves
In a rapidly expanding repository containing hundreds of technical tool specifications, architectural guides, and automated workflows, inconsistent formats and missing context create significant operational hazards:
- **Documentation Drift**: Spec pages missing mandatory technical details or containing hallucinated model capabilities.
- **Agent Execution Failure**: Unstructured issue specs causing autonomous agents to fail pre-commit tests or generate invalid Git PR diffs.
- **Broken Navigation Links**: Divergent link paths breaking site builds and internal search indexers.
- **Unvalidated API Calls**: Lack of typing leading to runtime errors during automated intake syncs.

Establishing explicit, script-enforced standards resolves these failure modes by turning documentation quality into a testable invariant.

## Where it fits in the stack
**Governance & Contract Layer**.
This document sits at the root of the repository's rules hierarchy. It governs all documentation files in `docs/`, automation scripts in `scripts/`, and defines the exact verification checks executed by continuous integration pipelines.

```
+-----------------------------------------------------------------------------------+
| Governance Layer: standards.md & AGENTS.md                                        |
| - 13-Section Contract Rules / Taxonomy Map / Pydantic v2 Specifications           |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| Programmatic Enforcement Layer                                                    |
| - audit_docs_quality.py / check_docs_contract.py / check_catalog_consistency.py  |
+-----------------------------------------------------------------------------------+
                                         |
            +----------------------------+----------------------------+
            |                            |                            |
            v                            v                            v
+------------------------+  +------------------------+  +------------------------+
| Documentation Pages    |  | FastMCP Tool Servers   |  | Agent Fleet Workflows  |
| (680+ Canonical Specs) |  | (Python / TypeScript)  |  | (Jules, Claude Code)   |
+------------------------+  +------------------------+  +------------------------+
```

## Typical use cases
- **Continuous Quality Audits**: Guiding the rules enforced by `audit_docs_quality.py` and `check_docs_contract.py`.
- **Autonomous Agent Planning**: Serving as the system prompt context for agent planning, file expansion, and PR creation.
- **Intake File Processing**: Ensuring newly discovered AI tools log complete metadata and proper canonical link paths in `docs/new-sources/`.
- **FastMCP Tool Design**: Providing standard schemas and parameter typing for Model Context Protocol servers.

## Strengths
- **Programmatic Verifiability**: Every structural rule is paired with an automated diagnostic script that returns binary pass/fail results.
- **Agent-Friendly Contracts**: Clear, deterministic formatting rules enable autonomous agents to self-correct without human intervention.
- **Deep Interoperability**: Enforces uniform JSON logging, ISO8601 date conventions, and relative path structures across the entire stack.

## Limitations
- **Maintenance Overhead**: Adding new mandatory sections requires backfilling existing documentation pages via automated batch runs.
- **Strict Ordering**: Section headers must strictly match expected strings without unauthorized suffix modifications.

## When to use it
- When authoring or expanding any canonical documentation page in `docs/tools/`, `docs/services/`, or `docs/knowledge_base/`.
- When writing Python automation scripts or FastMCP 3.1 servers to ensure correct Pydantic v2 model validation.
- Before submitting any Pull Request to guarantee all quality gates pass without warnings.

## When not to use it
- For scratchpad files or temporary local test outputs that will not be committed to Git.
- When working on external third-party repositories with non-KnowledgeOps conventions.

## Getting started

### 1. Repository Setup
```bash
# Clone repository and verify environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Verify Standards Compliance Locally
```bash
# Audit all documentation files against standards
python3 scripts/audit_docs_quality.py

# Verify catalog consistency across mkdocs.yml and navigation
python3 scripts/check_catalog_consistency.py
```

## CLI examples

```bash
# Verify the KnowledgeOps contract for a target document
python3 scripts/check_docs_contract.py docs/tools/providers/vercel-ai-gateway.md

# Inspect document character lengths to identify shallow pages
python3 -c "import os; print([(f, len(open(os.path.join(r, f)).read())) for r, d, fs in os.walk('docs') for f in fs if f.endswith('.md') and 'README' not in f][:5])"

# Update repository metrics and track shallow doc progress
python3 scripts/growth_tracker.py
```

## API examples

The following Python script demonstrates how standard document metadata and FastMCP 3.1 tool definitions are validated using **Pydantic v2**:

```python
import re
from datetime import date
from typing import Literal, List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("StandardsVerificationServer")

class ContributionMetadata(BaseModel):
    filepath: str = Field(..., description="Relative path to target document")
    last_reviewed: date = Field(..., description="ISO 8601 date format (YYYY-MM-DD)")
    confidence: Literal["high", "medium", "low"] = Field(..., description="Assessment confidence level")

    @field_validator("last_reviewed")
    @classmethod
    def validate_recent_date(cls, v: date) -> date:
        if v.year < 2026:
            raise ValueError("Review date must be within or after 2026")
        return v

class DocumentAuditReport(BaseModel):
    filepath: str
    is_compliant: bool
    missing_sections: List[str]
    character_count: int = Field(..., ge=0)
    metadata: Optional[ContributionMetadata] = None

@mcp.tool()
async def audit_document_contract(filepath: str, content: str) -> str:
    """FastMCP 3.1 tool to validate a markdown file against the KnowledgeOps contract."""
    required_sections = [
        "What it is", "What problem it solves", "Where it fits in the stack",
        "Typical use cases", "Strengths", "Limitations", "When to use it",
        "When not to use it", "Getting started", "CLI examples", "API examples",
        "Related tools / concepts", "Sources / references"
    ]

    missing = [sec for sec in required_sections if f"## {sec}" not in content]

    # Extract metadata
    date_match = re.search(r"Last reviewed:\s*(\d{4}-\d{2}-\d{2})", content)
    conf_match = re.search(r"Confidence:\s*(high|medium|low)", content, re.IGNORECASE)

    meta_obj = None
    if date_match and conf_match:
        try:
            meta_obj = ContributionMetadata(
                filepath=filepath,
                last_reviewed=date_match.group(1),
                confidence=conf_match.group(1).lower()
            )
        except ValidationError:
            pass

    report = DocumentAuditReport(
        filepath=filepath,
        is_compliant=len(missing) == 0 and meta_obj is not None,
        missing_sections=missing,
        character_count=len(content),
        metadata=meta_obj
    )
    return report.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Core Taxonomy & Contracts

### Core Taxonomy
The knowledge base uses a stable set of top-level categories. Do not create new top-level sections unless strictly necessary.

| Category | Location | What belongs here |
| :--- | :--- | :--- |
| **AI & Knowledge** | `docs/tools/ai_knowledge/` | General AI tools, knowledge management, LLM products |
| **Frameworks** | `docs/tools/frameworks/` | Libraries for building LLM apps (LangChain, LlamaIndex, etc.) |
| **Providers** | `docs/tools/providers/` | Companies offering LLM APIs or managed AI services |
| **Agents** | `docs/tools/agents/` | Agent frameworks and autonomous AI tools |
| **Orchestration** | `docs/tools/orchestration/` | Workflow automation, multi-agent routing, pipeline tools |
| **Infrastructure** | `docs/tools/infrastructure/` | Inference engines, vector DBs, serving stacks, quantisation |
| **Benchmarking** | `docs/tools/benchmarking/` | Eval frameworks, benchmarks, leaderboards |
| **Development & Ops** | `docs/tools/development_ops/` | AI-assisted coding tools and IDEs |
| **Patterns** | `docs/knowledge_base/patterns/` | Recurring design patterns (RAG, tool calling, routing, etc.) |
| **Playbooks** | `docs/playbooks/` | Step-by-step workflow guides |

### KnowledgeOps Contract (High Confidence Standard)
Every high-confidence documentation page must include these 13 sections in this exact order:
1. `What it is`
2. `What problem it solves`
3. `Where it fits in the stack`
4. `Typical use cases`
5. `Strengths`
6. `Limitations`
7. `When to use it`
8. `When not to use it`
9. `Getting started`
10. `CLI examples`
11. `API examples`
12. `Related tools / concepts` (>= 7 unique relative markdown links)
13. `Sources / references` (at least one valid URL)

### Contribution Metadata (Required)
Every knowledge page must include this section at the bottom:
- `Last reviewed`: ISO date (`YYYY-MM-DD`)
- `Confidence`: `high`, `medium`, or `low`

## Related tools / concepts
- [AGENTS.md](../AGENTS.md) — Operating guidelines for AI agent interactions.
- [Multi-Agent KnowledgeOps](architecture/multi_agent_knowledgeops.md) — Architectural framework for multi-agent workflows.
- [Audit Docs Quality Script](../scripts/audit_docs_quality.py) — Repository audit utility.
- [Check Docs Contract Script](../scripts/check_docs_contract.py) — Per-file contract validator script.
- [Claude Code](tools/development_ops/claude-code.md) — Terminal-native agentic development CLI.
- [Jules Agent](tools/ai_knowledge/jules.md) — Autonomous repository maintenance agent.
- [FastMCP 3.1](tools/automation_orchestration/mcp.md) — Framework for Model Context Protocol 3.1.

## Sources / references
- [GitHub Flow Guide](https://docs.github.com/en/get-started/quickstart/github-flow)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec/3.1)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
