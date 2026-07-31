# Documentation Writer Skill

## What it is
The Documentation Writer Skill is a highly specialized developer-oriented automation tool designed for next-generation AI coding agents (such as Claude Code, Cursor, and Gemini CLI). Adhering to the universal, cross-agent `SKILL.md` specification, it automates the creation, continuous auditing, and maintenance of repository documentation. It is fully updated for late October / November 2026, natively supporting Model Context Protocol (MCP 3.1), FastMCP 3.1, and stateful developer sandboxes.

## What problem it solves
It eradicates "documentation drift" and documentation debt in high-velocity agile repositories. When codebase schemas, routes, or APIs change, documentation rarely stays synchronized, causing developer friction. This skill continuously monitors commit hooks, reads Language Server Protocol (LSP) symbols, and performs semantic edits to ensure markdown files, architectural diagrams, and site indices (e.g., `mkdocs.yml`) remain completely accurate.

## Where it fits in the stack
**Category**: [Agents](index.md) / [Specialized Skills](claude-skills-ecosystem.md). It operates as an agent-executable logical plugin layer, frequently executed during Ralph-loop cycles or integrated directly into CI/CD build gates.

## Typical use cases
- **Incremental Codebase Mapping**: Automatically parsing Python, TypeScript, or Go source files to write and update markdown API references.
- **Continuous Documentation Auditing**: Scanning repository markdown files to detect broken relative links, missing metadata headers, or structural format violations.
- **KnowledgeOps Navigation Syncing**: Modifying site navigation config blocks (such as MkDocs or Docusaurus configs) in-situ when new documentation folders are created.
- **Architectural Diagram Drafting**: Generating and refreshing complex Mermaid.js or Excalidraw block diagram specifications from source module changes.

## Key Features (late 2026 Update)
- **Universal SKILL.md Spec Conformity**: Fully compatible with advanced multi-turn task structures executed by Claude 5.1 and GPT-5.5.
- **Symbolic Source Parsing**: Integrates with local LSP daemons to capture precise structural changes instead of relying on expensive, raw-text prompt tokens.
- **FastMCP 3.1 Validation Integrations**: Queries local tools and tests code blocks inside a secure dockerized environment before editing docs.
- **Deep Drift Detection**: Automatically tracks file git diff history and matches changed code signatures against last reviewed documentation dates.

## Strengths
- **Low Hallucination Rate**: Leverages strict schema maps and LSP data, ensuring that generated code signatures exactly match the actual implementation.
- **High Schema Compliance**: Enforces exact organizational standards, including metadata structures, taxonomic order, and relative link formatting.
- **CI/CD native execution**: Can be triggered as a pre-commit action or as a Docker container task inside GitHub Actions or GitLab runners.
- **Multi-lingual parsing**: Out-of-the-box support for python docstrings, JSDoc, rustdoc, and swagger/openapi schema definitions.

## Limitations
- **Strategic Intent Gap**: While exceptionally skilled at describing *how* code functions structurally, it still requires human input to explain strategic *why* decisions and business logic.
- **Token Budget Overhead**: Running repository-wide deep audits across hundreds of source files can quickly consume large model context spaces.

## When to use it
- During the documentation phase of a major release cycle to audit and sync API files.
- To enforce continuous documentation style guides and prevent broken relative links inside monorepos.
- Onboarding new engineers into large codebases where reading accurate, automatically generated structural maps saves massive time.

## When not to use it
- For drafting legal-compliance text, product copywriting, or terms of service documentation that require precise human accountability.
- In tiny, low-frequency personal scripts where manual documentation takes less time than configuring automated workflows.

## Getting started

### 1. Global Installation
You can add the Documentation Writer Skill directly to your agentic terminal environment via the Antigravity Awesome Skills installer:

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
```

## API examples
Below is a complete Python program utilizing `pydantic` (v2) to define, validate, and parse a documentation audit metadata payload generated by the Documentation Writer's background analyzer.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field

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
    status: str = Field(..., description="Overall compliance status (e.g., PASSED, FAILED)")
    metrics: DocumentMetric
    failed_files: List[FailedFileDetail] = Field(default_factory=list, alias="failedFiles")

async def parse_audit_results():
    # Simulated JSON payload representing the output of an automated CI doc audit
    raw_payload = {
        "batchId": "batch-281-CI",
        "status": "FAILED",
        "metrics": {
            "totalDocs": 553,
            "compliantDocs": 552,
            "compliancePercentage": 99.82
        },
        "failedFiles": [
            {
                "filepath": "docs/tools/ai_knowledge/legacy-tool.md",
                "issueType": "MISSING_CONTRIBUTION_METADATA",
                "description": "File is missing required 'Last reviewed' header line"
            }
        ]
    }

    # Pydantic v2 schema-enforced validation
    validated_report = AuditResult.model_validate(raw_payload)
    print(f"CI Document Audit Result Parsed for Batch: {validated_report.batch_id}")
    print(f"Overall Status: {validated_report.status}")
    print(f"Compliance: {validated_report.metrics.compliance_percentage}%")
    if validated_report.failed_files:
        print("Contract Violations Found:")
        for failure in validated_report.failed_files:
            print(f"  - {failure.filepath}: [{failure.issue_type}] {failure.description}")

if __name__ == "__main__":
    asyncio.run(parse_audit_results())
```

## Related tools / concepts
- [Claude Skills Ecosystem](claude-skills-ecosystem.md) — The parent ecosystem catalog for skill integration.
- [Superpowers](superpowers.md) — Hand-crafted developer skill combinations.
- [KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — The operational concept of managing knowledge bases using developer workflows.
- [Claude Code](../development_ops/claude-code.md) — SOTA command-line agent utilizing this skill.
- [PydanticAI](../frameworks/pydantic-ai.md) — Multi-agent model validation framework.
- [big-AGI](../ai_knowledge/big-agi.md) — GUI multi-model console workspace.

## Sources / references
- [Universal SKILL.md Standard & API Specifications](https://github.com/awesome-copilot/awesome-skills/blob/main/SPEC.md)
- [Antigravity Awesome Skills Ecosystem Directory](https://github.com/awesome-copilot/awesome-skills)
- [AI Agent Developer Skills Guide (2026 edition)](https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
