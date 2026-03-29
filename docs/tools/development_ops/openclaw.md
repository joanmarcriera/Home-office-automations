# OpenClaw

## What it is

OpenClaw (formerly Clawdbot) is an open-source, self-hostable autonomous AI agent platform designed for deploying personal and team agents that operate through messaging channels (Telegram, WhatsApp, Discord, Slack), run scheduled tasks, execute multi-step workflows, and manage long-lived memory. It provides a skill marketplace (ClawHub), a modular plugin architecture, and first-class support for local LLMs via LiteLLM.

## What problem it solves

Setting up a personal AI agent that works continuously across messaging apps, remembers context between sessions, and integrates with dozens of services normally requires significant custom engineering. OpenClaw packages that infrastructure — runtime, memory, channel adapters, skill routing, and API integrations — into a composable, self-hosted deployment that non-engineers can configure without writing code for common workflows.

## Where it fits in the stack

**Agent Runtime / Orchestration Layer**. OpenClaw is the execution environment and distribution surface for packaged agent behaviour. It sits above LLMs (local or cloud) and below application-level workflows.

```text
┌─────────────────────────────────────────────────────┐
│           User Channels (Telegram/WhatsApp/CLI)      │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                  OpenClaw Runtime                    │
│  ┌───────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Router   │  │  Skill Bus   │  │   Memory     │  │
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
| **Router** | Receives messages from channels; selects the appropriate skill or default agent loop |
| **Skill Bus** | Loads, validates, and executes installed skills; enforces permissions |
| **Memory** | Conversation history + semantic long-term memory (vector store) |
| **Channel adapters** | Telegram bot, WhatsApp Business API, Discord bot, REST webhook, CLI |
| **Scheduler** | Cron-like task runner for timed or recurring agent actions |
| **LLM Client** | Configurable backend; supports any OpenAI-compatible endpoint |

### Skill system

Skills are self-contained behaviour modules. Each skill defines:
- A **trigger** (keyword, regex, slash-command, or schedule)
- **Instructions** (a system prompt or structured directive)
- **Tool bindings** (HTTP calls, shell commands, MCP server connections)
- **Permissions** (which channels or users may invoke it)

Skills are distributed as files (YAML + Markdown) or packages from ClawHub. They compose: a skill can invoke another skill, pass context forward, or branch based on LLM output.

## Typical use cases

- **Personal assistant via Telegram**: Ask questions, manage tasks, set reminders, trigger home-automation scenes.
- **Research pipeline**: Schedule a nightly research skill that searches the web, summarises findings, and posts a digest to a Slack channel.
- **Code review assistant**: Triggered by a GitHub webhook; summarises a PR diff and posts a review to a messaging channel.
- **Document ingestion**: Receive a forwarded PDF via WhatsApp, extract key fields with an OCR skill, and file it in Paperless-ngx.
- **Scheduled reporting**: Run a data-collection skill every Monday morning and send a structured report.

## Self-hosting

### Docker Compose (minimal)

```yaml
version: "3.9"
services:
  openclaw:
    image: openclaw/openclaw:latest
    restart: unless-stopped
    environment:
      LLM_BASE_URL: "http://litellm:4000"   # LiteLLM proxy or direct Ollama
      LLM_MODEL: "llama3.2"
      TELEGRAM_BOT_TOKEN: "${TELEGRAM_BOT_TOKEN}"
      OPENCLAW_API_KEY: "${OPENCLAW_API_KEY}"
    volumes:
      - ./skills:/app/skills
      - ./data:/app/data
    ports:
      - "3000:3000"

  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    volumes:
      - ./litellm-config.yaml:/app/config.yaml
    ports:
      - "4000:4000"
    command: --config /app/config.yaml
```

### Connecting to local Ollama (TrueNAS stack)

```yaml
# litellm-config.yaml
model_list:
  - model_name: llama3.2
    litellm_params:
      model: ollama/llama3.2
      api_base: http://192.168.0.5:30068   # TrueNAS Ollama
  - model_name: qwen2.5-coder
    litellm_params:
      model: ollama/qwen2.5-coder:7b
      api_base: http://192.168.0.5:30068
```

## Skill installation

### From ClawHub

```bash
# Install a skill from the ClawHub marketplace
openclaw skill install clawhub:telegram-reminder
openclaw skill install clawhub:web-research
openclaw skill install clawhub:paperless-intake

# List installed skills
openclaw skill list

# Enable / disable
openclaw skill enable web-research
```

### Writing a custom skill

```yaml
# skills/daily-summary.yaml
name: daily-summary
description: Posts a morning digest of open tasks and weather
trigger:
  schedule: "0 7 * * *"         # every day 07:00
  keywords: ["morning brief", "daily summary"]
permissions:
  channels: ["telegram:*"]
instructions: |
  You are a concise morning briefing assistant.
  Retrieve the user's open tasks from Vikunja, fetch today's weather,
  and write a 3-bullet summary. Be direct and under 150 words.
tools:
  - vikunja_api
  - weather_api
