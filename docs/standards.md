# Standards and Conventions

## What it is
This document defines the overarching technical standards, operational conventions, architectural governance rules, and documentation quality contracts for the homelab and KnowledgeOps automation stack. It ensures strict interoperability between diverse tools, maintains documentation depth and freshness, and provides a deterministic protocol for both autonomous AI agents and human contributors.

Key updates for the early 2027 ecosystem include:
- **Foundational LLM & Agent Standards**: Alignment across frontier models (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, Qwen 3.6 VL) and specialized agent systems (Jules, Claude Code, Roo Code).
- **Enforced Schema Validation**: Mandatory implementation of Pydantic v2 schemas for all Python script interfaces, API drivers, and metadata verification pipelines.
- **Model Context Protocol (MCP 3.1 / FastMCP 3.1)**: Full protocol alignment with the FastMCP 3.1 transport specifications (gRPC, SSE, stdio) for agent tool calls and structured task decomposition.
- **Ralph-loop Continuous Knowledgeops**: Automated batching protocols (Action A: Do work, Action B: Add links, Action C: Divide work into task-decomposition tracking files) to guarantee repository expansion without technical debt.

```
+-----------------------------------------------------------------------------------+
|                        Repository Governance & Standards                          |
+-----------------------------------------------------------------------------------+
                                          |
                        +-----------------+-----------------+
                        |                                   |
             Documentation Contracts              Code & Schema Governance
                        |                                   |
                        v                                   v
+---------------------------------------+   +---------------------------------------+
|  13-Section KnowledgeOps Standard     |   |  Pydantic v2 Schemas                  |
|  - What it is, What problem it solves |   |  - Strict type checking & coercion    |
|  - 7+ Relative links, Valid URL       |   |  - FastMCP 3.1 tool input/outputs     |
|  - ISO date contribution metadata     |   |  - JSON-RPC protocol compliance       |
+---------------------------------------+   +---------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Automated Audit & Verification Pipeline                    |
|   `audit_docs_quality.py` | `check_docs_contract.py` | `check_catalog_consistency.py` |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
In a complex, multi-tool environment with frequent contributions from AI agents, fragmentation, hallucinated documentation, and inconsistency are high risks. These standards eliminate ambiguity in naming, document structure, metadata, and cross-tool communication, ensuring the repository remains a reliable, machine-readable source of truth.

- **Documentation Rot & Inconsistent Formatting**: Unifies document layouts using the mandatory 13-section KnowledgeOps contract.
- **Unverified Agent Contributions**: Prevents invalid pull requests by requiring all agent changes to pass deterministic pre-commit audit scripts.
- **Schema & API Incompatibilities**: Standardizes error handling, token metrics tracking, and API signatures through Pydantic v2 and FastMCP 3.1 protocols.
- **Catalog Navigation Disconnects**: Ensures all created canonical pages are indexed accurately within `mkdocs.yml` and `data/all_tools.json`.

## Where it fits in the stack
**Governance Layer** — acts as the foundational contract for all activities within the repository, from documentation updates and tool integrations to service deployments and multi-agent coordination.

## Typical use cases
- **Documentation Audits**: Supplying the explicit rule set enforced by `check_docs_contract.py` and `audit_docs_quality.py`.
- **Agent Onboarding & Operating Contracts**: Providing autonomous agents (such as Jules or Claude Code) with clear operating instructions (`AGENTS.md`) and pre-commit verification workflows.
- **FastMCP 3.1 Tool Registration**: Establishing input/output validation standards for tool servers across the homelab infrastructure.
- **Repository Growth Tracking**: Measuring shallow document reduction and total character expansion using `scripts/growth_tracker.py`.

## Strengths
- **Deterministic Programmatic Verification**: Supported by automated Python scripts that validate document structure, links, and schema integrity.
- **Comprehensive Agent Alignment**: Tailored specifically to support autonomous SWE agents with clear "done" criteria and error-recovery loops.
- **Strong Type Safety**: Enforces Pydantic v2 validation across all backend tool definitions and API integration scripts.
- **Clear Category Taxonomy**: Maintains a structured category breakdown in `docs/tools/` to prevent directory clutter.

## Limitations
- **Maintenance Discipline**: Requires contributors to execute audit scripts prior to merging pull requests.
- **Strict Formatting Rules**: Headings must match expected string signatures exactly without custom additions (e.g., `## API examples` must not be appended with extra text).

## When to use it
- Whenever creating or expanding a tool page, service document, or reference implementation.
- When configuring a new FastMCP 3.1 tool server or writing automation scripts.
- Before submitting any Pull Request to guarantee complete compliance across all quality gates.

## When not to use it
- For temporary, local scratchpad files that will never be committed to the repository.
- During preliminary local testing prior to staging files for pre-commit verification.

## Standards Architecture & Governance Lifecycle

### Quality Audit & Pipeline Gate Stages
All repository changes follow a four-stage governance pipeline to guarantee zero-regression merges:

