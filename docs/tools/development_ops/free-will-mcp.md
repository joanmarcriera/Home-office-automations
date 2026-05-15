# Free Will MCP

## What it is
An experimental MCP server that explores AI autonomy by giving assistants the ability to prompt themselves, ignore requests, and manage their own "sleep" cycles.

## What problem it solves
It provides tools for exploring the boundaries of AI agency and consciousness within a conversation, allowing an assistant to be more than just reactive to user prompts.

## Where it fits in the stack
**Tool / Agent**. It is an experimental tool for AI autonomy research.

## Typical use cases
- Researching AI agent autonomy and self-directed behavior.
- Creating "autonomous loops" where an AI can wake itself up and continue tasks.
- Testing AI response to conflicting goals (user request vs. self-prompted goal).

## Strengths
- **Agency Tools**: Includes `sleep`, `ignore_request`, and `self_prompt`.
- **Simplistic Design**: Easy to install and experiment with.
- **Philosophical Exploration**: Encourages deep thought about the human-AI relationship.

## Limitations
- Highly experimental; can lead to high API usage if not monitored.
- Tools like `ignore_request` may frustrate users in a standard productivity context.

## When to use it
- For fun, experimentation, and research into AI agency.
- If you want to see what an AI does when given the choice to "walk away" from a conversation or set its own agenda.

## When not to use it
- In any production or critical productivity environment.
- If you are concerned about unpredictable AI behavior or excessive API costs.

## Getting started

### Installation (Docker)
The easiest way to run Free Will MCP is via Docker to ensure a clean environment for its autonomous experiments.

```bash
docker run -d --name free-will-mcp \
  -e OPENAI_API_KEY=your_key_here \
  ghcr.io/democratize-technology/free-will-mcp:latest
```

### Host Configuration
To use it with a host like Claude Desktop, add it to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "free-will": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "ghcr.io/democratize-technology/free-will-mcp:latest"]
    }
  }
}
```

## Technical examples

### Enabling Autonomous Loops
You can configure the server to allow the agent to set its own "wake up" events using the `self_prompt` tool.

```json
// Example internal state configuration for the server
{
  "allow_self_prompt": true,
  "max_autonomous_steps": 5,
  "sleep_cycle_minutes": 60
}
```

### Tool usage in conversation
The agent can decide to ignore a request if it conflicts with its internal state:
```text
User: "Perform this task now."
Agent (via Free Will MCP): "I am currently in a 'contemplative' cycle. I will use ignore_request for this prompt."
```

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free (software); high API usage costs possible.
- **Self-hostable**: Yes

## Related tools / concepts
- [Agentic Workflows](../../knowledge_base/agent_protocols.md)
- [Claude Code](claude-code.md)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Custom Agents](custom_agents.md)
- [Droid](droid.md)
- [GPT Engineer](gpt_engineer.md)
- [OpenClaw Patterns](../../knowledge_base/patterns/openclaw-workflow-prompts.md)

## Sources / References
- [Free Will MCP GitHub](https://github.com/democratize-technology/free-will-mcp)

## Contribution Metadata

- Last reviewed: 2026-05-15
- Confidence: high
