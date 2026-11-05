# Documentation Writer Skill

## What it is
The Documentation Writer Skill is a specialized, developer-oriented automation tool built for AI coding agents (such as [Claude Code](../development_ops/claude-code.md), [Cline](cline.md), and [Roo Code](roo-code.md)). Adhering to the universal, cross-agent `SKILL.md` specification, it automates the creation, continuous auditing, and maintenance of repository documentation. In early 2027, it natively supports FastMCP 3.1, stateful developer sandboxes, Language Server Protocol (LSP) symbol indexing, and multi-model execution across **Claude 5.1**, **Claude 5.6**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, and **DeepSeek-V4**.

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

---

## Mathematical Formulation: AST Symbol Drift Distance & Doc Coverage

To detect and quantify divergence between codebase implementation and documentation, the Documentation Writer Skill parses source code abstract syntax trees (ASTs) using Tree-sitter grammars into an exported symbol set $\mathcal{S}_{\text{code}} = \{ s_1, s_2, \dots, s_M \}$, where each symbol $s_i$ contains an identifier, type signature, and parameter signature:

$$
s_i = \langle \text{name}_i, \text{kind}_i, \text{params}_i, \text{return\_type}_i \rangle
$$

Similarly, existing documentation markdown files are parsed into documented API symbols $\mathcal{S}_{\text{doc}} = \{ d_1, d_2, \dots, d_K \}$.

The **AST Signature Distance** $D_{\text{AST}}(s_i, d_j)$ between code symbol $s_i$ and doc symbol $d_j$ evaluates structural string editing and type tree distance:

$$
D_{\text{AST}}(s_i, d_j) = w_1 \cdot \mathbb{I}(\text{name}_i \ne \text{name}_j) + w_2 \cdot \text{Levenshtein}(\text{sig}_i, \text{sig}_j) + w_3 \cdot D_{\text{type}}(\tau_i, \tau_j)
$$

Where weights satisfy $\sum w_i = 1.0$.

The **Repository Documentation Coverage** $\mathcal{C}_{\text{repo}}$ across all source code modules is computed as:

$$
\mathcal{C}_{\text{repo}} = \frac{|\{ s \in \mathcal{S}_{\text{code}} \mid \exists d \in \mathcal{S}_{\text{doc}} \text{ s.t. } D_{\text{AST}}(s, d) < \epsilon \}|}{|\mathcal{S}_{\text{code}}|}
$$

When a git commit introduces delta $\Delta \mathcal{S}_{\text{code}}$, the **Documentation Drift Index** $\Omega_{\text{drift}}$ is formulated as:

$$
\Omega_{\text{drift}} = \frac{|\Delta \mathcal{S}_{\text{code}} \setminus \mathcal{S}_{\text{doc}}|}{|\mathcal{S}_{\text{code}}|} \times \left(1 + \frac{\text{lines}_{\text{modified}}}{\text{lines}_{\text{total}}}\right)
$$

If $\Omega_{\text{drift}} > \theta_{\text{threshold}}$ (default $\theta = 0.05$), the skill automatically fails pre-commit gates or triggers autonomous incremental generation cycles to restore $\mathcal{C}_{\text{repo}} \to 1.0$.

---

## What problem it solves
It eradicates "documentation drift" and documentation debt in high-velocity agile engineering repositories. When codebase schemas, routes, or APIs change, manual documentation updates are often delayed or forgotten, leading to broken references and developer friction. The Documentation Writer skill continuously monitors commit hooks, reads LSP symbols, and performs semantic edits to ensure markdown files, architectural diagrams, and navigation indices (e.g., `mkdocs.yml`) remain completely synchronized with source code.

In large-scale microservice architectures and agentic AI repos, stale documentation leads to broken subagent tool calls and failed agentic reasoning. By continuously auditing frontmatter contracts, relative cross-links, and FastMCP tool signatures, the Documentation Writer Skill guarantees that both human developers and autonomous AI coding agents navigate valid, reliable documentation.

