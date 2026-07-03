# Chatbox AI

## What it is
Chatbox AI is a comprehensive, multi-platform AI client that allows users to access a wide range of frontier models (including **Claude 4.8 Opus**, **GPT-5.5**, **Gemini 2.0**, and local models via **Ollama**) through a unified, privacy-focused interface. As of July 2026, it is a leading "cockpit" for human-AI collaboration, available on Windows, macOS, Linux, iOS, Android, and the web.

## What problem it solves
It centralizes AI interaction, eliminating the need to manage multiple browser tabs or individual subscriptions for different providers. By allowing users to "Bring Your Own Key" (BYOK), it provides a cost-effective and privacy-conscious way to use high-end AI models while keeping conversation history, custom agents, and settings synchronized across all devices with end-to-end encryption.

## Where it fits in the stack
**AI Consumption & Interaction Layer**. It acts as a sophisticated front-end for various API providers and local inference engines. It now natively supports the **Model Context Protocol (MCP) 3.0**, allowing the client to act as a host for diverse tool-using agents.

## Typical use cases
- **Multi-Device Research**: Starting a complex research prompt on a desktop and continuing the conversation seamlessly on a mobile device while commuting.
- **Local LLM UI**: Using Chatbox as a polished, high-performance front-end for models running locally via Ollama or LM Studio.
- **Agentic Workflows**: Deploying "Agentic Presets" within the chat for specialized tasks like code auditing or market analysis.
- **Privacy-First Collaboration**: Storing all conversation data locally or in an encrypted cloud sync, ensuring sensitive data never trains provider models.

## Strengths
- **Native Multi-Platform Support**: Consistent, high-quality experience across desktop and mobile.
- **MCP 3.0 Integration**: Can connect to any MCP-compliant server for local tool execution and data retrieval.
- **Broad Model Support**: Direct integration with OpenAI, Anthropic, Google, DeepSeek, and local providers.
- **Superior Artifact Handling**: Modern "Artifacts" view for code, documents, and web previews, similar to Claude's native interface.

## Limitations
- **Semi-Proprietary**: While the issue tracker and some components are public, the core application remains closed-source.
- **Sync Requires Subscription**: Advanced features like cross-device synchronization and certain "Agentic Presets" require a Pro subscription.
- **Limited to Chat-centric Agents**: While it supports tool-use, it is primarily a chat interface and lacks the deep filesystem automation of dedicated CLI agents like [Claude Code](../development_ops/claude-code.md).

## When to use it
- If you use multiple different AI models daily and want a single, high-quality application to manage them.
- If you value having your AI history and custom agents available on your mobile device as well as your workstation.
- When you want to use frontier models like Claude 4.8 with local tools via MCP 3.0 without writing custom code.

## When not to use it
- For tasks requiring fully autonomous, filesystem-level agentic behavior (use [Claude Code](../development_ops/claude-code.md) or [Aider](../development_ops/aider.md)).
- If your workflow requires a 100% open-source software stack (use [LibreChat](librechat.md)).

## Getting started

### Installation
1.  **Desktop**: Download the latest installer from [ChatboxAI.app](https://chatboxai.app/).
2.  **Mobile**: Install from the [App Store](https://apps.apple.com/app/chatbox-ai/id6471368056) or [Google Play](https://play.google.com/store/apps/details?id=xyz.chatboxapp.chatbox).
3.  **Setup**: Open **Settings** > **Model**, select your provider (e.g., Anthropic), and enter your API key.

### Configuring MCP
1.  Go to **Settings** > **MCP Servers**.
2.  Add a new server by providing its name and endpoint (e.g., `http://localhost:3000`).
3.  Chatbox will automatically discover and enable tools for the current model.

## CLI examples

Chatbox is primarily a GUI application, but its data and configuration can be managed on desktop systems.

### Inspecting Local Data (macOS/Linux)
```bash
# Locate the Chatbox data directory to inspect local sqlite history
ls ~/Library/Application\ Support/chatbox/ # macOS
ls ~/.config/chatbox/ # Linux
```

### Scripting Configuration
```bash
# Example of programmatically updating the configuration (JSON)
# Use with caution while the application is closed
jq '.ai_provider = "Anthropic" | .api_key = "sk-ant-..." ' config.json > config.new.json
```

## API examples

### Connecting to Ollama (Local API)
In the Chatbox Settings:
1.  Select **Provider**: `Ollama`.
2.  **API Host**: `http://localhost:11434`.
3.  **Model**: Select your local model (e.g., `llama4-maverick`).

### Custom OpenAI-Compatible Endpoint
```json
{
  "name": "Local Gateway",
  "api_key": "not-needed",
  "base_url": "http://192.168.1.50:8000/v1",
  "model": "mistral-large-2026"
}
```

## Related tools / concepts
- [TypingMind](typingmind.md) — The primary competitor for professional AI chat interfaces.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The standard for client-tool communication.
- [Ollama](../../services/ollama.md) — The standard local LLM runner supported by Chatbox.
- [Claude](claude.md) — Anthropic's flagship models supported by Chatbox.
- [ChatGPT](chatgpt.md) — OpenAI's models supported by Chatbox.
- [LibreChat](librechat.md) — An open-source multi-model chat interface.
- [Jan.ai](../infrastructure/jan-ai.md) — Local-first AI desktop client.
- [LM Studio](../infrastructure/lm-studio.md) — Local model runner and discovery tool.

## Sources / references
- [Chatbox AI Official Site](https://chatboxai.app/)
- [Chatbox AI GitHub (Issue Tracker)](https://github.com/Bin-Huang/chatbox)
- [MCP Integration Guide for Chatbox](https://chatboxai.app/docs/mcp)

## Contribution Metadata
- Last reviewed: 2026-07-02
- Confidence: high
