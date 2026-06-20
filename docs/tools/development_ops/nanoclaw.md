# NanoClaw

## What it is
NanoClaw is a lightweight, AI-native personal assistant framework designed as a secure, containerized alternative to [OpenClaw](openclaw.md). It runs on the Claude Agent SDK and prioritizes codebase simplicity and OS-level isolation.

## What problem it solves
It addresses the security risks and code complexity of heavy agent frameworks by providing a minimalist, container-first assistant that evolves through self-modification and composable skills. It ensures that agentic workflows remain secure and private.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Personal Assistant. It is a lightweight agent framework for individuals and developers looking for a secure local-first execution environment.

## Typical use cases
- Secure, sandboxed AI assistance for personal local tasks.
- Building custom multi-channel agents (WhatsApp, Telegram, etc.) with strict data isolation.
- Prototyping agent swarms in a low-complexity environment.
- Using Claude 4.8 and GPT-5.5 with local tool-calling via MCP 3.0.

## Strengths
- **Security-First**: Native container isolation; agents run in ephemeral Linux containers by default.
- **Minimalist**: Small codebase, easy to understand and fork for specific needs.
- **Self-Modifying**: Can evolve its own features through code transformations via the [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) protocol.
- **High Efficiency**: Optimized layer templates can reduce token costs by up to 40% compared to unoptimized patterns.

## Limitations
- **Claude-Centric**: Primary optimization is for Claude models; other models may require custom adapter work.
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

### MCP 3.0 Bridge
NanoClaw can bridge local tools to remote agents via MCP 3.0:

```json
{
  "mcpBridge": {
    "enabled": true,
    "port": 3000,
    "allowedTools": ["filesystem", "bash"]
  }
}
```

## Related tools / concepts
- [OpenClaw](openclaw.md) (The heavier "Gateway" alternative)
- [Claude Code](claude-code.md) (Primary setup tool)
- [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) (Evolution protocol)
- [Symphony](../agents/symphony.md)
- [Jules](../ai_knowledge/jules.md) (Automated maintenance agent)
- [vLLM](../infrastructure/vllm.md) (Local inference backend)
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / references
- [Official GitHub Repository](https://github.com/qwibitai/nanoclaw)
- [Official Website](https://nanoclaw.dev/)
- [NanoClaw Security Whitepaper](https://nanoclaw.dev/security)
- [NanoClaw Setup 2026 Guide](https://advenboost.com/nanoclaw-setup/)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