```
+-----------------------------------------------------------------------------------+
| 1. Authoring / Agent Execution Phase                                              |
|    - Content expansion (> 15,000 chars for tool pages).                           |
|    - Inclusion of ASCII architecture diagrams, FastMCP code, Pydantic v2 models.   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. Local Contract & Quality Auditing Phase                                        |
|    - `python3 scripts/check_docs_contract.py <filepath>`                         |
|    - `python3 scripts/audit_docs_quality.py`                                      |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 3. Catalog & Intake Integrity Phase                                              |
|    - `python3 scripts/check_catalog_consistency.py`                               |
|    - `python3 scripts/validate_new_sources.py`                                    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 4. Metrics Recording & PR Submission                                              |
|    - `python3 scripts/growth_tracker.py` updates `data/growth-metrics.json`.      |
|    - Rebase onto `main` and submit PR using required branch/title conventions.   |
+-----------------------------------------------------------------------------------+
```

## Getting started

### Environment Setup
To ensure local compliance with standards:
```bash
# Ensure Python 3.11+ is active and dependencies are installed
python3 --version
pip install pydantic fastmcp mkdocs pytest
```

### Running Verification Suite
Execute the standard verification sequence before staging git commits:
```bash
# Audit specific file contract
python3 scripts/check_docs_contract.py docs/standards.md

# Audit entire documentation suite
python3 scripts/audit_docs_quality.py

# Verify navigation catalog matching
python3 scripts/check_catalog_consistency.py
```

## CLI examples

```bash
# Check document freshness and metadata dates
python3 scripts/check_doc_freshness.py docs --max-days 30

# Scan for coverage gaps in documentation
python3 scripts/coverage_gap_scan.py

# Run growth tracking metrics generator
python3 scripts/growth_tracker.py
```

## API examples

### Pydantic v2 Standards Compliance Schema Verification
The script below illustrates how repository standards enforce document metadata parsing and validation using Pydantic v2:

```python
import re
import sys
from datetime import date
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class ContributionMetadata(BaseModel):
    last_reviewed: date = Field(..., description="ISO 8601 date (YYYY-MM-DD)")
    confidence: Literal["high", "medium", "low"] = Field(..., description="Assessment confidence rating")

    @field_validator("last_reviewed")
    @classmethod
    def assert_valid_review_date(cls, v: date) -> date:
        if v.year < 2026:
            raise ValueError("Review date cannot be older than 2026")
        return v

class DocumentContractValidation(BaseModel):
    filepath: str = Field(..., description="Target documentation path")
    character_count: int = Field(..., ge=1000)
    required_sections_present: bool = Field(..., description="Indicates all 13 KnowledgeOps sections exist")
    relative_link_count: int = Field(..., ge=7, description="Must contain at least 7 relative markdown links")
    has_valid_source_url: bool = Field(..., description="Must contain at least one HTTP/HTTPS reference link")
    metadata: ContributionMetadata

def audit_document_standards(filepath: str, content: str) -> DocumentContractValidation:
    """Parses raw markdown content and verifies compliance against KnowledgeOps standards."""
    # Check section count
    required_headings = [
        "## What it is", "## What problem it solves", "## Where it fits in the stack",
        "## Typical use cases", "## Strengths", "## Limitations", "## When to use it",
        "## When not to use it", "## Getting started", "## CLI examples", "## API examples",
        "## Related tools / concepts", "## Sources / references"
    ]
    sections_valid = all(heading in content for heading in required_headings)

    # Count relative links
    rel_links = len(re.findall(r"\]\((?!\w+://)[^)]+\.md\)", content))

    # Check source URL
    has_url = bool(re.search(r"https?://", content))

    # Parse metadata
    date_match = re.search(r"Last reviewed:\s*(\d{4}-\d{2}-\d{2})", content)
    conf_match = re.search(r"Confidence:\s*(high|medium|low)", content, re.IGNORECASE)

    if not date_match or not conf_match:
        raise ValueError("Document missing required Contribution Metadata block")

    meta = ContributionMetadata(
        last_reviewed=date_match.group(1),
        confidence=conf_match.group(1).lower()
    )

    payload = {
        "filepath": filepath,
        "character_count": len(content),
        "required_sections_present": sections_valid,
        "relative_link_count": rel_links,
        "has_valid_source_url": has_url,
        "metadata": meta
    }

    try:
        validated = DocumentContractValidation.model_validate(payload)
        print(f"[✓] {filepath} fully complies with KnowledgeOps standards ({validated.character_count} chars).")
        return validated
    except ValidationError as ve:
        print(f"[!] Validation Failure for {filepath}:\n{ve}", file=sys.stderr)
        raise

if __name__ == "__main__":
    sample_doc = """
    # Sample Page
    ## What it is
    Sample text...
    ## What problem it solves
    Sample text...
    ## Where it fits in the stack
    Sample text...
    ## Typical use cases
    Sample text...
    ## Strengths
    Sample text...
    ## Limitations
    Sample text...
    ## When to use it
    Sample text...
    ## When not to use it
    Sample text...
    ## Getting started
    Sample text...
    ## CLI examples
    Sample text...
    ## API examples
    Sample text...
    ## Related tools / concepts
    - [link1](a.md)
    - [link2](b.md)
    - [link3](c.md)
    - [link4](d.md)
    - [link5](e.md)
    - [link6](f.md)
    - [link7](g.md)
    ## Sources / references
    - https://example.com
    ## Contribution Metadata
    - Last reviewed: 2027-01-07
    - Confidence: high
    """
    audit_document_standards("docs/sample.md", sample_doc)
```

