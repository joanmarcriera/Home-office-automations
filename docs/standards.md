# Standards and Conventions

## What it is
This document defines the technical standards and operational conventions for the homelab automation stack. It ensures interoperability between diverse tools, maintains documentation quality, and provides a clear protocol for autonomous agents and human contributors.

Key updates for the early January 2027 ecosystem include:
- **Foundational LLM Standards**: Multi-agent alignment across frontier models (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, Qwen 3.6 VL, and FastMCP 3.1).
- **Enforced Schema Validation**: Standardization of all API integration scripts using strict Pydantic v2 schemas.
- **Model Context Protocol (FastMCP 3.1) Task Protocol**: Full alignment with the FastMCP 3.1 Task Protocol JSON schema for multi-agent execution pipelines and structured tool tracking.

## What problem it solves
In a complex, multi-tool environment with frequent contributions from AI agents, fragmentation and inconsistency are high risks. These standards eliminate ambiguity in naming, document structure, metadata, and cross-tool communication, ensuring the repository remains a reliable source of truth.

## Where it fits in the stack
**Governance Layer** — acts as the foundational contract for all activities within the repository, from documentation updates to new service deployments.

## Typical use cases
- **Documentation Audits**: Providing the criteria used by scripts like `check_docs_contract.py` to verify page quality.
- **Agent Onboarding**: Giving new AI agents (e.g., Claude 5.6) the "rules of the road" for how to contribute safely and effectively.
- **Workflow Design**: Setting the expectations for how n8n workflows should be named and how data should be formatted.
- **Model Evaluation**: Standardizing the benchmarks and metrics used by GPT-5.6, DeepSeek-V4, and Qwen 3.6 VL for self-correction.

## Strengths
- **Consistency**: Enforces a uniform "look and feel" across hundreds of documentation pages.
- **Automation-Friendly**: Standards are defined with programmatic verification in mind (using Python scripts).
- **Interoperability**: Standardized data formats (JSON) and date types (ISO8601) simplify tool integration.

## Limitations
- **Overhead**: Requires contributors to follow specific steps (registry updates, metadata additions) which can be slower for manual edits.
- **Enforcement Gap**: While many standards are script-verified, some (like "one canonical page") still require human or advanced AI judgment.

## When to use it
- Whenever creating a new tool page or reference implementation.
- When designing a new n8n workflow or drafting a system prompt.
- Before submitting a Pull Request to ensure all quality gates pass.

## When not to use it
- For temporary, local-only notes that will not be merged into the repository.
- During rapid prototyping where speed is prioritized over documentation (though standards should be retrofitted before merge).

## Getting started
### Repository Setup
1. Clone the repository and install dependencies using Poetry or native package tools.
2. Ensure you have the latest Python version (3.11+) and `mkdocs` installed.
3. Run `python3 find_oldest_issues.py` to identify pending tasks.

### Multi-Agent Interaction
Agents must adhere to the `AGENTS.md` operating contract, which takes precedence in cases of conflict regarding agentic behavior.

## CLI examples
Standards can be verified using the following CLI tools.

```bash
# Verify the KnowledgeOps contract for a specific file
python3 scripts/check_docs_contract.py docs/tools/ai_knowledge/claude.md

# Run a full quality audit across the repository
python3 scripts/audit_docs_quality.py

# Find documentation pages that are stale or missing metadata
python3 scripts/check_doc_freshness.py docs --max-days 30
```

## API examples
The following Python script demonstrates programmatic validation of document metadata using Pydantic v2 schemas and mock FastMCP 3.1 task integration.

```python
import re
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class DocMetadata(BaseModel):
    filepath: str = Field(..., description="Relative path of the document")
    last_reviewed: date = Field(..., description="ISO 8601 format review date")
    confidence: Literal["high", "medium", "low"] = Field(..., description="Confidence level")

    @field_validator("last_reviewed")
    @classmethod
    def validate_recent_date(cls, v: date) -> date:
        if v.year < 2026:
            raise ValueError("Review date must be within or after 2026")
        return v

def extract_and_validate_metadata(filepath: str, content: str) -> DocMetadata:
    """Parses and validates document metadata using Pydantic v2."""
    date_match = re.search(r"Last reviewed:\s*(\d{4}-\d{2}-\d{2})", content)
    conf_match = re.search(r"Confidence:\s*(high|medium|low)", content, re.IGNORECASE)

    if not date_match or not conf_match:
        raise ValueError("Missing required contribution metadata fields")

    return DocMetadata(
        filepath=filepath,
        last_reviewed=date_match.group(1),
        confidence=conf_match.group(1).lower()
    )

# Example Verification Usage:
if __name__ == "__main__":
    sample_content = """
    # Sample Page
    ## Contribution Metadata
    - Last reviewed: 2027-01-07
    - Confidence: high
    """

    try:
        metadata = extract_and_validate_metadata("docs/sample.md", sample_content)
        print("Validation Succeeded:", metadata.model_dump_json(indent=2))
    except Exception as e:
        print("Validation Failed:", str(e))
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
- [AGENTS.md](../AGENTS.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [Multi-Agent KnowledgeOps](architecture/multi_agent_knowledgeops.md)
- [n8n Service](services/n8n.md)
- [Paperless-ngx](services/paperless-ngx.md)
- [Audit Docs Quality Script](../scripts/audit_docs_quality.py)
- [Check Docs Contract Script](../scripts/check_docs_contract.py)
- [Claude Code](tools/development_ops/claude-code.md)
- [Model Context Protocol (MCP)](tools/automation_orchestration/mcp.md)

## Sources / references
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [n8n Best Practices](https://docs.n8n.io/workflows/best-practices/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