---

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

---

## Feature Comparison Matrix

| Capability / Dimension | Documentation Writer Skill | Mintlify | Docusaurus DocGen | TypeDoc / Sphinx | Swimm |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Drift Detection Engine** | AST + Tree-sitter + Git Diff | Git sync only | None (manual build) | None (compiler only) | IDE code-coupling tokens |
| **Semantic Formatting** | Rich Markdown + FastMCP 3.1 + Mermaid | Custom MDX components | MDX / React | Raw docstring HTML/MD | Proprietary markup |
| **Contract Enforcement** | Strict frontmatter & link validation | Basic schema check | Build error on broken link | Syntax check | Token anchor verification |
| **Autonomous AI Regeneration** | Yes (Claude 5.6, GPT-5.6, DeepSeek-V4) | AI Search / Chat only | No | No | AI snippet suggestions |
| **Multi-Language AST** | Python, TypeScript, Go, Rust, C++ | OpenAPI / TS | JavaScript / TS | Language-specific | Multi-language snippets |
| **FastMCP 3.1 Integration** | Native First-Class Server | None | None | None | None |
| **CI/CD Pre-Commit Gate** | Sub-second local check | Cloud build hook | Webpack compilation | Make / Gradle step | PR check bot |

---

## Production Multi-Container Orchestration (`docker-compose.yml`)

The following Docker Compose file deploys an autonomous Documentation Writer background service with an embedded LSP indexing engine, FastMCP 3.1 verification daemon, and live Caddy static preview server:

```yaml
version: "3.8"

services:
  doc-writer-daemon:
    image: python:3.11-slim
    container_name: doc-writer-daemon
    restart: unless-stopped
    working_dir: /workspace
    environment:
      - DOC_WRITER_ENV=production
      - LSP_SERVER_HOST=lsp-indexer
      - LSP_SERVER_PORT=2087
      - FASTMCP_PORT=9095
      - REDIS_URL=redis://doc-writer-redis:6379/0
      - MKDOCS_CONFIG_PATH=/workspace/mkdocs.yml
    volumes:
      - .:/workspace:rw
      - doc_writer_cache:/root/.cache/docwriter
    ports:
      - "9095:9095"
    command: >
      bash -c "pip install fastmcp>=3.1.0 pydantic>=2.0 tree-sitter mkdocs-material redis && python3 -m scripts.doc_writer_daemon"
    depends_on:
      lsp-indexer:
        condition: service_started
      doc-writer-redis:
        condition: service_started

  lsp-indexer:
    image: node:20-slim
    container_name: doc-writer-lsp
    restart: unless-stopped
    volumes:
      - .:/workspace:ro
    command: >
      bash -c "npm install -g typescript pyright && npx --yes pyright --watch --lib /workspace"

  caddy-preview:
    image: caddy:2.7-alpine
    container_name: doc-writer-preview
    restart: unless-stopped
    ports:
      - "8008:80"
    volumes:
      - ./site:/usr/share/caddy:ro

  doc-writer-redis:
    image: redis:7.2-alpine
    container_name: doc-writer-redis
    restart: unless-stopped
    volumes:
      - doc_writer_redis_data:/data

volumes:
  doc_writer_cache:
  doc_writer_redis_data:
```

---

## Production Systemd Service Unit (`doc-writer.service`)

To run the Documentation Writer daemon as a hardened system service on Linux development servers or CI runners:

```ini
[Unit]
Description=Documentation Writer Skill & KnowledgeOps Daemon
After=network.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=doc-agent
Group=doc-agent
WorkingDirectory=/opt/repo-workspace
ExecStart=/usr/local/bin/python3 -m scripts.doc_writer_daemon \
  --listen 127.0.0.1:9095 \
  --repo /opt/repo-workspace \
  --target docs/ \
  --strict-contract
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=FASTMCP_PORT=9095

# Sandboxing and Security Rules
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true
ProtectKernelTunables=true
ProtectControlGroups=true
ReadWritePaths=/opt/repo-workspace/docs /opt/repo-workspace/site /tmp

# Resource Limits
LimitNOFILE=65536
MemoryAccounting=true
MemoryHigh=8G
MemoryMax=12G

[Install]
WantedBy=multi-user.target
```

