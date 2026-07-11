# Documentation Writer Skill

## What it is
A specialized skill for AI agents (Claude Code, Cursor, Gemini CLI, etc.), designed to automate the creation, auditing, and maintenance of project documentation. It follows the universal `SKILL.md` format and integrates directly with agentic development workflows, fully supporting [Gemma 3](../ai_knowledge/local_llms.md) and [MCP 3.0](../../tools/automation_orchestration/mcp.md).

## What problem it solves
Documentation rot is a major issue in fast-moving projects. This skill ensures that READMEs, API references, architecture diagrams, and changelogs stay synchronized with the actual source code, reducing technical debt and onboarding friction.

## Where it fits in the stack
**Category**: [Agents](index.md) / [Specialized Skills](claude-skills-ecosystem.md). It acts as a documentation-specific playbook for the agent, often leveraged during Ralph-loop cycles.

## Typical use cases
- **Full Repository Audit**: Scanning the codebase to identify missing documentation or outdated sections.
- **Automated API Reference**: Generating docstrings and markdown files from function/class definitions.
- **KnowledgeOps Sync**: Updating repository indexes and site navigation (e.g., `mkdocs.yml`) based on new files.
- **Visual Mapping**: Generating Mermaid or Excalidraw diagram definitions to visualize architecture.

## Key Features (July 2026 Update)
- **Universal SKILL.md Support**: Compatible with the latest cross-agent skill standard used by Claude Code, Cursor, and [Gemma 3](../ai_knowledge/local_llms.md).
- **Symbolic Analysis**: Uses LSP (Language Server Protocol) data to provide deeper, more accurate code explanations than raw text analysis.
- **Documentation Linting**: Automatically checks for broken relative links, missing metadata, and taxonomy violations.
- **MCP 3.0 Task Protocol**: Native integration with Model Context Protocol for cross-tool documentation workflows.

## Strengths
- **Frontier Intelligence**: Optimized for **Claude 4.8**, **GPT-5.5**, and **Gemma 3**, ensuring deep understanding of complex architectural patterns.
- **Workflow Integration**: Can be triggered as a post-commit hook or as part of a CI/CD pipeline.
- **Taxonomy Compliance**: Enforces project-specific documentation standards (e.g., [KnowledgeOps](../../standards-and-conventions.md)).
- **Zero Drift**: Detects when code changes without corresponding documentation updates.

## Limitations
- **Design Intent**: While it can describe *what* code does, it may still require human input for the *why* behind strategic design decisions.
- **Token Usage**: Large-scale repository audits can consume significant context window space.

## When to use it
- During the "Documentation Phase" of a sprint or Ralph-loop run.
- When onboarding a new contributor to a complex, poorly documented repository.
- To maintain high-quality `README.md` and `ARCHITECTURE.md` files in open-source projects.

## When not to use it
- For legal, medical, or security-compliance documentation that requires strict human accountability.
- In extremely small projects where manual documentation takes less time than configuring the skill.

## Getting started

### Installation
Install the skill using the [Antigravity Awesome Skills](https://github.com/awesome-copilot/awesome-skills) installer:

```bash
npx skills@latest add awesome-copilot/documentation-writer
```

### Basic Commands
Trigger the skill from within your agent terminal:

```bash
/document-codebase --deep
```

Document a specific module:
```bash
/document-module src/auth/
```

Audit existing documentation for freshness:
```bash
/audit-docs
```

## CLI examples
The `documentation-writer` skill is often invoked via the agent's CLI or integrated terminal.

```bash
# Generate documentation for all Python files in the current directory
/document-python --recursive

# Check for documentation drift against the latest git commit
/check-drift --since HEAD~1

# Export the current repository map to a Mermaid diagram
/export-map --format mermaid > docs/architecture/map.md
```

## API examples
When used within a programmable agent framework, the documentation writer can be controlled via API.

```python
from skills.documentation_writer import DocumentationAuditor

# Initialize the auditor for the current repository
auditor = DocumentationAuditor(repo_path=".")

# Run a freshness audit and get a list of stale files
stale_files = auditor.run_audit(depth="deep")
print(f"Stale documentation found in: {stale_files}")

# Automatically update a specific file based on code changes
auditor.update_file("docs/api/auth.md", focus="src/auth/service.py")
```

## Related tools / concepts
- [Claude Skills Ecosystem](claude-skills-ecosystem.md): The broader collection of agent enhancements.
- [Superpowers](superpowers.md): Curated skill bundles for developers.
- [KnowledgeOps](../../architecture/multi_agent_knowledgeops.md): The philosophy of managing knowledge like code.
- [Claude Code](../development_ops/claude-code.md): The CLI agent that frequently uses this skill.
- [PydanticAI](../frameworks/pydantic-ai.md): For creating agents that require high-quality documentation.
- [big-AGI](../ai_knowledge/big-agi.md): A GUI that can orchestrate documentation-heavy workflows.
- [agentic-workflows](../../knowledge_base/patterns/agentic-workflows.md): Patterns for building autonomous documentation pipelines.
- [LibreChat](../ai_knowledge/librechat.md): Unified AI interface with agent support.

## Sources / references
- [Documentation Writer Skill (GitHub)](https://github.com/awesome-copilot/documentation-writer)
- [Universal SKILL.md Standard](https://github.com/awesome-copilot/awesome-skills/blob/main/SPEC.md)
- [10 Must-Have Skills for 2026](https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051)

## Contribution Metadata
- Last reviewed: 2026-07-11
- Confidence: high
