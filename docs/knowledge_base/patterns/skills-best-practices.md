# Agent Skills Best Practices

## What it is
An agent **skill** is a self-contained, named behaviour module that an autonomous agent can discover, trigger, and execute. Skills define *what* to do (instructions), *when* to do it (triggers), *what tools* are available, and *what permissions* are required. Well-authored skills are the foundation of reliable agentic workflows using Claude 4.8 Opus and GPT-5.5. In July 2026, the **MCP 3.0 Task Protocol** has standardized how these skills are advertised and executed across heterogeneous agent swarms. This document covers authoring for **Claude Code** and **OpenClaw** runtimes.

## What problem it solves
Poorly authored skills lead to:
- **False Positives**: Skills triggering on irrelevant input, wasting tokens and causing side effects.
- **Ambiguity**: Agents performing tasks inconsistently due to vague instructions.
- **Security Risks**: Skills having broader permissions than necessary for their task.
- **Context Bloat**: Verbose skill definitions that consume the agent's context window unnecessarily.
- **Silent Failures**: Skills that fail without surfacing the correct error to the operator.

## Where it fits in the stack
**Pattern Layer**. Governs the engineering of prompts and tool definitions for all autonomous agents in the ecosystem, including [OpenClaw](../../tools/development_ops/openclaw.md) and [Claude Code](../../tools/development_ops/claude-code.md).

## Typical use cases
- **Code Maintenance**: Standardizing how agents perform git commits and PR reviews.
- **Document Ingestion**: Defining how PDFs from [Paperless-ngx](../../services/paperless-ngx.md) are classified and tagged.
- **Workflow Automation**: Creating triggers for [n8n](../../services/n8n.md) tasks via agentic decision-making.
- **System Self-Healing**: Setting up skills that monitor logs and restart services like [Gitea](../../services/gitea.md) when health checks fail.

## Strengths
- **Deterministic Routing**: Clear trigger definitions (keywords, slash commands, schedules) reduce "routing hallucinations".
- **MCP 3.0 Interoperability**: Adherence to the Task Protocol ensures skills are discoverable and executable by any MCP-compliant agent (e.g., Gemma 3, Llama 4).
- **Lean Instructions**: Step-by-step, deterministic instructions minimize token usage and improve reliability.
- **Reusability**: Skills can be shared across different agent runtimes and projects.
- **Auditability**: Encapsulated skills make it easier to audit exactly what an agent is allowed to do.

## Limitations
- **Model Dependency**: A skill optimized for Claude 4.8 may require slight adjustment for Llama 4 Maverick.
- **Overhead**: Requires disciplined documentation and versioning to prevent "skill drift" over time.
- **Complexity**: Deeply nested skills can become hard to debug if trigger logic overlaps significantly.

## When to use it
- When building **reusable agent behaviors** that will be invoked multiple times.
- To **standardize operational procedures** across a team of AI agents.
- When you need to **restrict agent actions** to a specific, verified set of tools and steps.

## When not to use it
- For **one-off, unique tasks** that will never be repeated.
- If the agent is operating in a purely conversational mode without tool access.
- When the task is so simple it can be handled by a single-sentence prompt without structured steps.

## Getting started

### Skill Anatomy (Claude Code - Markdown)
```markdown
---
name: commit
description: Create a git commit. Trigger when user says "commit" or "save changes".
---
# Commit Skill
## Steps
1. `git status` — confirm staged changes exist.
2. `git diff --staged` — identify changes.
3. Draft: imperative subject (<72 chars).
4. `git commit -m "[message]"`
5. Output: "{sha} {subject}"
```

### Skill Anatomy (OpenClaw - YAML)
```yaml
name: paperless-intake
description: Extract fields and file in Paperless-ngx.
trigger:
  keywords: ["file this", "intake document"]
  file_types: ["application/pdf"]
tools: [paperless_api, ocr_extract]
instructions: |
  1. Extract: type, date, correspondent, amount.
  2. POST to Paperless-ngx with correct tag.
  3. Reply with ID.
```

## CLI examples

### Validating Skill Syntax
Using an internal validator script:
```bash
python3 scripts/validate_skill.py --file .claude/skills/commit.md
```

### Listing Active Skills (Claude Code)
```bash
claude skills list
```

## API examples

### Programmatic Skill Registration (Python)
Using the Anthropic Agent SDK pattern:

```python
from anthropic_agent import Skill

@Skill(
    name="file_document",
    description="Files a document into Paperless-ngx. Trigger on 'file this pdf'.",
    permissions=["paperless_write"]
)
def file_document(content: str, title: str):
    # Implementation logic here
    pass
```

## Skill Quality Assurance & Validation
To ensure agentic reliability, every new skill must undergo standardized validation:
1. **Trigger Specificity Test**: Confirm positive and negative (near-miss) trigger firing.
2. **Token Efficiency Audit**: Ensure instructions are under 300 tokens (tiktoken `cl100k_base`).
3. **Resilience Test**: Simulate tool failures (e.g., 500 error) and verify graceful reporting.
4. **Consistency Baseline**: Run 3 times on same input to ensure zero-variance output.

### Automated Verification Snippet
```python
import tiktoken

def check_skill_efficiency(content, limit=300):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = len(encoding.encode(content))
    return tokens <= limit, tokens
```

## Related tools / concepts
- [Claude Code](../../tools/development_ops/claude-code.md) — The primary runtime for many engineering-focused skills.
- [OpenClaw](../../tools/development_ops/openclaw.md) — Multi-channel agent framework using YAML skills.
- [n8n](../../services/n8n.md) — For executing backend logic triggered by agent skills.
- [Paperless-ngx](../../services/paperless-ngx.md) — A common target for document-processing skills.
- [Gitea](../../services/gitea.md) — Used for versioning and storing skill definitions.
- [Fine-tuning Open Models](fine-tuning-open-models.md) — Used to bake skill-adherence behaviors into models.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Standard for connecting skills to tools.

## Sources / references
- [Claude Code Skills Documentation](https://docs.anthropic.com/claude-code/skills)
- [OpenClaw Skills Guide](https://github.com/openclaw/openclaw/wiki/Skills)
- [Anthropic Agent Skills Documentation](https://docs.anthropic.com/claude/docs/agent-skills)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