```

## Integrating with LiteLLM for local model routing

OpenClaw uses an OpenAI-compatible API contract. Point `LLM_BASE_URL` at a LiteLLM proxy to gain:

- **Model fallbacks**: If Ollama is unavailable, fall back to OpenRouter free tier
- **Cost tracking**: All OpenClaw LLM calls logged and attributed
- **Model switching per skill**: Different skills can request different models

```yaml
# litellm-config.yaml — recommended routing for OpenClaw
model_list:
  - model_name: default
    litellm_params:
      model: ollama/llama3.2
      api_base: http://192.168.0.5:30068
    model_info:
      max_tokens: 8192

  - model_name: coding
    litellm_params:
      model: ollama/qwen2.5-coder:14b
      api_base: http://192.168.0.5:30068

  - model_name: fallback
    litellm_params:
      model: openrouter/google/gemma-3-27b-it:free
      api_key: os.environ/OPENROUTER_API_KEY

router_settings:
  fallback_model: fallback
  allowed_fails: 2
```

## Security model

| Risk | Mitigation |
|---|---|
| Skill execution RCE | Run in Docker; skills execute in sandboxed container; no host filesystem access by default |
| Prompt injection via messages | Input sanitisation; strict tool-permission declarations per skill |
| Credential exposure | Secrets via environment variables; never hardcoded in skill YAML |
| Unvetted ClawHub skills | Review skill source before installing; prefer community-vetted or self-authored |
| Channel access control | Per-channel permission lists in skill config; OPENCLAW_API_KEY for REST API |

!!! warning "High-autonomy risk"
    OpenClaw skills can execute shell commands and HTTP calls. Always review skill source before installing from ClawHub. Apply the principle of least privilege in tool bindings.

## Strengths

- **Rapid deployment**: Default configuration deploys in minutes; no custom code for common workflows
- **Skill ecosystem**: ClawHub provides community skills for 100+ common integrations
- **Multi-channel**: Single agent instance serves Telegram, WhatsApp, Discord, Slack, and CLI simultaneously
- **Local-LLM first**: Designed to work offline with Ollama; cloud models are optional
- **Composable**: Skills chain; one skill can trigger another; supports branching logic
- **Scheduler built-in**: No external cron orchestration needed for time-triggered tasks

## Limitations

- **Security governance**: High-autonomy agents require careful review of installed skills; history of RCE vulnerabilities in unpatched versions
- **Token budgets**: Poorly constrained agent loops can consume large amounts of tokens; set model budget limits in LiteLLM
- **Skill quality variability**: ClawHub community skills vary in quality and maintenance; not all are production-grade
- **Complex customisation**: Advanced workflows (conditional branching, multi-agent orchestration) still require skill authoring knowledge
- **Channel rate limits**: WhatsApp Business API and Telegram have message-rate limits that affect high-frequency agents

## When to use it

- When you want a ready-to-run personal assistant that works through messaging apps
- For home-lab automation tied to Ollama, n8n, Paperless-ngx, or Vikunja
- When you want a skill marketplace rather than building all integrations from scratch
- For scheduled agent tasks without a separate cron/n8n workflow
- As a distribution surface for packaged agent behaviours you want to share

## When not to use it

- For mission-critical enterprise workflows without a thorough security review of all installed skills
- If you need fine-grained RBAC and audit logging (use OpenHands Enterprise or a custom agent stack)
- When the task is purely code-centric; [OpenHands](openhands.md) or [Aider](aider.md) are better suited
- If you are uncomfortable maintaining a self-hosted Docker environment

## Comparison with related tools

| Tool | Best for | Autonomy | Local LLM | Skills marketplace |
|---|---|---|---|---|
| **OpenClaw** | Messaging-channel agents, personal assistant | High | Yes (via LiteLLM) | Yes (ClawHub) |
| **OpenHands** | Software engineering tasks, code generation | Very high | Yes (via LiteLLM) | No |
| **NanoClaw** | Constrained, auditable agent loops | Medium | Yes | No |
| **Aider** | Codebase editing, PR generation | Medium | Yes | No |
| **n8n** | Visual workflow automation | Low–Medium | Via node | No |

## Related tools / concepts

- [LiteLLM](../../services/litellm.md) — model routing proxy for connecting OpenClaw to local or remote models
- [OpenHands](openhands.md) — software-engineering agent platform
- [NanoClaw](nanoclaw.md) — minimal, constrained agent runtime
- [Picnic](../automation_orchestration/picnic.md) — desktop product that exposes OpenClaw-powered flows and scheduled agents through a non-technical UI
- [OpenSwarm](openswarm.md) — multi-agent swarm orchestration
- [Ollama](../../services/ollama.md) — local model serving
- [n8n](../../services/n8n.md) — complementary workflow automation
- [OpenClaw Workflow Prompts](../../knowledge_base/patterns/openclaw-workflow-prompts.md) — curated prompt library
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md) — skill authoring guide

## Sources / References

- [GitHub — openclaw/openclaw](https://github.com/openclaw/openclaw)
- [ClawHub Marketplace](https://www.clawhub.ai/)
- [OpenClaw after 50 days: all prompts for 20 real workflows](https://gist.github.com/velvet-shark/b4c6724c391f612c4de4e9a07b0a74b6)
- [Pattern: OpenClaw Workflow Prompts](../../knowledge_base/patterns/openclaw-workflow-prompts.md)

## Contribution Metadata

- Last reviewed: 2026-03-21
- Confidence: high
