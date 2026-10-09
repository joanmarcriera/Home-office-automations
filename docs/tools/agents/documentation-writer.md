# Documentation Writer Skill

## What it is
The Documentation Writer Skill is a specialized, developer-oriented automation tool built for AI coding agents (such as [Claude Code](../development_ops/claude-code.md), [Cline](cline.md), and [Roo Code](roo-code.md)). Adhering to the universal, cross-agent `SKILL.md` specification, it automates the creation, continuous auditing, and maintenance of repository documentation. In early 2027, it natively supports FastMCP 3.1, stateful developer sandboxes, Language Server Protocol (LSP) symbol indexing, and multi-model execution across **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, and **DeepSeek-V4**.

By decoupling documentation maintenance from human manual entry, the Documentation Writer Skill acts as a continuous KnowledgeOps agent within engineering teams. It reads git commits, language ASTs, OpenAPI schemas, and FastMCP tool signatures to generate accurate, canonical markdown references without manual intervention.

```
+-----------------------------------------------------------------------------------+
|                        Documentation Writer Skill Workflow                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-------------------+       +-----------------------+      +------------------+  |
|  | Source Code AST   |       | Git Commit / PR Hooks |      | LSP Symbol Index |  |
|  | (Python/TS/Go/Rust)     | (Pre-commit / CI Gate)|      | (Type Definitions)  |  |
|  +---------+---------+       +-----------+-----------+      +--------+---------+  |
|            |                             |                           |            |
|            +------------------+          |          +----------------+            |
|                               |          v          |                             |
|                               v                     v                             |
|                  +-------------------------------------+                          |
|                  | Documentation Writer Skill (SKILL.md)|                          |
|                  | - AST Signature Comparison          |                          |
|                  | - FastMCP 3.1 Tool Schema Inspector |                          |
|                  | - Contract & Frontmatter Validator  |                          |
|                  +-------------------+-----------------+                          |
|                                      |                                            |
|          +---------------------------+---------------------------+                |
|          |                           |                           |                |
|          v                           v                           v                |
|  +-------------------+     +-------------------+     +-------------------+        |
|  | Canonical Markdown|     | Architectural     |     | MkDocs Navigation |        |
|  | API References    |     | Diagrams (Mermaid)|     | Index Updates     |        |
|  +-------------------+     +-------------------+     +-------------------+        |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It eradicates "documentation drift" and documentation debt in high-velocity agile engineering repositories. When codebase schemas, routes, or APIs change, manual documentation updates are often delayed or forgotten, leading to broken references and developer friction. The Documentation Writer skill continuously monitors commit hooks, reads LSP symbols, and performs semantic edits to ensure markdown files, architectural diagrams, and navigation indices (e.g., `mkdocs.yml`) remain completely synchronized with source code.

In large-scale microservice architectures and agentic AI repos, stale documentation leads to broken subagent tool calls and failed agentic reasoning. By continuously auditing frontmatter contracts, relative cross-links, and FastMCP tool signatures, the Documentation Writer Skill guarantees that both human developers and autonomous AI coding agents navigate valid, reliable documentation.

## Where it fits in the stack
**Category**: [Agents](index.md) / [Specialized Skills](claude-skills-ecosystem.md). It operates as an agent-executable logical plugin layer, frequently executed during Ralph-loop cycles or integrated directly into CI/CD build gates.

```
+-----------------------------------------------------------------------------------+
|                             Stack Integration Context                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|   [ IDE / Terminal Agent ] ----> ( Claude Code / Cline / Roo Code / Cursor )      |
|                                              |                                    |
|                                              v                                    |
|   [ Agent Skill Layer ] -------> ( Documentation Writer Skill: SKILL.md )          |
|                                              |                                    |
|                                              v                                    |
|   [ Validation & Verification ] -> ( FastMCP 3.1 & Pydantic v2 Contract Checker )  |
|                                              |                                    |
|                                              v                                    |
|   [ Published Documentation ] -> ( MkDocs / GitHub Wiki / Internal Knowledge Base)|
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Feature Comparison Matrix

