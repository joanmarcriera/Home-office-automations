# Documentation Writer Skill

## What it is
A specialized skill for AI agents (Claude Code, Cursor, Gemini CLI, etc.), designed to automate the creation, auditing, and maintenance of project documentation. It follows the universal `SKILL.md` format and integrates directly with agentic development workflows.

## What problem it solves
Documentation rot is a major issue in fast-moving projects. This skill ensures that READMEs, API references, architecture diagrams, and changelogs stay synchronized with the actual source code, reducing technical debt and onboarding friction.

## Where it fits in the stack
**Category**: [Agents](index.md) / [Specialized Skills](claude-skills-ecosystem.md). It acts as a documentation-specific playbook for the agent.

## Typical use cases
- **Full Repository Audit**: Scanning the codebase to identify missing documentation or outdated sections.
- **Automated API Reference**: Generating docstrings and markdown files from function/class definitions.
- **KnowledgeOps Sync**: Updating repository indexes and site navigation (e.g., `mkdocs.yml`) based on new files.
- **Visual Mapping**: Generating Mermaid or Excalidraw diagram definitions to visualize architecture.

## Key Features (May 2026 Update)
- **Universal SKILL.md Support**: Compatible with the latest cross-agent skill standard used by Claude Code, Cursor, and Antigravity IDE.
- **Symbolic Analysis**: Uses LSP (Language Server Protocol) data to provide deeper, more accurate code explanations than raw text analysis.
- **Documentation Linting**: Automatically checks for broken relative links, missing metadata, and taxonomy violations.
- **Multi-Format Export**: Generates documentation in Markdown, PDF, and interactive HTML.

## Strengths
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

## Licensing and cost
- **Open Source**: MIT License.
- **Cost**: Free (Requires LLM API tokens for the host agent).
- **Self-hostable**: Yes, via the universal skill installer.

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

## Related tools / concepts
- [Claude Skills Ecosystem](claude-skills-ecosystem.md): The broader collection of agent enhancements.
- [Superpowers](superpowers.md): Curated skill bundles for developers.
- [KnowledgeOps](../../multi_agent_knowledgeops.md): The philosophy of managing knowledge like code.

## Sources / references
- [Documentation Writer Skill (GitHub)](https://github.com/awesome-copilot/documentation-writer)
- [Universal SKILL.md Standard](https://github.com/awesome-copilot/awesome-skills/blob/main/SPEC.md)
- [10 Must-Have Skills for 2026](https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
