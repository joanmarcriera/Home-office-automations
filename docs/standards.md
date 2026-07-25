# Standards and Conventions

## What it is
This document defines the technical standards and operational conventions for the homelab automation stack. It ensures interoperability between diverse tools, maintains documentation quality, and provides a clear protocol for autonomous agents and human contributors.

## What problem it solves
In a complex, multi-tool environment with frequent contributions from AI agents, fragmentation and inconsistency are high risks. These standards eliminate ambiguity in naming, document structure, metadata, and cross-tool communication, ensuring the repository remains a reliable source of truth.

## Where it fits in the stack
**Governance Layer** — acts as the foundational contract for all activities within the repository, from documentation updates to new service deployments.

## Typical use cases
- **Documentation Audits**: Providing the criteria used by scripts like `check_docs_contract.py` to verify page quality.
- **Agent Onboarding**: Giving new AI agents (e.g., Claude 5.1) the "rules of the road" for how to contribute safely and effectively.
- **Workflow Design**: Setting the expectations for how n8n workflows should be named and how data should be formatted.
- **Model Evaluation**: Standardizing the benchmarks and metrics used by GPT-5.5 and Llama 4 for self-correction.

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
While standards are primarily documentation-based, they are enforced via scripts that use the following logic.

### Metadata Extraction (Python)
```python
import re

def get_last_reviewed(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        match = re.search(r"Last reviewed:\s*(\d{4}-\d{2}-\d{2})", content)
        return match.group(1) if match else None

# Example usage
# date = get_last_reviewed("docs/standards.md")
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
            "standards_version": "2026.8",
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
- Last reviewed: 2026-08-31
- Confidence: high
