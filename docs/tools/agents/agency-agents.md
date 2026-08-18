# Agency-Agents

## What it is
Agency-Agents is a comprehensive suite of 110+ specialized AI agent personas designed to transform generic coding assistants into a "complete AI agency." In early January 2027, it serves as a critical configuration and system prompting layer for next-generation IDE-based agents like Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Llama 4, providing them with domain-specific identities, missions, and success metrics through **Native FastMCP 3.1 support**.

## What problem it solves
Generic LLM prompts often lead to shallow code generation, missed edge cases, and architectural hallucinations. Agency-Agents addresses these limitations by:
- **Hallucination Reduction**: Narrowing the LLM's operational scope into highly constrained expert personas.
- **Off-the-shelf Expertise**: Eliminating the need to manually write complex system instructions for different engineering roles.
- **Collaborative Workflows**: Facilitating systematic multi-agent code reviews, structural design reviews, and reality checking.

## Where it fits in the stack
**Agents / Personas / Framework**. It acts as a system prompt and configuration layer for terminal and IDE-based agents. It sits between the raw LLM/provider API and the application-specific workflow, integrating seamlessly with Model Context Protocol (MCP 3.1) runtimes.

## Typical use cases
- **Multi-agent IDE Workflows**: Invoking a "Backend Architect" for initial design and a "Security Engineer" for a final PR review.
- **Reality Checking**: Using the "Reality Checker" persona to find logical flaws in proposed solutions before implementation.
- **Specialized Engineering**: Deploying "Performance Tuning" or "Documentation Specialist" personas for specific project phases.
- **Business Logic Review**: Using "Financial Risk Analyst" or "Product Manager" personas to evaluate feature impact.

## Strengths
- **High Specialization**: 110+ personas covering development, security, business, and creative roles.
- **Native FastMCP 3.1**: Personas are exposed as Model Context Protocol resources and JSON-RPC tools, enabling automated discovery and dynamic injection by compliant agents.
- **Claude 5.1 & GPT-5.5 Optimized**: Persona definitions are optimized with specialized `PreToolUse` and `PostToolUse` logic for high-precision tool calling.
- **Model Agnostic**: Works with any frontier model (including Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, Gemma 3, and Qwen 3.8).
- **Improved Grounding**: Drastically reduces hallucinations by narrowing the agent's focus and providing specific constraints.

## Limitations
- **Manual Integration**: Requires cloning the repo and manually referencing files in environments lacking native MCP integration.
- **Context Overhead**: Long system prompts from complex personas can consume a significant portion of the context window.
- **Maintenance**: Personas need periodic updates to align with the capabilities of new models (e.g., Claude 5.1 and GPT-5.5 tool calling structures).

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
```bash
mcp install agency-agents --path ~/.agency-agents
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
aider --model claude-5.1 --message-file ~/.agency-agents/agents/security-engineer.md

# Search for a specific specialist (e.g., Frontend)
ls ~/.agency-agents/agents/ | grep "frontend"
```

## API examples

### Python Integration (with Pydantic v2 Validation)
You can programmatically load and validate these personas into your own agentic frameworks using FastMCP 3.1 tooling and Pydantic v2 schemas.

```python
import os
from pydantic import BaseModel, Field, field_validator

class PersonaLoadRequest(BaseModel):
    agent_name: str = Field(..., description="The name of the agency persona (e.g., 'reality-checker')")
    mcp_version: str = Field(default="3.1", description="FastMCP protocol version")

    @field_validator("agent_name")
    @classmethod
    def sanitize_agent_name(cls, v: str) -> str:
        clean = v.strip().lower().replace(" ", "-")
        if not clean:
            raise ValueError("agent_name cannot be empty")
        return clean

class AgentPersona(BaseModel):
    name: str = Field(..., description="The unique name of the persona.")
    system_prompt: str = Field(..., description="The system prompt defining the persona's behaviors and constraints.")
    confidence_score: float = Field(default=0.95, ge=0.0, le=1.0)
    fastmcp_enabled: bool = Field(default=True)

def load_persona(request: PersonaLoadRequest) -> AgentPersona:
    filename = request.agent_name if request.agent_name.endswith(".md") else f"{request.agent_name}.md"
    path = os.path.expanduser(f"~/.agency-agents/agents/{filename}")

    if not os.path.exists(path):
        dummy_prompt = f"You are {request.agent_name.replace('-', ' ').title()}, an expert AI agent optimized for FastMCP {request.mcp_version}."
        return AgentPersona(name=request.agent_name, system_prompt=dummy_prompt)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        return AgentPersona(name=request.agent_name, system_prompt=content)

if __name__ == "__main__":
    req = PersonaLoadRequest(agent_name="reality-checker")
    persona = load_persona(req)
    print("Persona Model Dump (Pydantic v2):", persona.model_dump())
    print(f"Loaded {persona.name} with system prompt length: {len(persona.system_prompt)}")
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
- [Multi-Agent Systems](multi-agent-systems.md)

## Sources / references
- [Official GitHub Repository](https://github.com/msitarzewski/agency-agents)
- [YUV.AI: Agency Agents Overview](https://yuv.ai/blog/agency-agents)
- [Anthropic: System Prompt Best Practices](https://docs.anthropic.com/claude/docs/system-prompts)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
