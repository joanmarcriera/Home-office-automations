# NanoClaw

## What it is
NanoClaw is a lightweight, AI-native personal assistant framework designed as a secure, containerized alternative to [OpenClaw](openclaw.md). It runs on the Claude Agent SDK and prioritizes codebase simplicity and OS-level isolation, fully supporting the [MCP 3.0 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) for reliable tool execution in July 2026.

## What problem it solves
It addresses the security risks and code complexity of heavy agent frameworks by providing a minimalist, container-first assistant that evolves through self-modification and composable skills. It ensures that agentic workflows remain secure and private by utilizing **FastMCP 3.0** for rapid, type-safe tool discovery and execution.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Personal Assistant. It is a lightweight agent runtime for individuals and developers looking for a secure local-first execution environment that integrates seamlessly with [Gemma 3](../ai_knowledge/local_llms.md) and Claude 4.8.

## Typical use cases
- **Secure AI Assistance**: Sandboxed task execution for personal local automation.
- **Custom Agent Swarms**: Building multi-channel agents (WhatsApp, Telegram, etc.) with strict data isolation.
- **Self-Evolving Skills**: Developing agents that modify their own logic through the [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) protocol.
- **Local Tool-Calling**: Using [Gemma 3](../ai_knowledge/local_llms.md) with local system tools via the MCP 3.0 Bridge.

## Strengths
- **Security-First**: Native container isolation; agents run in ephemeral Linux containers by default.
- **Minimalist**: Small codebase (under 5k LOC), easy to understand and fork for specific needs.
- **FastMCP 3.0 Integration**: Lowest latency for tool registration and execution in the personal assistant category.
- **High Efficiency**: Optimized layer templates reduce token costs by up to 40% compared to unoptimized patterns.

## Limitations
- **Claude-Centric**: Primary optimization is for Claude models, though [Gemma 3](../ai_knowledge/local_llms.md) support is stable via MCP.
- **Self-Modification Risk**: Requires comfort with an assistant that writes its own logic (can be disabled via `NC_READONLY_MODE=true`).
- **Resource Minimums**: Requires at least 4GB RAM and Docker 24+ for the isolation layer to function correctly.

## When to use it
- When you want a personal AI assistant that can be fully understood and customized (low code complexity).
- When you require strong security via Linux container isolation (Apple Container or Docker).
- If you prefer a "skills over features" model where the assistant evolves through code transformations.

## When not to use it
- If you require a managed service or a complex, multi-user enterprise framework.
- If you are not comfortable with an assistant that modifies its own source code to add features.
- For high-concurrency production workloads that require complex orchestration beyond a single node.

## Getting started

### Installation
NanoClaw requires Node.js 22+ and Docker.

```bash
# Clone the repository
git clone https://github.com/qwibitai/nanoclaw.git
cd nanoclaw

# Install dependencies
npm install

# Initialize with Claude Code
claude /setup
```

### Verifying Isolation
To ensure your agent is correctly sandboxed, run:
```bash
nanoclaw exec "echo 'hello' > /root/secret.txt && ls /root"
```
Then verify that a subsequent command or a different container instance cannot see that file.

## CLI examples

### Execution
```bash
# Run a one-off task in the sandbox
nanoclaw task "Organize my downloads folder into categories"

# List active agent containers
nanoclaw ps
```

### Skill Management
```bash
# Add a new skill via natural language
nanoclaw add-skill "Integrate with my local Obsidian vault"

# View installed skills
nanoclaw list-skills
```

## API examples

### Node.js (Agent SDK)
```javascript
import { NanoClaw } from 'nanoclaw';

const agent = new NanoClaw({
  model: 'claude-4-8-sonnet',
  sandbox: true
});

const response = await agent.run("Summarize README.md and suggest 3 improvements.");
console.log(response);
```

### FastMCP 3.0 Bridge
NanoClaw can bridge local tools to remote agents via FastMCP:

```json
{
  "mcpBridge": {
    "enabled": true,
    "port": 3000,
    "protocol": "fastmcp-3.0",
    "allowedTools": ["filesystem", "bash"]
  }
}
```

## Related tools / concepts
- [OpenClaw](openclaw.md) (The heavier "Gateway" alternative)
- [Claude Code](claude-code.md) (Primary setup tool)
- [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) (Evolution protocol)
- [Symphony](../agents/symphony.md) (Agentic orchestration)
- [Jules](../ai_knowledge/jules.md) (Automated maintenance agent)
- [vLLM](../infrastructure/vllm.md) (Local inference backend)
- [Gemma 3](../ai_knowledge/local_llms.md) (Recommended local model)
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md) (Standard for tool use)

## Sources / references
- [Official GitHub Repository](https://github.com/qwibitai/nanoclaw)
- [Official Website](https://nanoclaw.dev/)
- [NanoClaw Security Whitepaper](https://nanoclaw.dev/security)
- [NanoClaw Setup 2026 Guide](https://advenboost.com/nanoclaw-setup/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