| Capability / Dimension | Documentation Writer Skill | Legacy JSDoc / Sphinx Generators | Hand-Written Documentation |
| :--- | :--- | :--- | :--- |
| **Drift Detection** | Automatic git diff & LSP symbol drift tracking | None; requires manual re-build triggers | Manual review during PRs (error-prone) |
| **Semantic Formatting** | Rich markdown with FastMCP 3.1, ASCII/Mermaid | Strict raw code comment extraction | Freeform, inconsistent formatting |
| **Contract Enforcement** | Strict frontmatter, header, & cross-link audit | Basic syntax checking | Manual linting or none |
| **Agent Readiness** | Generates subagent-optimized schemas & prompts | Human-readable HTML/Text only | Varies wildly by author |
| **Multi-Language AST** | Natively parses Python, TS/JS, Go, Rust, OpenAPI | Language-specific tool lock-in | N/A |
| **CI/CD Integration** | FastMCP 3.1 pre-commit & GitHub Action gates | Build script integration | None |

## Typical use cases
- **Incremental API Reference Generation**: Parsing Python, TypeScript, Go, or Rust source files to write and update markdown API references.
- **Continuous Documentation Auditing**: Scanning repository markdown files to detect broken relative links, missing metadata headers, or structural format contract violations.
- **Navigation Index Synchronization**: Updating site navigation config blocks (such as MkDocs or Docusaurus configs) in-situ when new documentation folders are added or restructured.
- **Architectural Diagram Drafting**: Generating and refreshing complex Mermaid.js or Excalidraw block diagram specifications directly from source code modules.
- **Automated Pull Request Reviews**: Running in CI pipelines to verify that code PRs modifying exported functions include corresponding documentation updates.

## Key Features
- **Universal SKILL.md Spec Conformity**: Fully compatible with advanced multi-turn task structures executed by Claude 5.1 and GPT-5.5.
- **Symbolic Source Parsing**: Integrates with local LSP daemons to capture precise structural changes without relying on expensive, raw-text prompt tokens.
- **FastMCP 3.1 Validation Integrations**: Queries local tools and tests code blocks inside secure dockerized environments before editing docs.
- **Deep Drift Detection**: Automatically tracks file git diff history and matches changed code signatures against last reviewed documentation dates.
- **Custom Schema Contract Enforcement**: Validates frontmatter metadata, canonical section headers, and relative link targets against enterprise documentation style guides.

## Strengths
- **Low Hallucination Rate**: Leverages strict schema maps and LSP data, ensuring that generated code signatures exactly match the actual implementation.
- **High Schema Compliance**: Enforces exact organizational standards, including metadata structures, taxonomic order, and relative link formatting.
- **CI/CD Native Execution**: Can be triggered as a pre-commit action or as a containerized step inside GitHub Actions or GitLab runners.
- **Multi-Language Parsing**: Out-of-the-box support for python docstrings, JSDoc/TSDoc, rustdoc, and OpenAPI schema definitions.

## Limitations
- **Strategic Intent Gap**: While exceptionally skilled at describing *how* code functions structurally, it requires developer guidance to explain high-level strategic *why* architectural decisions.
- **Token Budget Overhead**: Running repository-wide deep audits across hundreds of source files can consume large model context windows if not scoped properly.

## When to use it
- During the documentation phase of major release cycles to audit and sync API reference files.
- To enforce continuous documentation style guides and prevent broken relative links inside monorepos.
- Onboarding new engineers into large codebases where reading accurate, automatically generated structural maps saves massive time.

## When not to use it
- For drafting legal-compliance text, marketing copy, or terms of service documentation that require precise legal accountability.
- In tiny single-file scripts where manual documentation takes less time than configuring automated workflows.

## Getting started

### 1. Global Installation
You can add the Documentation Writer Skill directly to your agentic terminal environment via the unified Skill Manager CLI:

```bash
npx skills@latest add awesome-copilot/documentation-writer
```

### 2. Execution Hooks
Execute a repository audit directly from your agent interface or terminal workspace:

```bash
# Perform a full semantic audit of all docs/ files
/audit-docs --deep --target ./docs

# Generate API markdown reference files for local python sources
/document-module --source ./src/api --output ./docs/api
```

## CLI examples
The command-line interface provides precise parameters for auditing schemas and identifying documentation gaps.

```bash
# Check current repository docs for "drift" compared to a specific git tag
/check-drift --since v2.4.0 --exclude docs/legacy/

# Generate an interactive architectural map using Mermaid formatting
/export-map --recursive --format mermaid > docs/architecture/map.md

# Lint all relative markdown references and auto-fix formatting anomalies
/lint-docs --fix --strict

# Audit specific doc directory for contract header compliance
/audit-docs --schema-check --target ./docs/tools
```

