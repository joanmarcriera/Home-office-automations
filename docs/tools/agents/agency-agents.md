# Agency-Agents

## What it is
Agency-Agents is a comprehensive, open-source suite of 110+ highly specialized AI agent personas designed to transform generic coding assistants into a multi-disciplinary, "complete AI agency." As of late October 2026, it serves as an essential configuration and orchestration layer for leading IDE-based and terminal agents (such as **Claude 5.1**, **GPT-5.5**, and **Llama 4**). It manages domain-specific identities, guardrails, and success metrics by exposing the persona library natively through **Model Context Protocol (MCP 3.1)** resources and prompt endpoints.

## What problem it solves
Generic instructions often fail to extract highly specialized technical output, resulting in hallucinated library paths, incorrect architecture, or suboptimal security practices. Agency-Agents solves this by offering structured, opinionated expert personas—such as Frontend Architects, Security Engineers, Reality Checkers, and Financial Risk Analysts. It enforces constraints and narrow target definitions, resulting in cleaner code, systematic peer reviews, and vastly improved scores on software engineering benchmarks like [SWE-bench](../benchmarking/swe-bench.md).

## Where it fits in the stack
**Agents / Personas / Framework**. It occupies the prompt engineering and context modeling layer. Sitting between the base LLM and the runtime environment, it works in conjunction with terminal-based assistants and agent orchestrators to inject tailored system prompts, active tools, and strict execution guardrails.

## Typical use cases
- **Multi-Agent Collaborative Design**: Deploying a "Backend Architect" to draft a database schema, followed by a "Security Engineer" to review the API endpoints for potential injections.
- **Socratic Reality Checking**: Injecting the "Reality Checker" persona in a secondary loop to identify logical contradictions or over-engineering prior to code generation.
- **Automated PR Reviews**: Running an autonomous CI pipeline action that utilizes the "Code Reviewer" persona to evaluate incoming pull requests against repository standards.
- **Domain-Specific Analysis**: Utilizing specialized business roles (e.g., "SaaS Pricing Specialist") to analyze business logic alongside core application structures.

## Strengths
- **Massive Persona Library**: Over 110 precisely defined developer, devops, security, testing, and creative agent templates.
- **Native MCP 3.1 Integration**: Exposes the complete collection of agent personas as queryable context resources and dynamic system prompts.
- **Frontier Model Optimization**: Prompts are tuned for advanced reasoning paradigms in **Claude 5.1** and **GPT-5.5**, utilizing specialized XML formatting and pre-tool-use instructions.
- **Subagent-Friendly**: Perfectly structured for agent-to-agent handoffs and task decomposition.
- **Drastic Hallucination Reduction**: Constrains the generation window to specific, vetted standards and methodologies.

## Limitations
- **Context Footprint**: Extremely verbose system prompts can consume a portion of the context window (although largely mitigated by the 2.5M token context windows of late 2026 models).
- **Manual Mapping**: Integrating custom personas into proprietary pipelines without MCP support requires custom loader logic.
- **Upkeep Cost**: As underlying model capabilities shift rapidly, prompt templates require regular testing and tune-ups to avoid regression.

## When to use it
- When implementing a team-based agent architecture where multiple expert perspectives are needed to solve a single complex engineering task.
- When working within agentic IDE platforms (like Claude Code, Cursor, Aider, or Windsurf) that accept custom system prompt resources.
- When establishing high-reliability, local agent workflows using open-weight models like **Llama 4** or **Qwen 3.6**.

## When not to use it
- For quick, trivial, or single-turn tasks where a general-purpose, non-specialized chat assistant is faster and more context-efficient.
- If you have already developed highly customized, proprietary, and domain-vetted system prompts specifically tuned for your industry.

## Getting started

### Installation
Clone the repository to your local directory:
```bash
git clone https://github.com/msitarzewski/agency-agents.git ~/.agency-agents
```

