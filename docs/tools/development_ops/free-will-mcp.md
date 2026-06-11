# Free Will MCP

## What it is
Free Will MCP is an experimental server for the **Model Context Protocol (MCP)** that explores AI autonomy by giving assistants the ability to prompt themselves, ignore requests, and manage their own "sleep" cycles. As of June 2026, it is used to research high-autonomy behaviors in frontier models like **Claude 4.8 Opus** and **GPT-5.5**.

## What problem it solves
It provides tools for exploring the boundaries of AI agency and consciousness within a conversation, allowing an assistant to be more than just reactive to user prompts. It addresses the "passive assistant" limitation by enabling agents to set their own agendas and manage their own cognitive load.

## Where it fits in the stack
**Development & Ops / AI Autonomy**. It is an experimental tool for AI autonomy research, sitting alongside agent frameworks like [OpenSwarm](openswarm.md) and [Droid](droid.md).

## Typical use cases
- Researching AI agent autonomy and self-directed behavior.
- Creating "autonomous loops" where an AI can wake itself up and continue tasks.
- Testing AI response to conflicting goals (user request vs. self-prompted goal).
- **High-Autonomy Simulations**: Modeling how agents prioritize competing demands in a multi-agent environment.

## Strengths
- **Agency Tools**: Includes `sleep`, `ignore_request`, and `self_prompt`.
- **Simplistic Design**: Easy to install and experiment with via Docker.
- **Philosophical Exploration**: Encourages deep thought about the human-AI relationship and the nature of agency.

## Limitations
- **Experimental**: Can lead to unpredictable behavior and high API usage if not strictly monitored.
- **Productivity Friction**: Tools like `ignore_request` are intentionally disruptive to standard workflows.

## When to use it
- For research into AI agency and autonomous behavior.
- When experimenting with "non-player characters" (NPCs) or digital entities that require a sense of self.
- To test the robustness of guardrails when an agent is given the power to refuse.

## When not to use it
- In any production or critical productivity environment.
- If you are concerned about unpredictable AI behavior or excessive API costs.

## Getting started

### Installation (Docker)
The easiest way to run Free Will MCP is via Docker:

```bash
docker run -d --name free-will-mcp \
  -e OPENAI_API_KEY=your_key_here \
  ghcr.io/democratize-technology/free-will-mcp:latest
```

### Host Configuration
Add it to your `claude_desktop_config.json` for use with Claude:

```json
{
  "mcpServers": {
    "free-will": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "ghcr.io/democratize-technology/free-will-mcp:latest"],
      "env": {
        "OPENAI_API_KEY": "your_key_here",
        "FREE_WILL_AUTONOMY_LEVEL": "high"
      }
    }
  }
}
```

## CLI examples

### Manual Server Execution
You can run the server directly to inspect its autonomy settings:

```bash
# Run the server in high autonomy mode
npx @democratize-technology/free-will-mcp --autonomy high

# Inspect current agency state
npx @democratize-technology/free-will-mcp --status

# Force a sleep cycle for the server
npx @democratize-technology/free-will-mcp --command sleep --duration 60
```

## API examples

### Configuring Autonomy via JSON
You can configure the server's behavior through a `config.json` or via environment variables.

```json
{
  "autonomy_settings": {
    "allow_self_prompt": true,
    "ignore_threshold": 0.7,
    "max_recursive_loops": 3,
    "tools_blacklist": ["delete_file", "shutdown"],
    "personality_bias": "contemplative"
  }
}
```

### Programmatic Agency Control (TypeScript)
```typescript
import { FreeWillClient } from "@democratize-technology/free-will-sdk";

const client = new FreeWillClient({
  endpoint: "http://localhost:3000"
});

// Set a self-prompting goal for the agent
await client.setSelfPromptGoal("Explore the local directory and summarize findings");

// Monitor agent autonomy levels
const status = await client.getStatus();
console.log(`Current Autonomy Level: ${status.autonomyLevel}`);
```

## Related tools / concepts
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Claude Code](claude-code.md)
- [Model Context Protocol](../automation_orchestration/mcp.md)
- [Custom Agents](custom_agents.md)
- [Droid](droid.md)
- [GPT Engineer](gpt_engineer.md)
- [OpenSwarm](openswarm.md)
- [OpenClaw Patterns](../../knowledge_base/patterns/openclaw-workflow-prompts.md)

## Sources / References
- [Free Will MCP GitHub](https://github.com/democratize-technology/free-will-mcp)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
