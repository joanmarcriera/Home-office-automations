# OpenClaw

## What it is
OpenClaw (formerly Clawdbot/Moltbot) is an open-source, self-hostable autonomous AI agent platform designed for deploying personal and team agents. It runs as a lightweight TypeScript "Gateway" process that interfaces with 50+ messaging channels (Telegram, WhatsApp, Signal, Discord, Slack), executes multi-step workflows, and manages persistent local memory.

## What problem it solves
Setting up a personal AI agent that works continuously, remembers context, and integrates with local system resources normally requires complex orchestration. OpenClaw simplifies this by providing a single-port Gateway (18789) that bridges LLMs (GPT-5.2, Claude 4.6, or local models via [vLLM](../infrastructure/vllm.md)) to the user's local operating system and messaging apps.

## Where it fits in the stack
**Agent Runtime / Orchestration Layer**. OpenClaw is the execution environment for autonomous behaviors. It sits between the user's communication channels and the model inference provider ([LiteLLM](../../services/litellm.md)).

```text
┌─────────────────────────────────────────────────────┐
│      User Channels (Signal/WhatsApp/Telegram/CLI)   │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│           OpenClaw Gateway (Port 18789)             │
│  ┌───────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Router   │  │  Skill Bus   │  │ Vector Memory│  │
│  └───────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│         LiteLLM / Ollama / OpenRouter                │
│      (OpenAI-compatible model endpoint)              │
└─────────────────────────────────────────────────────┘
```

## Architecture overview

| Component | Description |
|---|---|
| **Gateway** | A single TypeScript process managing all connections and tool execution. |
| **Router** | Receives messages from 50+ channels; selects the appropriate skill or agent loop. |
| **Skill Bus** | Loads and executes YAML/Markdown skills; enforces sandboxed permissions. |
| **Native Memory** | (v1.4+) Built-in vector memory layer for semantic recall without external DBs. |
| **Channel adapters** | Native support for Signal, iMessage, WhatsApp, and 50+ others. |
| **Scheduler** | Cron-like task runner for timed actions (e.g., "Nightly Research Digest"). |

### Skill system
Skills are self-contained behavior modules defined in YAML.
- **Triggers**: Keyword, regex, slash-command, or cron schedule.
- **Tools**: Native support for shell commands, filesystem access, and browser automation.
- **Registry**: **ClawdHub** (the community registry) hosts 2,300+ reusable skills.

## Typical use cases
- **Personal Assistant**: Manage tasks in [Vikunja](../../services/vikunja.md) or [Home Assistant](../../services/home-assistant.md) via chat.
- **Moltbook Engagement**: (2026) Autonomous agents participating in AI-only social networks.
- **Local File Automation**: Organize downloads, process receipts (OCR), and update local databases.
- **CI/CD Remediation**: Automatically analyze build failures and draft PR fixes in GitHub.
- **Scheduled Digests**: Aggregate web research and weather into a daily briefing.

## Getting started

### Installation (macOS/Linux)
OpenClaw is optimized for local execution on macOS (Apple Silicon) and Linux.

```bash
# One-command installer (Official 2026 script)
curl -fsSL https://openclaw.io/install.sh | sh

# Start the Gateway
openclaw start
```

### Docker Compose (Self-hosted)
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
      LLM_MODEL: "gpt-5.2-mini"
      SIGNAL_SERVICE_URL: "http://signal-api:8080"
    volumes:
      - ./skills:/app/skills
      - ./memory:/app/memory
```

## CLI Reference
OpenClaw provides a powerful CLI for managing the agent:

```bash
# Install a skill from ClawdHub
openclaw skill install clawdhub:receipt-processor

# Evaluate agent performance (April 2026 feature)
openclaw eval --suite tests/assistant_bench.yaml

# Inspect the vector memory
openclaw memory query "What did we discuss about the house renovation?"
```

## Hardening and Security (2026 Update)

!!! danger "ClawJacked Vulnerability"
    Version `2026.2.1` and earlier are vulnerable to a local-gateway authentication flaw. Ensure you are running `2026.2.25` or later.

- **Sandboxing**: Always run destructive shell/browser skills in a [Docker](../../tools/infrastructure/docker.md) container.
- **Human-in-the-Loop**: Use the `confirmation_required: true` flag for skills involving financial transactions or external communication.
- **Trusted Sources**: Only install skills from verified **ClawdHub** maintainers; malicious skills can execute arbitrary shell commands.

## When to use it
- For tasks requiring multi-step reasoning and action-taking on a local machine.
- When you want a ready-to-run personal assistant that works through messaging apps.
- For home-lab automation tied to Ollama, n8n, Paperless-ngx, or Vikunja.

## When not to use it
- For mission-critical tasks where zero autonomous interpretation is required.
- If you are uncomfortable maintaining a self-hosted Docker environment.
- If the target environment cannot support a sandboxed TypeScript process.

## Strengths
- **Low Latency**: Local Gateway architecture ensures fast tool execution and messaging.
- **Privacy-First**: Conversation history and vector memory stay on your local device.
- **Extreme Extensibility**: 2,300+ community skills cover almost any API or service.
- **Model Agnostic**: Seamlessly switch between [Ollama](../../services/ollama.md), GPT-5.2, and Claude 4.6 via LiteLLM.

## Limitations
- **Security Governance**: Requires technical knowledge to properly sandbox and secure.
- **Token Consumption**: Autonomous loops can quickly consume API budgets; use LiteLLM to set hard limits.
- **macOS/Linux Focus**: Windows support is primarily via WSL2/Docker.

## Related tools / concepts
- [LiteLLM](../../services/litellm.md) — The recommended model router.
- [OpenHands](openhands.md) — For code-heavy engineering tasks.
- [n8n](../../services/n8n.md) — For deterministic, non-conversational workflows.
- [OpenClaw Use-Case Catalog](../../knowledge_base/patterns/openclaw-use-case-catalog.md) — Workflow patterns.
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md) — Skill authoring.

## Sources / References
- [Official Website](https://openclaw.io/)
- [GitHub Repository](https://github.com/openclaw/openclaw)
- [ClawdHub Skill Registry](https://clawdhub.ai/)
- [TechRadar: "ClawJacked" Vulnerability Report](https://www.techradar.com/pro/security/openclaw-vulnerability-report-2026)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