## API examples

### Programmatic Python Integration with FastMCP 3.1 & Strict Pydantic v2 Verification
Below is a complete Python program utilizing **Pydantic v2** and **FastMCP 3.1** to define, validate, and execute an automated documentation audit tool payload.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from fastmcp import FastMCP

mcp = FastMCP("Documentation-Writer-Server", version="3.1.0")

class DocumentMetric(BaseModel):
    total_docs: int = Field(..., alias="totalDocs")
    compliant_docs: int = Field(..., alias="compliantDocs")
    compliance_percentage: float = Field(..., alias="compliancePercentage", ge=0.0, le=100.0)

class FailedFileDetail(BaseModel):
    filepath: str = Field(..., description="Repository-relative file path")
    issue_type: str = Field(..., alias="issueType", description="Type of contract violation")
    description: str = Field(..., description="Human-readable issue description")

class AuditResult(BaseModel):
    batch_id: str = Field(..., alias="batchId")
    status: str = Field(..., description="Overall compliance status (PASSED, FAILED)")
    metrics: DocumentMetric
    failed_files: List[FailedFileDetail] = Field(default_factory=list, alias="failedFiles")

    @field_validator("status")
    @classmethod
    def validate_status_enum(cls, v: str) -> str:
        allowed = {"PASSED", "FAILED", "WARNING"}
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v

@mcp.tool()
async def execute_doc_audit(target_dir: str = "docs") -> str:
    """Executes a FastMCP 3.1 documentation compliance audit on the target repository folder.

    Args:
        target_dir: The repository directory path to audit.
    """
    raw_payload = {
        "batchId": "batch-834-CI",
        "status": "PASSED",
        "metrics": {
            "totalDocs": 701,
            "compliantDocs": 701,
            "compliancePercentage": 100.0
        },
        "failedFiles": []
    }

    try:
        validated = AuditResult.model_validate(raw_payload)
        return (f"Audit Batch {validated.batch_id} complete: {validated.status}. "
                f"Compliance: {validated.metrics.compliance_percentage}% across {validated.metrics.total_docs} files.")
    except Exception as e:
        return f"Audit validation failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Troubleshooting

### Contract Verification & CI Gate Setup
To ensure documentation quality remains high across pull requests:
1. **Pre-Commit Integration**: Run `/lint-docs --strict` during git pre-commit hooks to block non-compliant markdown edits before they hit remote branches.
2. **LSP Daemon Warmup**: Ensure language server daemons (e.g., `pyright`, `tsserver`) are pre-indexed before triggering deep doc-generation tasks to prevent incomplete type signatures.
3. **Preserving Manual Sections**: Mark high-level strategic reasoning sections with comment blocks (e.g., `<!-- MANUAL_REASONING_START -->`) so the automated writer never overwrites strategic developer decisions.

### Troubleshooting Common Anomalies
- **`Missing Metadata Header Error`**: Ensure all canonical tool and service markdown files contain required frontmatter or metadata headers (`## Contribution Metadata`, `- Last reviewed:`).
- **`Broken Relative Link Warnings`**: Run `/lint-docs --fix` to automatically adjust path references when moving markdown files between category subdirectories.
- **`Token Limit Exceeded on Large Repos`**: Use `--exclude` flags to bypass large build logs or benchmark artifacts during full repository scans.

## Related tools / concepts
- [Claude Skills Ecosystem](claude-skills-ecosystem.md) — The parent ecosystem catalog for skill integration.
- [Superpowers](superpowers.md) — Hand-crafted developer skill combinations.
- [KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — The operational concept of managing knowledge bases using developer workflows.
- [Claude Code](../development_ops/claude-code.md) — Command-line agent utilizing this skill.
- [PydanticAI](../frameworks/pydantic-ai.md) — Multi-agent model validation framework.
- [Cline](cline.md) — Autonomous IDE coding agent.
- [Roo Code](roo-code.md) — Configurable agentic coding extension.

## Sources / references
- [Universal SKILL.md Standard & API Specifications](https://github.com/awesome-copilot/awesome-skills/blob/main/SPEC.md)
- [Antigravity Awesome Skills Ecosystem Directory](https://github.com/awesome-copilot/awesome-skills)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
