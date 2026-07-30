# Agent Skills Best Practices

## What it is
An agent **skill** is a self-contained, named behavior module that an autonomous agent can discover, trigger, and execute. Skills define *what* to do (instructions), *when* to do it (triggers), *what tools* are available, and *how to report success* using standardized protocols like the **MCP 3.1 Task Protocol**. Well-authored skills are the foundation of reliable agentic workflows using Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, and Qwen 3.6.

## What problem it solves
Poorly authored skills lead to:
- **False Positives**: Skills triggering on irrelevant input, wasting tokens and causing side effects.
- **Ambiguity**: Agents performing tasks inconsistently due to vague instructions.
- **Security Risks**: Skills having broader permissions than necessary for their task.
- **Context Bloat**: Verbose skill definitions that consume the agent's context window unnecessarily.
- **Silent Failures**: Skills that fail without surfacing the correct error to the operator or the next agent in the loop.

## Where it fits in the stack
**Pattern Layer**. Governs the engineering of prompts and tool definitions for all autonomous agents in the ecosystem, including [OpenClaw](../../tools/development_ops/openclaw.md), [Claude Code](../../tools/development_ops/claude-code.md), and [Gemma 3](../../tools/ai_knowledge/local_llms.md) based local agents.

## Typical use cases
- **Code Maintenance**: Standardizing how agents perform git commits and PR reviews.
- **Document Ingestion**: Defining how PDFs from [Paperless-ngx](../../services/paperless-ngx.md) are classified and tagged.
- **Workflow Automation**: Creating triggers for [n8n](../../services/n8n.md) tasks via agentic decision-making.
- **System Self-Healing**: Setting up skills that monitor logs and restart services like [Gitea](../../services/gitea.md) when health checks fail.
- **Standardized Validation**: Every skill must undergo standardized validation: Trigger Specificity Test, Token Efficiency Audit, Resilience Test, and Consistency Baseline.

## Strengths
- **Deterministic Routing**: Clear trigger definitions (keywords, slash commands, schedules) reduce "routing hallucinations".
- **Lean Instructions**: Step-by-step, deterministic instructions minimize token usage and improve reliability.
- **Reusability**: Skills can be shared across different agent runtimes and projects.
- **Interoperability**: Compatibility with **MCP 3.1 Task Protocol** allows skills to be executed across diverse model architectures.

## Limitations
- **Model Dependency**: A skill optimized for Claude 5.1 may require slight adjustment for Llama 4 Maverick or Gemma 3.
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
### Steps
1. `git status` — confirm staged changes exist.
2. `git diff --staged` — identify changes.
3. Draft: imperative subject (<72 chars).
4. `git commit -m "[message]"`
5. Output: "{sha} {subject}"
```

### MCP 3.1 Task Protocol Integration
Skills in late October / November 2026 are increasingly defined using the **MCP 3.1 Task Protocol**, which provides a JSON-schema for task requirements and state tracking:

```json
{
  "task": "technical-audit",
  "protocol": "mcp-3.1",
  "triggers": ["audit document", "check freshness"],
  "tools": ["read_file", "grep", "check_docs_contract"],
  "requirements": {
    "sections": 13,
    "last_reviewed_format": "ISO-8601"
  }
}
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

### Programmatic Skill Registration with Pydantic v2 validation under MCP 3.1
Using the Anthropic Agent SDK pattern with MCP 3.1 support, we can strictly validate skill manifest properties before registration.

```python
from typing import List, Dict, Any
from pydantic import BaseModel, Field, field_validator

# Define Pydantic v2 schemas for Skill manifest verification
class SkillManifest(BaseModel):
    name: str = Field(..., description="Unique skill identifier")
    description: str = Field(..., min_length=15, description="Clear description of when/how the agent triggers this skill")
    permissions: List[str] = Field(default_factory=list, description="Explicit scopes needed")
    protocol: str = Field("mcp-3.1", description="Supported protocol version")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="JSON schema parameters")

    @field_validator("protocol")
    def validate_protocol(cls, v: str) -> str:
        if v not in ["mcp-3.0", "mcp-3.1"]:
            raise ValueError("Protocol must be mcp-3.0 or mcp-3.1")
        return v

# Programmatic registration wrapper
def register_skill_securely(manifest_data: dict) -> SkillManifest:
    # Validate the data using model_validate
    validated_manifest = SkillManifest.model_validate(manifest_data)

    # Process registration downstream
    print(f"Skill '{validated_manifest.name}' validated successfully on {validated_manifest.protocol}.")
    return validated_manifest

# Test sample registration
sample_manifest = {
    "name": "file_document",
    "description": "Files a parsed document securely into the Paperless-ngx file vault.",
    "permissions": ["paperless_write"],
    "protocol": "mcp-3.1",
    "parameters": {
        "type": "object",
        "properties": {
            "content": {"type": "string"},
            "title": {"type": "string"}
        },
        "required": ["content"]
    }
}

manifest = register_skill_securely(sample_manifest)
```

## Related tools / concepts
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — The standard for connecting skills to tools (MCP 3.1 Task Protocol).
- [Claude Code](../../tools/development_ops/claude-code.md) — Runtime for engineering-focused skills.
- [OpenClaw](../../tools/development_ops/openclaw.md) — Multi-channel agent framework using YAML skills.
- [Local LLMs](../../tools/ai_knowledge/local_llms.md) — Reference for running Gemma 3 and other models locally.
- [n8n](../../services/n8n.md) — For executing backend logic triggered by agent skills.
- [Paperless-ngx](../../services/paperless-ngx.md) — A common target for document-processing skills.
- [Fine-tuning Open Models](fine-tuning-open-models.md) — Used to bake skill-adherence behaviors into models.

## Sources / references
- [Claude Code Skills Documentation](https://docs.anthropic.com/claude-code/skills)
- [Model Context Protocol 3.1 Specification](https://modelcontextprotocol.io/spec/3.1)
- [Anthropic Agent Skills Documentation](https://docs.anthropic.com/claude/docs/agent-skills)
- [Gemma 3 Technical Report](https://storage.googleapis.com/deepmind-media/gemma/gemma-3-report.pdf)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