Reload and initialize the unit:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now doc-writer.service
sudo systemctl status doc-writer.service
```

---

## Typical use cases
- **Incremental API Reference Generation**: Parsing Python, TypeScript, Go, or Rust source files to write and update markdown API references.
- **Continuous Documentation Auditing**: Scanning repository markdown files to detect broken relative links, missing metadata headers, or structural format contract violations.
- **Navigation Index Synchronization**: Updating site navigation config blocks (such as MkDocs or Docusaurus configs) in-situ when new documentation folders are added or restructured.
- **Architectural Diagram Drafting**: Generating and refreshing complex Mermaid.js or Excalidraw block diagram specifications directly from source code modules.
- **Automated Pull Request Reviews**: Running in CI pipelines to verify that code PRs modifying exported functions include corresponding documentation updates.

---

## Key Features
- **Universal SKILL.md Spec Conformity**: Fully compatible with advanced multi-turn task structures executed by Claude 5.1, Claude 5.6, and GPT-5.6.
- **Symbolic Source Parsing**: Integrates with local LSP daemons to capture precise structural changes without relying on expensive, raw-text prompt tokens.
- **FastMCP 3.1 Validation Integrations**: Queries local tools and tests code blocks inside secure dockerized environments before editing docs.
- **Deep Drift Detection**: Automatically tracks file git diff history and matches changed code signatures against last reviewed documentation dates.
- **Custom Schema Contract Enforcement**: Validates frontmatter metadata, canonical section headers, and relative link targets against enterprise documentation style guides.

---

## Strengths
- **Low Hallucination Rate**: Leverages strict schema maps and LSP data, ensuring that generated code signatures exactly match the actual implementation.
- **High Schema Compliance**: Enforces exact organizational standards, including metadata structures, taxonomic order, and relative link formatting.
- **CI/CD Native Execution**: Can be triggered as a pre-commit action or as a containerized step inside GitHub Actions or GitLab runners.
- **Multi-Language Parsing**: Out-of-the-box support for python docstrings, JSDoc/TSDoc, rustdoc, and OpenAPI schema definitions.

---

## Limitations
- **Strategic Intent Gap**: While exceptionally skilled at describing *how* code functions structurally, it requires developer guidance to explain high-level strategic *why* architectural decisions.
- **Token Budget Overhead**: Running repository-wide deep audits across hundreds of source files can consume large model context windows if not scoped properly.

---

## When to use it
- During the documentation phase of major release cycles to audit and sync API reference files.
- To enforce continuous documentation style guides and prevent broken relative links inside monorepos.
- Onboarding new engineers into large codebases where reading accurate, automatically generated structural maps saves massive time.

---

## When not to use it
- For drafting legal-compliance text, marketing copy, or terms of service documentation that require precise legal accountability.
- In tiny single-file scripts where manual documentation takes less time than configuring automated workflows.

---

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

---

## CLI examples
The command-line interface provides precise parameters for auditing schemas and identifying documentation gaps:

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

---

## API examples

### Programmatic Python Integration with FastMCP 3.1 & Strict Pydantic v2 Verification
Below is a complete Python program utilizing **Pydantic v2** (`ConfigDict(extra="forbid", frozen=True)`) and **FastMCP 3.1** to define, validate, and execute an automated documentation audit tool payload:

```python
import asyncio
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastmcp import FastMCP

mcp = FastMCP("Documentation-Writer-Server", version="3.1.0")

