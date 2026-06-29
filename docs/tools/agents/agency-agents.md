# Agency-Agents

## What it is
Agency-Agents is a comprehensive suite of 110+ specialized AI agent personas designed to transform generic coding assistants into a "complete AI agency." In June 2026, it serves as a critical configuration layer for IDE-based agents like Claude 4.8 Opus and GPT-5.5, providing them with domain-specific identities, missions, and success metrics.

## What problem it solves
It reduces AI hallucinations and improves technical output by providing "off-the-shelf" expert personas. It moves beyond generic "write code" prompts to specialized, opinionated domain expertise—from Frontend Architects and Security Engineers to Reality Checkers and specialized Business Analysts.

## Where it fits in the stack
**Agents / Personas / Framework**. It acts as a system prompt and configuration layer for terminal and IDE-based agents. In June 2026, it features **Native MCP 3.0 support**, allowing personas to be directly instantiated as agentic tools.

## Typical use cases
- **Multi-agent IDE Workflows**: Invoking a "Backend Architect" for initial design and a "Security Engineer" for a final PR review.
- **Reality Checking**: Using the "Reality Checker" persona to find logical flaws in proposed solutions before implementation.
- **Specialized Engineering**: Deploying "Performance Tuning" or "Documentation Specialist" personas for specific project phases.
- **Business Logic Review**: Using "Financial Risk Analyst" or "Product Manager" personas to evaluate feature impact.
- **Agentic Resource Discovery**: Using the MCP 3.0 protocol to dynamically load personas based on current project requirements.

## Strengths
- **High Specialization**: 110+ personas covering development, security, business, and creative roles.
- **Model Agnostic**: Works with any frontier model (Claude, GPT, Gemini) through any interface.
- **Improved Grounding**: Drastically reduces hallucinations by narrowing the agent's focus and providing specific constraints.
- **Native MCP 3.0 Support**: Personas can now be shared and invoked via standard agent protocols.
- **Markdown-First**: Easy to version control, edit, and share across teams.

## Limitations
- **Manual Integration**: Standard usage still requires cloning the repo and manually referencing files in non-MCP tools.
- **Context Overhead**: Long system prompts from complex personas can consume a significant portion of the context window.
- **Configuration Drifts**: Personas may need periodic updates to align with the rapidly evolving tool-calling capabilities of frontier models.

## When to use it
- When you need more than just a general-purpose assistant and want a virtual "team" of experts.
- For complex engineering tasks that require multiple perspectives (architecture, security, testing).
- When using tools like Claude Code, Cursor, or Aider that allow custom system instructions or MCP integration.

## When not to use it
- For simple, one-off tasks where a general-purpose assistant is sufficient.
- If you have already developed highly customized, proprietary system prompts for your specific domain.

## Getting started

### 1. Installation
Clone the repository to your local machine to access the persona library.

```bash
git clone https://github.com/msitarzewski/agency-agents.git ~/.agency-agents
```

### 2. Basic Usage (Claude Code)
Reference a persona file in your initial query to set the agent's expertise.

```bash
claude "Use ~/.agency-agents/agents/backend-architect.md to design a FastAPI service."
```

### 3. MCP 3.0 Integration
Add the Agency-Agents MCP server to your configuration to enable dynamic persona selection.

## CLI examples

```bash
# List all available agent personas
ls ~/.agency-agents/agents/

# Use the 'Security Engineer' persona with Aider (Claude 4.8)
aider --model claude-4-8-opus-20260528 --message-file ~/.agency-agents/agents/security-engineer.md

# Search for specialized roles
ls ~/.agency-agents/agents/ | grep "architect"
```

## API examples

### Python: Programmatic Persona Loading
Load personas directly into your agentic frameworks for custom orchestrations.

```python
import os

def load_persona(agent_name):
    filename = f"{agent_name}.md" if not agent_name.endswith(".md") else agent_name
    path = os.path.expanduser(f"~/.agency-agents/agents/{filename}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Persona {agent_name} not found.")

    with open(path, "r") as f:
        return f.read()

# Example: Use with a Claude 4.8 tool-calling loop
# persona_prompt = load_persona("reality-checker")
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md)
- [Aider](../development_ops/aider.md)
- [CrewAI](../frameworks/crewai.md)
- [AutoGen](../frameworks/autogen.md)
- [OpenClaw](../development_ops/openclaw.md)
- [Model Context Protocol](../automation_orchestration/mcp.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [System Prompt Engineering](../../knowledge_base/patterns/system-prompts.md)
- [AutoGen Studio](../automation_orchestration/autogen-studio.md)

## Sources / references
- [Official GitHub Repository](https://github.com/msitarzewski/agency-agents)
- [YUV.AI: Agency Agents Overview](https://yuv.ai/blog/agency-agents)
- [Anthropic: System Prompt Best Practices](https://docs.anthropic.com/claude/docs/system-prompts)
- [MCP 3.0 Specification](https://modelcontextprotocol.io/spec/3.0)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
