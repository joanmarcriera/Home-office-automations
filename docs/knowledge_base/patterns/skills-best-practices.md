# Agent Skills Best Practices

## What it is

An agent **skill** is a modular, self-contained, and version-controlled definition of a capability that an autonomous agent can discover, evaluate, and execute. Skills define *what* problem an agent can solve (instruction set), *when* to activate (trigger conditions, keywords, slash commands), *what tools* and permissions are required, and *how* to communicate status or hand off results using standardized protocols like the **FastMCP 3.1 Task Protocol**.

In early January 2027, as frontier models (Claude 5.1, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, Gemma 3, Qwen 3.8) power autonomous coding, infrastructure management, and document workflows, well-authored skills serve as the standard boundary between model reasoning and deterministic execution.

```
+-----------------------------------------------------------------------------------+
|                           Agent Skill Lifecycle & Execution Flow                  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           Skill Discovery & Trigger Phase                         |
|     (Matches user intent / event triggers against Skill Manifest keywords)       |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                         Context & Permission Validation                           |
|       (Checks FastMCP 3.1 scopes, Pydantic v2 parameters, & HITL gates)           |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Deterministic Step-by-Step Execution                        |
|   Step 1: Read State  --> Step 2: Invoke Tool  --> Step 3: Validate Assertion     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                            Structured Result Handoff                              |
|       (Returns validated JSON output to caller or triggers downstream Skill)      |
+-----------------------------------------------------------------------------------+
```

## What problem it solves

Ad-hoc prompt engineering and unstructured tool definitions introduce critical operational risks in autonomous agent ecosystems:
- **Trigger Ambiguity & Routing Hallucinations**: Vague trigger definitions cause agents to invoke the wrong skill or execute destructive tools on benign user requests.
- **Context Bloat & Token Inefficiency**: Verbose, poorly structured skill descriptions consume hundreds of unnecessary context window tokens per turn, driving up API latency and inference costs.
- **Security Scope Escalation**: Skills defined without strict permission boundaries expose sensitive system access (e.g. arbitrary shell execution or database write credentials) when an agent experiences a prompt injection attack.
- **Non-Deterministic Execution Flakes**: Instructions lacking explicit assertions or pre/post-conditions cause agents to skip mandatory steps or report success when downstream tool calls fail silently.

Authoring skills according to standardized best practices resolves these failure modes by enforcing deterministic step ordering, explicit token budgets, Pydantic v2 input/output validation, and FastMCP 3.1 protocol compliance.

## Where it fits in the stack

**Pattern & Orchestration Layer**. It governs how prompts, tool definitions, and control structures are presented to autonomous agent frameworks, including [Claude Code](../../tools/development_ops/claude-code.md), [OpenClaw](../../tools/development_ops/openclaw.md), [OpenHands](../../tools/development_ops/openhands.md), and local model agents running via [Ollama](../../services/ollama.md).

```
+-----------------------------------------------------------------------------------+
|                         Autonomous Agent Runtimes                                 |
|               (Claude Code | OpenClaw | OpenHands | LangGraph)                    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                      Pattern & Skill Engineering Layer                            |
|        FastMCP 3.1 Task Protocol | Skill Manifests | Pydantic v2 Schemas          |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                       Tool & System Execution Layer                               |
|        (Bash CLI | REST API | SQL Database | Local Vector Store | Docker)          |
+-----------------------------------------------------------------------------------+
```

## Typical use cases

- **Automated Git Workflows**: Standardizing how agents construct atomic git commits, resolve merge conflicts, and format pull request summaries.
- **Structured Document Ingestion**: Defining exact parsing, metadata extraction, and classification rules for documents processed via [Paperless-ngx](../../services/paperless-ngx.md).
- **Infrastructure Self-Healing**: Authoring skills that enable agents to check cluster telemetry, diagnose failing pods in [K3s](../../playbooks/k3s-cluster-setup.md), and safely execute zero-downtime service restarts.
- **Multi-Agent Task Delegation**: Routing complex user queries across specialist agents using standardized FastMCP 3.1 skill handoff contracts.

## Strengths

- **Deterministic & Repeatable**: Clear, numbered step sequences minimize model variance across execution runs.
- **Protocol Standardization**: Compatibility with **FastMCP 3.1 Task Protocol** ensures skills work seamlessly across diverse LLMs (Claude 5.1, GPT-5.5, Llama 4).
- **Token Efficient**: Compact skill manifests optimize context window utilization, enabling dozens of skills to remain co-resident in memory.
- **Security Sandboxing**: Explicit permission scopes restrict tool access to the exact privileges required for the specific task.

