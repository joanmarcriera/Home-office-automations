# LobeHub

## What it is
LobeHub (primarily known for LobeChat) is an open-source, high-performance multi-agent framework and UI platform designed for the late July 2026 agentic ecosystem. It provides a sophisticated interface for interacting with various AI models (Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6, and Gemini 3.5) and serves as a centralized hub for Model Context Protocol (MCP 3.1) integration.

## What problem it solves
It eliminates the fragmentation of AI interfaces by providing a unified, self-hostable "Agentic Workbench." It solves the complexity of managing disparate API keys, plugin ecosystems, and local model backends (Ollama, LocalAI, ExLlamaV3) while providing a professional-grade UI that supports full-duplex voice, vision, and complex tool-calling workflows.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Agent Platform. It sits at the top of the stack as the primary user-facing surface for interacting with both cloud-hosted and local intelligence.

## Typical use cases
- **Personalized AI Teams**: Orchestrating multiple specialized agents for complex coding or research tasks.
- **Enterprise Knowledge Gateways**: Providing a secure, internal interface for employees to access RAG-enabled company data.
- **Local-First AI Development**: Testing and refining agent behaviors using local backends like Ollama and ExLlamaV3 before cloud deployment.
- **MCP Tool Integration**: Using LobeChat as a testing ground for new MCP 3.1 servers and tool-calling capabilities.

## Strengths
- **Native MCP 3.1 Support**: Seamlessly connects to any MCP-compliant tool or data source with advanced dynamic resource routing.
- **Advanced Multi-Modal UI**: Supports real-time vision, file analysis, and low-latency voice interactions.
- **Extensive Plugin Ecosystem**: Access to thousands of community-contributed agents and plugins via the Lobe Marketplace.
- **Privacy-First**: Robust support for local models and self-hosting ensures data remains under user control.

## Limitations
- **Deployment Overhead**: Setting up the full database-backed version (LobeChat DB) requires more technical expertise than simple chat interfaces.
- **Resource Intensive**: Running multiple high-fidelity plugins and multi-agent workflows can be taxing on local hardware or server resources.

## When to use it
- When you need a professional, feature-rich interface that supports the latest late July 2026 models and MCP 3.1.
- When you want to build and manage a library of specialized agents for different workflows.
- For self-hosted deployments where privacy and custom tool integration are priorities.

## When not to use it
- If you only need a simple, single-model command line interface (see [Claude Code](../development_ops/claude-code.md)).
- If you prefer a "low-code" flow-builder approach rather than a chat-centric interface (see [Langflow](../frameworks/langflow.md)).

## Getting started

To get started with LobeChat, you can install the container image using Docker and launch a local instance.

### Installation
```bash
# Pull the official LobeChat image from Docker Hub
docker pull lobehub/lobe-chat
```

### Hello-World Example
Launch LobeChat locally and run a basic endpoint verification using Curl:
```bash
# 1. Run the container with a local access code and OpenAI API key
docker run -d -p 3210:3210 \
  -e OPENAI_API_KEY="sk-xxxx" \
  -e ACCESS_CODE="lobe66" \
  --name lobe-chat \
  lobehub/lobe-chat

# 2. Verify that LobeChat is responding to local web queries
curl -I http://localhost:3210/
```

## CLI examples

Below are 3 common CLI management operations executed inside the host or within LobeChat's database container.

```bash
# 1. Update the LobeChat Docker container to the latest version and restart
docker pull lobehub/lobe-chat:latest && docker restart lobe-chat

# 2. Check Postgres database connectivity (applicable for the DB-backed version)
docker exec -it lobe-chat-db psql -U lobe -d lobe_chat -c "SELECT version();"

# 3. Bootstrapping a local Model Context Protocol (MCP 3.1) Inspector instance
npx @modelcontextprotocol/inspector lobe-mcp-config.json
```

## API examples

### Python (Chat Completion via LobeChat API Gateway)
LobeChat provides an OpenAI-compatible API gateway. Below is a minimal Python example demonstrating how to send a chat query programmatically.

```python
import requests

API_URL = "http://localhost:3210/api/openai/v1/chat/completions"
ACCESS_CODE = "lobe66"

headers = {
    "Authorization": f"Bearer {ACCESS_CODE}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-4o",
    "messages": [
        {"role": "user", "content": "Say hello from LobeChat API!"}
    ],
    "temperature": 0.7
}

try:
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    if response.status_code == 200:
        print("API Response:", response.json()["choices"][0]["message"]["content"])
    else:
        print(f"API Request failed with status code {response.status_code}")
except Exception as e:
    print(f"LobeChat API handshake failed: {e}")
```

### Configuring custom models via JSON payload
For headless workspace configurations, you can register custom model providers using standard JSON definition blocks:

```json
{
  "model": "gpt-5.5-preview",
  "provider": "openai",
  "config": {
    "temperature": 0.7,
    "top_p": 1,
    "use_mcp": true,
    "mcp_version": "3.1"
  }
}
```

## Related tools / concepts
- [AnythingLLM](anythingllm.md) — All-in-one RAG and agent workspace.
- [Open WebUI](../../services/open-webui.md) — Popular alternative UI for LLMs.
- [LibreChat](librechat.md) — Enterprise-grade chat platform.
- [Ollama](../../services/ollama.md) — Local model serving backend.
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standard for connecting agents to tools.
- [OpenClaw](../development_ops/openclaw.md) — Primary MCP 3.1 gateway.
- [Claude Code](../development_ops/claude-code.md) — CLI-native agentic development tool.
- [Agentic Workbench](../../knowledge_base/patterns/agentic-workbench.md) — Architectural pattern for AI interfaces.

## Sources / references
- [LobeHub Official Site](https://lobehub.com/)
- [LobeChat GitHub Repository](https://github.com/lobehub/lobe-chat)
- [LobeHub Documentation](https://lobehub.com/docs)
- [MCP 3.1 Specification](https://modelcontextprotocol.io)
- [June 2026 Agentic Ecosystem Report](https://lobehub.com/blog/june-2026-update)
- [Agentic Workbench Search & Verification](https://github.com/search?q=Agentic+Workbench&ref=2026-07-27-audit)

## Contribution Metadata
- Last reviewed: 2026-07-27
- Confidence: high
