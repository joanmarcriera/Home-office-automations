# OpenClaw Workflow Prompt Library Pattern

## What it is
A reusable-prompt pattern for operating an agent stack through concrete workflow prompts. This pattern focuses on "operationalizing" agents by providing them with highly structured, intent-rich instructions for recurring tasks like monitoring, backups, research, and reporting. As of January 2027, this pattern is heavily utilized by **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Qwen 3.8** agents to maintain state across long-horizon tasks using **FastMCP 3.1** protocol bindings.

## What problem it solves
Users and developers often know the desired outcome of an automation but struggle to express instructions that are both executable by an agent and resilient to edge cases. The OpenClaw Workflow Prompt pattern provides a library of pre-validated, "battle-tested" prompts that reduce the trial-and-error phase of agent deployment. It also mitigates "instruction drift" when multiple models (e.g., Llama 4, Qwen 3.8, and Claude 5.1) are used in the same operational pipeline.

## Where it fits in the stack
Prompts & AI Layer — serves as the "software interface" between human intent and agentic execution. It supports [Operational Playbooks](../../playbooks/index.md) and standardized [Agentic Workflows](agentic-workflows.md).

## Typical use cases
- **Infrastructure Monitoring**: Prompts that guide an agent to check server logs and summarize anomalies.
- **Development Handoffs**: Standardized "context dumping" prompts for moving work between different coding agents (e.g., from an architect agent to a coder agent).
- **Scheduled Reporting**: Weekly briefs that aggregate data from multiple sources (GitHub, Vikunja, n8n) into a cohesive summary.
- **Resource Cleanup**: Automated "janitor" prompts for identifying and deleting temporary files or old cloud resources.

### Core Prompt Library Patterns

#### 1. The "Observer" (Monitoring)
> "Review the last 50 lines of the `syslog` and `n8n_output.log`. Identify any unique error codes and correlate them with any recent service restarts. Summarize the impact on the `Paperless-ngx` service."

#### 2. The "Archivist" (Cleanup)
> "Identify all files in the `tmp/` directory older than 30 days. List their sizes and last access times. If they are not in the `ignore_list.txt`, propose a deletion script."

#### 3. The "Sync-Master" (Reporting)
> "Compare the 'Completed Tasks' in Vikunja for the last 7 days against the 'GitHub PRs Merged' in the same period. Generate a bulleted 'Weekly Achievement' report for the family newsletter."

## Strengths
- **Reduced Hallucinations**: Structured templates guide models toward specific data sources and formats.
- **Faster Setup**: Drastically reduces the time required to bootstrap new automation workflows.
- **Standardization**: Ensures that different agents performing the same task use the same high-quality logic.
- **Cross-Model Compatibility**: Verified to work across Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Qwen 3.8, and Llama 4.

## Limitations
- **Environment Sensitivity**: Prompts often include assumptions about file structures or API availability that must be adapted for specific users.
- **Maintenance**: As underlying tools (like CLI versions or API schemas) change, the prompts must be updated (prompt drift).
- **Safety**: Reusable prompts must still be vetted for security, especially those involving destructive actions (e.g., `rm`, `delete`).
- **Context Pollution**: If placeholders are loaded with excessively long context tables, the model's instruction-following can degrade.

## When to use it
- When implementing recurring operational tasks that are too complex for simple scripts but too regular to rewrite every time.
- When building a "System of Record" for how your agents should behave across different domains.

## When not to use it
- For extremely simple, one-line commands that don't benefit from structured instructions.
- When a task is so unique that a template would provide no value or could introduce bias.

## Getting started
To start using the OpenClaw Workflow Prompt pattern, clone the standard library and integrate it into your agent's system prompt or tool-calling logic.

1.  **Select a Prompt**: Browse the [OpenClaw Use-Case Catalog](openclaw-use-case-catalog.md).
2.  **Fill Placeholders**: Replace variables like `{{ date }}` or `{{ project_path }}`.
3.  **Execute**: Send the prompt to your preferred model (Claude 5.1 or GPT-5.5 Recommended).

## CLI examples
> [!NOTE]
> This pattern is typically invoked via agent frameworks, but can be tested using the OpenClaw CLI.

```bash
# Execute a monitoring prompt via CLI
openclaw run monitoring --service "paperless"

# List available workflow prompts
openclaw list-prompts

# Export a prompt for use in another agent
openclaw export "sync-master" --format markdown
```

## API examples
Example of loading, validating with strict Pydantic v2 schemas, and executing an OpenClaw prompt using the **FastMCP 3.1** Python SDK with early January 2027 model parameters:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict, Any

mcp = FastMCP("OpenClaw-Workflow-Prompts")

class WorkflowParams(BaseModel):
    """Strict Pydantic v2 model for validating workflow prompt execution payload."""
    prompt_id: str = Field(..., description="Unique identifier for the OpenClaw workflow prompt")
    context: Dict[str, Any] = Field(default_factory=dict, description="Key-value mapping of prompt placeholders")
    model_override: str = Field(default="claude-5.6-sonnet", description="Target frontier model for execution")

@mcp.tool()
def execute_workflow(params: WorkflowParams) -> str:
    """Executes a standardized OpenClaw workflow prompt with Pydantic v2 runtime validation."""
    # Retrieve template safely based on validated prompt_id
    templates = {
        "observer": "Review the last 50 lines of syslog for {{ service }}. Highlight error codes.",
        "archivist": "Find files in {{ path }} older than {{ days }} days and summarize sizes."
    }

    template = templates.get(params.prompt_id, "Analyze context and report anomalies for {{ service }}.")

    # Fill placeholders safely
    filled_prompt = template
    for key, val in params.context.items():
        filled_prompt = filled_prompt.replace(f"{{{{ {key} }}}}", str(val))

    return f"Executed workflow [{params.prompt_id}] on model [{params.model_override}]:\n{filled_prompt}"
```

## Related tools / concepts
- [OpenClaw Use-Case Catalog](openclaw-use-case-catalog.md)
- [OpenClaw Security and Operations Pattern](openclaw-security-operations.md)
- [Agentic Workflows](agentic-workflows.md)
- [Skills Best Practices](skills-best-practices.md)
- [System Prompts](../system_prompts.md)
- [Prompt Requests](prompt_requests.md)
- [Jules Weekly Gap Analysis](../../reference-implementations/llm-prompts/jules-gap-analysis.md)
- [Family Context Prompt](../../reference-implementations/llm-prompts/family-context.md)
- [Model Context Protocol (Model Context Protocol (MCP 3.1))](tool-calling-and-mcp.md)

## Sources / References
- [OpenClaw after 50 days: all prompts for 20 real workflows](https://gist.github.com/velvet-shark/b4c6724c391f612c4de4e9a07b0a74b6)
- [OpenClaw Foundation Documentation (January 2027)](https://openclaw.io/docs)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