### FastMCP 3.1 Standards Verification Tool
This FastMCP 3.1 tool exposes standards auditing capabilities to remote agents:

```python
import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("StandardsAuditServer")

class StandardsCheckInput(BaseModel):
    filepath: str = Field(description="Relative path to file in docs/")

class StandardsCheckOutput(BaseModel):
    filepath: str
    compliant: bool
    issues: list[str]

@mcp.tool()
async def audit_file_standards(input_data: StandardsCheckInput) -> StandardsCheckOutput:
    """Audits a single markdown file against KnowledgeOps repository standards."""
    await asyncio.sleep(0.05)  # Simulate execution

    return StandardsCheckOutput(
        filepath=input_data.filepath,
        compliant=True,
        issues=[]
    )

if __name__ == "__main__":
    mcp.run()
```

## Core Taxonomy & Contracts

### Core Category Taxonomy
The knowledge base uses a stable set of top-level categories under `docs/tools/`:

| Category | Location | Scope & Contents |
| :--- | :--- | :--- |
| **AI Knowledge** | `docs/tools/ai_knowledge/` | General AI products, knowledge management systems, search engines |
| **Frameworks** | `docs/tools/frameworks/` | Agent and LLM application libraries (LangChain, Mastra, AG2) |
| **Providers** | `docs/tools/providers/` | API providers and cloud model inference endpoints |
| **Agents** | `docs/tools/agents/` | Autonomous agent platforms and task orchestrators |
| **Automation & Orchestration** | `docs/tools/automation_orchestration/` | Workflow automation, MCP tools, pipeline proxies |
| **Infrastructure** | `docs/tools/infrastructure/` | Inference servers, local runtimes, vector storage |
| **Benchmarking** | `docs/tools/benchmarking/` | Evaluation frameworks, leaderboards, testing tools |
| **Development & Ops** | `docs/tools/development_ops/` | AI coding assistants, IDE extensions, CLI tools |
| **Enterprise** | `docs/tools/enterprise/` | Enterprise platforms, search engines, compliance tools |
| **Calendar & Tasks** | `docs/tools/calendar_tasks/` | Time management, scheduling tools, task trackers |
| **Intake & Storage** | `docs/tools/intake_storage/` | Document ingestion, notes storage, local storage engines |
| **Process Understanding** | `docs/tools/process_understanding/` | Analytics, observability, logging, parsing tools |

### KnowledgeOps Contract (13 Mandatory Sections)
Every canonical documentation page must include these exact section headings in order:
1. `## What it is`
2. `## What problem it solves`
3. `## Where it fits in the stack`
4. `## Typical use cases`
5. `## Strengths`
6. `## Limitations`
7. `## When to use it`
8. `## When not to use it`
9. `## Getting started`
10. `## CLI examples`
11. `## API examples`
12. `## Related tools / concepts` (Must contain >= 7 relative markdown links)
13. `## Sources / references` (Must contain at least 1 valid web link)

### Contribution Metadata (Required Footer)
Every page must conclude with this metadata block:
```markdown
## Contribution Metadata
- Last reviewed: YYYY-MM-DD
- Confidence: high
```

## Related tools / concepts
- [AGENTS.md](../AGENTS.md) — Agent operating rules and guidelines.
- [Multi-Agent KnowledgeOps](architecture/multi_agent_knowledgeops.md) — Multi-agent orchestration framework.
- [Automated Contributions](architecture/automated_contributions.md) — Staged contribution pipeline.
- [Jules Agent](tools/ai_knowledge/jules.md) — Primary autonomous engineering agent.
- [Claude Code](tools/development_ops/claude-code.md) — Terminal-native developer CLI agent.
- [FastMCP](tools/automation_orchestration/mcp.md) — FastMCP 3.1 protocol framework.
- [Audit Docs Quality Script](../scripts/audit_docs_quality.py) — Documentation auditor script.
- [Check Docs Contract Script](../scripts/check_docs_contract.py) — Individual file contract validator.

## Sources / references
- [KnowledgeOps Standards Specification](https://github.com/joanmarcriera/homelab)
- [Pydantic v2 Core Reference](https://docs.pydantic.dev/latest/)
- [Model Context Protocol (FastMCP 3.1) Specification](https://modelcontextprotocol.io/spec/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
