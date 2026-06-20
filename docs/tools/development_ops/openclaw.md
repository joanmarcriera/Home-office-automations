# OpenClaw

## What it is
OpenClaw (formerly Clawdbot/Moltbot) is an open-source, self-hostable autonomous AI agent platform designed for deploying personal and team agents. It runs as a lightweight TypeScript "Gateway" process that interfaces with 50+ messaging channels (Telegram, WhatsApp, Signal, Discord, Slack), executes multi-step workflows, and manages persistent local memory. As of June 2026, it is the primary execution engine for agentic workflows in the home-office stack.

## What problem it solves
Setting up a personal AI agent that works continuously, remembers context, and integrates with local system resources normally requires complex orchestration. OpenClaw simplifies this by providing a single-port Gateway (18789) that bridges LLMs (GPT-5.5, Claude 4.8, or local models via [vLLM](../infrastructure/vllm.md)) to the user's local operating system and messaging apps. It handles the "last mile" of agent-to-human communication and tool execution.

## Where it fits in the stack
**Agent Runtime / Orchestration Layer**. OpenClaw is the execution environment for autonomous behaviors. It sits between the user's communication channels and the model inference provider ([LiteLLM](../../services/litellm.md)). It utilizes [MCP 3.0](../../tools/automation_orchestration/mcp.md) for seamless tool integration.

## Typical use cases
- **Personal Assistant**: Manage tasks in [Vikunja](../../services/vikunja.md) or [Home Assistant](../../services/home-assistant.md) via chat.
- **Moltbook Engagement**: (2026) Autonomous agents participating in AI-only social networks and decentralized knowledge markets.
- **Local File Automation**: Organize downloads, process receipts (OCR), and update local databases autonomously.
- **CI/CD Remediation**: Automatically analyze build failures and draft PR fixes in GitHub using [Claude Code](claude-code.md).
- **Scheduled Research**: Aggregate web research into a daily briefing via [SearXNG](../../services/searXNG-automation.md).

## Strengths
- **Low Latency**: Local Gateway architecture ensures fast tool execution and messaging compared to cloud-only platforms.
- **Privacy-First**: Conversation history and vector memory stay on your local device or self-hosted infrastructure.
- **Extreme Extensibility**: 2,300+ community skills on **ClawdHub** cover almost any API or service.
- **Model Agnostic**: Seamlessly switch between [Ollama](../../services/ollama.md), GPT-5.5, and Claude 4.8 via LiteLLM.
- **MCP 3.0 Support**: Native integration with the latest Model Context Protocol for unified tool access.

## Limitations
- **Security Governance**: Requires technical knowledge to properly sandbox and secure (see `ClawJacked` vulnerability notes).
- **Token Consumption**: Autonomous loops can quickly consume API budgets; requires [LiteLLM](../../services/litellm.md) budget management.
- **macOS/Linux Focus**: Windows support is primarily via WSL2/Docker, with some native limitations.

## When to use it
- For tasks requiring multi-step reasoning and action-taking on a local machine or home server.
- When you want a ready-to-run personal assistant that works through existing messaging apps like Signal or Discord.
- For home-lab automation tied to Ollama, n8n, Paperless-ngx, or Vikunja.

## When not to use it
- For mission-critical tasks where zero autonomous interpretation is required (use [n8n](../../services/n8n.md) instead).
- If you are uncomfortable maintaining a self-hosted Docker or Node.js environment.
- For purely cloud-native workflows where local system access is not needed.

## Getting started

### Local Installation (macOS/Linux)
OpenClaw is optimized for local execution on macOS (Apple Silicon) and Linux.

```bash
# One-command installer (Official June 2026 script)
curl -fsSL https://openclaw.io/install.sh | sh

# Start the Gateway
openclaw start
```

### Docker Setup (Self-hosted)
For server environments, use Docker to ensure sandboxed tool execution.

```yaml
services:
  openclaw:
    image: openclaw/openclaw:latest
    ports:
      - "18789:18789"
    environment:
      GATEWAY_PORT: 18789
      LLM_BASE_URL: "http://litellm:4000"
      LLM_MODEL: "claude-4-8-opus"
      SIGNAL_SERVICE_URL: "http://signal-api:8080"
    volumes:
      - ./skills:/app/skills
      - ./memory:/app/memory
```

## CLI examples
OpenClaw provides a powerful CLI for managing the agent and its memory:

```bash
# Install a skill from ClawdHub
openclaw skill install clawdhub:receipt-processor

# Evaluate agent performance on a specific suite
openclaw eval --suite tests/assistant_bench.yaml

# Inspect the vector memory
openclaw memory query "What did we discuss about the house renovation?"

# Update to the latest version (v2026.2.25+)
openclaw update
```

## API examples
OpenClaw exposes a REST API (typically on port 18789) for programmatic interaction:

```bash
# Trigger a specific skill via API
curl -X POST http://localhost:18789/api/execute \
  -H "Content-Type: application/json" \
  -d '{"skill": "weather-report", "params": {"location": "San Francisco"}}'

# Query the agent's status
curl http://localhost:18789/api/status
```

## Related tools / concepts
- [LiteLLM](../../services/litellm.md) — The recommended model router and inference plane.
- [Claude Code](claude-code.md) — For agentic coding and terminal-based automation.
- [OpenHands](openhands.md) — For code-heavy engineering tasks.
- [n8n](../../services/n8n.md) — For deterministic, non-conversational workflows.
- [Ollama](../../services/ollama.md) — Local model inference engine.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Standard for agentic tool use.
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md) — Guide for authoring skills.
- [Home Assistant](../../services/home-assistant.md) — Primary IoT integration target.

## Sources / references
- [Official Website](https://openclaw.io/)
- [GitHub Repository](https://github.com/openclaw/openclaw)
- [ClawdHub Skill Registry](https://clawdhub.ai/)
- [TechRadar: "ClawJacked" Vulnerability Report (Fixed in 2026.2.25)](https://www.techradar.com/pro/security/openclaw-vulnerability-report-2026)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
