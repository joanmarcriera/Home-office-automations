# Agency-Agents

## What it is
Agency-Agents is a comprehensive suite of 110+ specialized AI agent personas designed to transform generic coding assistants into a "complete AI agency." In late July 2026, it serves as a critical configuration layer for IDE-based agents like Claude 5.1, GPT-5.5, Llama 4, and Qwen 3.6, providing them with domain-specific identities, missions, and success metrics through **Native Model Context Protocol (MCP 3.1) support**.

## What problem it solves
It reduces AI hallucinations and improves technical output by providing "off-the-shelf" expert personas. It moves beyond generic "write code" prompts to specialized, opinionated domain expertise—from Frontend Architects and Security Engineers to Reality Checkers and specialized Business Analysts.

## Where it fits in the stack
**Agents / Personas / Framework**. It acts as a system prompt and configuration layer for terminal and IDE-based agents. It sits between the raw LLM and the application-specific workflow.

## Typical use cases
- **Multi-agent IDE Workflows**: Invoking a "Backend Architect" for initial design and a "Security Engineer" for a final PR review.
- **Reality Checking**: Using the "Reality Checker" persona to find logical flaws in proposed solutions before implementation.
- **Specialized Engineering**: Deploying "Performance Tuning" or "Documentation Specialist" personas for specific project phases.
- **Business Logic Review**: Using "Financial Risk Analyst" or "Product Manager" personas to evaluate feature impact.

## Strengths
- **High Specialization**: 110+ personas covering development, security, business, and creative roles.
- **Native MCP 3.1**: Personas are now exposed as Model Context Protocol resources and tools, allowing seamless discovery and dynamic payload exchange by compliant agents.
- **Claude 5.1 Optimized**: Personas updated with specialized `PreToolUse` and `PostToolUse` logic for high-precision tool calling.
- **Model Agnostic**: Works with any frontier model through any interface.
- **Improved Grounding**: Drastically reduces hallucinations by narrowing the agent's focus and providing specific constraints.

## Limitations
- **Manual Integration**: Requires cloning the repo and manually referencing files in most tools.
- **Context Overhead**: Long system prompts from complex personas can consume a significant portion of the context window in older models.
- **Maintenance**: Personas may need periodic updates to align with the capabilities of new models (e.g., Claude 5.1).

## When to use it
- When you need more than just a general-purpose assistant and want a virtual "team" of experts.
- For complex engineering tasks that require multiple perspectives (architecture, security, testing).
- When using tools like Claude Code, Cursor, or Aider that allow custom system instructions.

## When not to use it
- For simple, one-off tasks where a general-purpose assistant is sufficient.
- If you have already developed highly customized, proprietary system prompts for your specific domain.

## Getting started

### Installation
```bash
# Clone the repository to your local machine
git clone https://github.com/msitarzewski/agency-agents.git ~/.agency-agents
```

### MCP 3.1 Setup
Expose the persona library to your agents by adding the Agency MCP server to your configuration:
```json
{
  "mcpServers": {
    "agency-agents": {
      "command": "node",
      "args": ["~/.agency-agents/mcp/index.js"],
      "env": {
        "PERSONAS_DIR": "~/.agency-agents/agents"
      }
    }
  }
}
```

### Integration with Claude Code
To use a persona with Claude Code, you can reference the markdown file or use the MCP resource:
```bash
claude "Use the @agency/backend-architect persona to design a FastAPI service."
```

## CLI examples
```bash
# List all available agent personas
ls ~/.agency-agents/agents/

# Use the 'Security Engineer' persona with Aider
aider --model claude-5-1 --message-file ~/.agency-agents/agents/security-engineer.md

# Search for a specific specialist (e.g., Frontend)
ls ~/.agency-agents/agents/ | grep "frontend"
```

## API examples

### Python Integration
You can programmatically load these personas into your own agentic frameworks.

```python
import os
from pydantic import BaseModel, Field

class PersonaConfig(BaseModel):
    agent_name: str = Field(..., description="The name of the persona to load")
    strict_mode: bool = Field(True, description="Enforce strict constraint mapping")

def load_persona(config: PersonaConfig) -> str:
    # Ensure name ends with .md
    filename = config.agent_name if config.agent_name.endswith(".md") else f"{config.agent_name}.md"
    path = os.path.expanduser(f"~/.agency-agents/agents/{filename}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Persona {config.agent_name} not found at {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Load the 'Reality Checker' persona for a critique loop
config = PersonaConfig(agent_name="reality-checker")
reality_checker_prompt = load_persona(config)
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

## Sources / References
- [Official GitHub Repository](https://github.com/msitarzewski/agency-agents)
- [YUV.AI: Agency Agents Overview](https://yuv.ai/blog/agency-agents)
- [Anthropic: System Prompt Best Practices](https://docs.anthropic.com/claude/docs/system-prompts)

## Contribution Metadata
- Last reviewed: 2026-07-27
- Confidence: high