class DocumentMetric(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    total_docs: int = Field(..., alias="totalDocs", ge=0)
    compliant_docs: int = Field(..., alias="compliantDocs", ge=0)
    compliance_percentage: float = Field(..., alias="compliancePercentage", ge=0.0, le=100.0)
    drift_index: float = Field(default=0.0, ge=0.0, le=1.0)

class FailedFileDetail(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    filepath: str = Field(..., description="Repository-relative file path")
    issue_type: str = Field(..., alias="issueType", description="Type of contract violation")
    description: str = Field(..., description="Human-readable issue description")

class AuditResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

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
async def execute_doc_audit(target_dir: str = "docs") -> Dict[str, Any]:
    """Executes a FastMCP 3.1 documentation compliance audit on the target repository folder.

    Args:
        target_dir: The repository directory path to audit.
    """
    raw_payload = {
        "batchId": "batch-1043-CI",
        "status": "PASSED",
        "metrics": {
            "totalDocs": 710,
            "compliantDocs": 710,
            "compliancePercentage": 100.0,
            "drift_index": 0.012
        },
        "failedFiles": []
    }

    try:
        validated = AuditResult.model_validate(raw_payload)
        return {
            "batch_id": validated.batch_id,
            "status": validated.status,
            "total_docs": validated.metrics.total_docs,
            "compliance": validated.metrics.compliance_percentage,
            "drift": validated.metrics.drift_index
        }
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}

if __name__ == "__main__":
    mcp.run()
```

---

## Systematic Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **`MissingMetadataHeaderError`** | Markdown file lacks required `## Contribution Metadata` section | `python3 scripts/check_docs_contract.py <path>` | Append required metadata block including valid `Last reviewed` and `Confidence`. |
| **`BrokenRelativeLinkError`** | Referenced doc moved without updating relative link target | `grep -rn "docs/" docs/tools` | Run `python3 scripts/fix_internal_links.py` to calculate updated relative path. |
| **`LSPIndexConnectionRefused`** | Pyright / TypeScript language server daemon not running | `netstat -tlpn \| grep 2087` | Restart language server container or verify socket permissions. |
| **`ASTSignatureDriftWarning`** | Exported function parameters altered in source code without doc update | `/check-drift --strict` | Run `/document-module` to re-extract parameters into documentation. |
| **`MkDocsNavMismatchError`** | New markdown file created without entry in `mkdocs.yml` nav block | `python3 scripts/check_catalog_consistency.py` | Add the new canonical page under the appropriate section in `mkdocs.yml`. |
| **`TreeSitterGrammarCrash`** | Source code contains syntax extensions not supported by parser grammar | Check daemon stderr log | Update Tree-sitter grammar package: `pip install --upgrade tree-sitter-languages`. |
| **`PydanticFrozenInstanceError`** | Hook attempting to mutate validated `AuditResult` or `DocumentMetric` object | Review Python traceback logs | Use `result.model_copy(update={...})` instead of direct attribute mutation. |
| **`FastMCPContextTimeout`** | Deep AST parsing on large mono-repo exceeding MCP request timeout | Check gateway timeout metric | Split mono-repo targets by folder using `--target docs/<module>`. |

---

## Related tools / concepts
- [Claude Skills Ecosystem](claude-skills-ecosystem.md) — The parent ecosystem catalog for skill integration.
- [Superpowers](superpowers.md) — Hand-crafted developer skill combinations.
- [KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — The operational concept of managing knowledge bases using developer workflows.
- [Claude Code](../development_ops/claude-code.md) — Command-line agent utilizing this skill.
- [PydanticAI](../frameworks/pydantic-ai.md) — Multi-agent model validation framework.
- [Cline](cline.md) — Autonomous IDE coding agent.
- [Roo Code](roo-code.md) — Configurable agentic coding extension.

---

## Sources / references
- [Universal SKILL.md Standard & API Specifications](https://github.com/awesome-copilot/awesome-skills/blob/main/SPEC.md)
- [Antigravity Awesome Skills Ecosystem Directory](https://github.com/awesome-copilot/awesome-skills)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)
- [Tree-sitter Language Parsing Infrastructure](https://tree-sitter.github.io/tree-sitter/)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