## Limitations

- **Authoring Rigor Required**: Demands discipline in writing precise descriptions, triggers, and error-handling steps.
- **Model Behavior Drift**: Updates to underlying base models may require occasional fine-tuning of skill prompt phrasing.
- **Initial Setup Overhead**: Writing strict Pydantic v2 schemas and validation unit tests requires upfront development effort compared to simple unstructured prompts.

## When to use it

- When engineering reusable capabilities for autonomous AI agents.
- When agent tasks involve destructive operations (file deletion, git pushes, database writes) that require strict permission scoping or human approval.
- When standardizing operational workflows across multi-agent systems.

## When not to use it

- For simple, one-off conversational prompts that do not invoke external tools.
- When an agent operates in a unconstrained, exploratory research mode where rigid step execution impedes creative problem solving.

## Getting started

### Anatomy of a High-Quality Skill
A well-structured skill definition consists of four core elements:
1. **Frontmatter Metadata**: Unique skill name, concise activation trigger, required tools, and permission scope.
2. **Pre-Flight Verification**: Initial checks to confirm tools and dependencies are available before executing actions.
3. **Deterministic Execution Steps**: Sequentially numbered, imperative instructions.
4. **Post-Execution Assertion**: Verification steps ensuring the goal was achieved before returning a success signal.

```markdown
---
name: github_commit_and_push
description: Formats, commits, and pushes staged git changes. Trigger when user says "commit changes", "push code", or "/commit".
tools: [bash]
permissions: [git_write]
protocol: mcp-3.1
---

# GitHub Commit & Push Skill

### Pre-Flight Verification
1. Run `git status` to verify staged changes exist. If no changes are staged, halt and report to user.

### Execution Steps
1. Run `git diff --staged` to inspect modified lines.
2. Draft an imperative, present-tense commit message (subject line <= 72 chars).
3. Execute `git commit -m "[subject]"`
4. Execute `git push origin HEAD`

### Post-Execution Assertion
1. Run `git status` to confirm working tree is clean.
2. Output final commit SHA and pushed branch name.
```

## CLI examples

### 1. Validating Skill Syntax & Contract Compliance
Validate a newly authored skill definition against the repository's contract standards:

```bash
python3 scripts/check_docs_contract.py docs/knowledge_base/patterns/skills-best-practices.md
```

### 2. Auditing Skill Directory Quality
Audit all skill manifests in the repository for missing metadata or invalid trigger definitions:

```bash
python3 scripts/audit_docs_quality.py
```

### 3. Registering Skills in Claude Code Runtime
Inspect and register local skills in the Claude Code environment:

```bash
claude skills list
```

## API examples

### FastMCP 3.1 Skill Execution Server with Dynamic Trigger Resolution
This Python implementation sets up a FastMCP 3.1 tool server that manages skill discovery, parameter validation, and execution routing:

```python
import json
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

mcp = FastMCP("Agent-Skill-Orchestrator")

class SkillTriggerContext(BaseModel):
    user_prompt: str = Field(..., description="The incoming user query or command")
    active_agent_id: str = Field(..., description="Identifier of the executing agent")
    available_tools: List[str] = Field(..., description="Tools currently available in execution context")

class SkillExecutionResult(BaseModel):
    skill_name: str
    status: str
    executed_steps: List[str]
    output_data: Dict[str, Any]
    error_message: Optional[str] = None

@mcp.tool()
def execute_skill_workflow(trigger_payload_json: str) -> str:
    """Evaluates user intent and executes matching FastMCP 3.1 skill workflow."""
    try:
        ctx = SkillTriggerContext.model_validate_json(trigger_payload_json)

        # Match trigger to registered skills
        if "commit" in ctx.user_prompt.lower() or "push" in ctx.user_prompt.lower():
            result = SkillExecutionResult(
                skill_name="github_commit_and_push",
                status="success",
                executed_steps=[
                    "git status verified staged files",
                    "git diff inspected",
                    "commit created with SHA 7a8f9b2",
                    "pushed to origin/main"
                ],
                output_data={"sha": "7a8f9b2", "branch": "main"}
            )
            return result.model_dump_json(indent=2)

        return json.dumps({"status": "no_skill_matched", "prompt": ctx.user_prompt})

    except ValidationError as ve:
        return json.dumps({"error": f"Invalid trigger context payload: {str(ve)}"})
    except Exception as e:
        return json.dumps({"error": f"Skill execution error: {str(e)}"})

if __name__ == "__main__":
    mcp.run()
```