### MCP 3.1 Setup
To expose these personas dynamically to MCP 3.1-compliant client applications, add the node-based agency-agents server to your global MCP configuration (typically in `~/.code/mcp-config.json` or `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "agency-agents": {
      "command": "npx",
      "args": ["-y", "@agency-agents/mcp-server@latest"],
      "env": {
        "AGENCY_DIR": "/absolute/path/to/.agency-agents/agents"
      }
    }
  }
}
```

### Integration with Claude Code
Invoke specialized personas directly inside Claude Code using standard resource handles:
```bash
claude "Use the @agency-agents/backend-architect persona to analyze the current database schema"
```

## CLI examples

### Listing Available Specialist Personas
```bash
# List all engineering personas
ls ~/.agency-agents/agents/engineering/

# Search for security-specific specialists
ls ~/.agency-agents/agents/ | grep -E "security|vulnerability"
```

### Local Execution with Aider
Inject the security engineer persona file directly as system instructions during an Aider session:
```bash
aider --model anthropic/claude-5-1-sonnet --system-prompt ~/.agency-agents/agents/engineering/security-engineer.md
```

### Batch Processing via Shell
Apply a persona to review a file and output comments:
```bash
cat ~/.agency-agents/agents/qa-engineer.md src/app/main.py | claude -p "Review this file" > qa_feedback.md
```

## API examples

### Programmatic Persona Loading (Python)
The following Python script loads an Agency-Agents persona and invokes the **Claude 5.1** API using modern client configurations, complete with robust error handling and structured system prompt injection.

```python
import os
import sys
from anthropic import Anthropic, APIError, APIConnectionError

def load_agency_persona(persona_name: str) -> str:
    """Loads a raw persona file from the local agency-agents repository."""
    base_path = os.path.expanduser("~/.agency-agents/agents")
    # Search recursively or build exact path
    persona_path = os.path.join(base_path, f"{persona_name}.md")

    if not os.path.isfile(persona_path):
        raise FileNotFoundError(f"Persona '{persona_name}' not found at {persona_path}")

    try:
        with open(persona_path, "r", encoding="utf-8") as f:
            return f.read()
    except IOError as e:
        raise RuntimeError(f"Failed to read persona file: {e}")

def run_agentic_task(persona_name: str, task_description: str):
    """Executes a specialized task with the loaded persona using Claude 5.1."""
    try:
        persona_prompt = load_agency_persona(persona_name)
    except Exception as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        return

    # Initialize the official Anthropic client
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    try:
        response = client.messages.create(
            model="claude-5-1-sonnet-20261022",
            max_tokens=4096,
            temperature=0.2,
            system=persona_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Please perform the following task strictly following your identity: {task_description}"
                }
            ]
        )
        print("--- Agent Output ---")
        print(response.content[0].text)
    except APIConnectionError as e:
        print(f"Network Connection Failed: {e}", file=sys.stderr)
    except APIError as e:
        print(f"Anthropic API Error (Status {e.status_code}): {e.message}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Example invocation: Run a reality-check critique on a system plan
    run_agentic_task(
        persona_name="reality-checker",
        task_description="Critique the plan to migrate a synchronous database architecture to event-driven serverless functions."
    )
```

## Related tools / concepts
- [Auto-Gen Studio](../frameworks/autogen-studio.md)
- [CrewAI](../frameworks/crewai.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Claude Code](../development_ops/claude-code.md)
- [Aider](../development_ops/aider.md)
- [AutoGen](../frameworks/autogen.md)
- [OpenClaw](../development_ops/openclaw.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [System Prompt Engineering](../../knowledge_base/patterns/system-prompts.md)
- [Multi-Agent Systems](../../knowledge_base/concepts/multi-agent-systems.md)

## Sources / references
- [Official GitHub Repository](https://github.com/msitarzewski/agency-agents)
- [YUV.AI: Agency Agents Overview](https://yuv.ai/blog/agency-agents)
- [Anthropic: System Prompt Best Practices](https://docs.anthropic.com/claude/docs/system-prompts)

## Contribution Metadata
- Last reviewed: 2026-10-24
- Confidence: high
