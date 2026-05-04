# Agency-Agents

## What it is
Agency-Agents is a comprehensive suite of 110+ specialized AI agent personas designed to transform generic coding assistants into a "complete AI agency." It provides markdown-based system prompts for roles ranging from Frontend Architects to Security Engineers and Reality Checkers.

## What problem it solves
It reduces AI hallucinations and improves code quality by providing "off-the-shelf" expert personas with predefined identities, missions, and success metrics. It moves away from generic "write code" prompts to specialized, opinionated domain expertise.

## Where it fits in the stack
**Category**: Agent / Personas / Framework. It acts as a configuration layer for IDE-based agents like Claude Code, Cursor, and Aider.

## Typical use cases
- **Multi-agent IDE Workflows**: Invoking a "Backend Architect" for design and a "Security Engineer" for review.
- **Reality Checking**: Using the "Reality Checker" persona to find flaws in proposed solutions.
- **Specialized Automation**: Deploying "Reddit community ninjas" or "Whimsy injectors" for niche business tasks.

## Getting started

### Installation
```bash
# Clone the repository to your local machine
git clone https://github.com/msitarzewski/agency-agents.git ~/.agency-agents
```

### Integration with Claude Code
To use a persona with Claude Code, you can reference the markdown file in your system prompt or initial query:
```bash
claude "Use the instructions in ~/.agency-agents/agents/backend-architect.md to design a FastAPI service."
```

## CLI examples
```bash
# List all available agent personas
ls ~/.agency-agents/agents/

# Use the 'Security Engineer' persona with Aider
aider --model claude-3-5-sonnet-20241022 --message-file ~/.agency-agents/agents/security-engineer.md

# Search for a specific specialist (e.g., Frontend)
ls ~/.agency-agents/agents/ | grep "frontend"
```

## API examples
While primarily markdown-based, you can use these personas in your own Python agents:

```python
import os

def load_persona(agent_name):
    path = os.path.expanduser(f"~/.agency-agents/agents/{agent_name}.md")
    with open(path, "r") as f:
        return f.read()

# Load the 'Reality Checker' persona
reality_checker_prompt = load_persona("reality-checker")

# Use it with your favorite LLM client
# response = client.chat(messages=[{"role": "system", "content": reality_checker_prompt}, ...])
```

## Strengths
- **High Specialization**: 110+ personas covering almost every development and business role.
- **Model Agnostic**: Works with any LLM (Claude, GPT, Gemini) through any interface.
- **Improved Grounding**: Drastically reduces hallucinations by narrowing the agent's focus.

## Limitations
- **Manual Integration**: Requires cloning and manual referencing in most tools.
- **Persona Maintenance**: Prompts may need adjustment as models evolve.

## When to use it
- When you need more than just a general-purpose assistant and want a "team" of experts.
- For business workflows that map well to traditional agency roles.

## When not to use it
- For simple tasks where a single general assistant (e.g., Claude or ChatGPT) is sufficient.

## Related tools / concepts
- [Claude Code](../ai_knowledge/claude-code.md)
- [Aider](../development_ops/aider.md)
- [CrewAI](../frameworks/crewai.md)
- [AutoGen](../frameworks/autogen.md)
- [OpenClaw](../development_ops/openclaw.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / References
- [Official GitHub Repository](https://github.com/msitarzewski/agency-agents)
- [YUV.AI: Agency Agents Overview](https://yuv.ai/blog/agency-agents)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high
