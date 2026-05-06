# LobeHub

## What it is
LobeHub is an open-source, collaborative AI agent platform designed for building and managing personalized AI assistants and teams. It features a modern, user-friendly interface that supports a wide range of AI providers and models.

## What problem it solves
It centralizes multiple AI models (OpenAI, Claude, Gemini, Ollama) and an extensive ecosystem of plugins and MCP servers into a single, cohesive workspace for both personal productivity and team collaboration.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Agent Platform

## Typical use cases
- **Personalized AI Assistants**: Creating custom agents for writing, coding, or professional tasks.
- **Multi-Agent Collaboration**: Building and managing teams of agents that specialize in different parts of a workflow.
- **Self-Hosted AI Workspace**: Deploying a private, secure AI interface via Docker.

## Strengths
- **Extensive Ecosystem**: Over 200,000 skills and 30,000+ MCP servers available in its marketplace.
- **Multi-Provider Support**: Switch seamlessly between cloud providers (OpenAI, Anthropic) and local models (Ollama).
- **Modern UI**: Highly refined user experience with support for multi-modal interactions (text, voice, image).

## Limitations
- **Configuration Complexity**: Setting up complex multi-agent workflows can have a steep learning curve.
- **Resource Intensive**: Self-hosting the full platform with multiple plugins requires meaningful server resources.

## When to use it
- When you want a professional-grade, self-hostable interface for all your AI models.
- When you need to build specialized "agent teams" for complex tasks.

## When not to use it
- If you need a extremely lightweight, single-model chat client.
- If you prefer a CLI-first or terminal-integrated workflow (see [Claude Code](../development_ops/claude-code.md)).

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free (Self-hosted) / Freemium (Cloud version with credit system)
- **Self-hostable**: Yes (via Docker)

## Getting started

### Installation (Docker)
The recommended way to self-host LobeHub (Lobe Chat) is via Docker.

```bash
# Using the setup script
bash <(curl -fsSL https://lobe.li/setup.sh)

# Start the service
docker compose up -d
```

### Local Development
```bash
git clone https://github.com/lobehub/lobe-chat.git
cd lobe-chat
pnpm install
pnpm dev
```

## CLI examples

### 1. Initialize Docker Infrastructure
```bash
# Pulls latest images and sets up initial volumes
bash <(curl -fsSL https://lobe.li/setup.sh)
```

### 2. Start with Environment Variables
```bash
docker run -d -p 3210:3210 \
  -e OPENAI_API_KEY=sk-xxxx \
  -e ACCESS_CODE=lobe66 \
  --name lobe-chat \
  lobehub/lobe-chat
```

### 3. Check Service Status
```bash
docker ps | grep lobe-chat
```

## API examples

### Integration with Ollama
LobeHub connects to Ollama via its local endpoint. In LobeHub settings:
1. Navigate to `Language Models` -> `Ollama`.
2. Set `Proxy` to `http://localhost:11434/v1` (or your Ollama server IP).
3. Enable the models you have pulled locally.

### Using MCP Servers
LobeHub supports Model Context Protocol (MCP) servers. To add a tool via MCP:
1. Go to `Plugins` -> `MCP`.
2. Enter the MCP server URL or configure a local executable path.
3. The tools provided by the MCP server will now be available for your agents to use.

## Related tools / concepts
- [AnythingLLM](anythingllm.md)
- [Open WebUI](../../services/open-webui.md)
- [LibreChat](librechat.md)
- [Ollama](../../services/ollama.md)
- [MCP](../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References
- [LobeHub Official Site](https://lobehub.com/)
- [LobeHub GitHub](https://github.com/lobehub/lobe-chat)
- [LobeHub Documentation](https://lobehub.com/docs)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