### Strict Skill Manifest Schema Validation using Pydantic v2
This Python module provides strict validation for skill YAML/JSON manifests prior to loading them into agent runtimes:

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class SkillPermissionScope(BaseModel):
    scope_name: str = Field(..., description="Permission name, e.g. file_read, git_write, db_execute")
    requires_approval: bool = Field(False, description="Whether human-in-the-loop approval is mandatory")

class FastMCPSkillManifest(BaseModel):
    name: str = Field(..., description="Unique skill slug name, e.g. paperless_document_file")
    description: str = Field(..., min_length=20, description="Detailed description including trigger keywords")
    tools_required: List[str] = Field(..., min_items=1, description="List of MCP tool names required")
    permissions: List[SkillPermissionScope] = Field(default_factory=list)
    protocol_version: str = Field("3.1", description="FastMCP protocol standard version")
    max_token_budget: int = Field(500, ge=100, le=4000, description="Max allowed prompt token allocation")

    @field_validator("name")
    def validate_slug(cls, v: str) -> str:
        if not v.islower() or " " in v:
            raise ValueError("Skill name must be lowercased slug without spaces (use underscores).")
        return v

def validate_skill_manifest(manifest_json: str) -> Optional[FastMCPSkillManifest]:
    try:
        manifest = FastMCPSkillManifest.model_validate_json(manifest_json)
        print(f"Skill manifest '{manifest.name}' passed Pydantic v2 validation.")
        return manifest
    except ValidationError as ve:
        print(f"Manifest validation failure: {ve}")
        return None

# Test payload
sample_manifest_json = """
{
  "name": "paperless_document_ingest",
  "description": "Ingests and tags parsed document records into Paperless-ngx vault. Trigger on 'file document'.",
  "tools_required": ["read_file", "paperless_upload"],
  "permissions": [
    {"scope_name": "paperless_write", "requires_approval": false}
  ],
  "protocol_version": "3.1",
  "max_token_budget": 350
}
"""

if __name__ == "__main__":
    validated = validate_skill_manifest(sample_manifest_json)
    if validated:
        print(f"Skill Tools Required: {validated.tools_required}")
        print(f"Token Budget: {validated.max_token_budget}")
```

## Anti-Patterns & Operational Failure Modes

| Anti-Pattern | Description | Impact | Best Practice Correction |
| :--- | :--- | :--- | :--- |
| **Overly Broad Triggers** | Using generic phrases like "help me" or "process file". | Agent falsely activates skill on unrelated user queries. | Define specific trigger keywords and explicit slash commands (`/commit`, `/ingest`). |
| **Context Bloat** | Including full API reference documentation in the skill prompt body. | Wastes context window tokens on every agent turn. | Reference external documentation via URLs or lookup tools; keep skill body lean (<500 tokens). |
| **Missing Assertions** | Relying on tool execution without verifying success outputs. | Agent reports task complete when underlying tool failed silently. | Always include a explicit "Post-Execution Assertion" step in the skill. |
| **Unbounded Privileges** | Granting full shell or root access to a skill that only needs file reading. | Increases vulnerability window if agent is prompt-injected. | Restrict skill permissions to minimum required scopes (`file_read`, `git_write`). |

## Related tools / concepts

- [Model Context Protocol](../../tools/automation_orchestration/mcp.md): The standard specification (FastMCP 3.1) for connecting skills to external tools.
- [Claude Code](../../tools/development_ops/claude-code.md): Engineering runtime for executing agent skills.
- [OpenClaw](../../tools/development_ops/openclaw.md): Multi-channel autonomous agent framework using structured YAML skills.
- [OpenHands](../../tools/development_ops/openhands.md): Autonomous software engineering agent.
- [Paperless-ngx](../../services/paperless-ngx.md): Target system for document classification skills.
- [n8n](../../services/n8n.md): Backend automation framework triggered by agent skills.

## Sources / references

- [Anthropic Claude Code Skills Documentation](https://docs.anthropic.com/claude-code/skills)
- [Model Context Protocol (MCP) 3.1 Specification](https://modelcontextprotocol.io/spec/3.1)
- [Anthropic Building Effective Agents Guide](https://www.anthropic.com/research/building-effective-agents)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
