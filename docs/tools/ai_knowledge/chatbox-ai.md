# Chatbox AI

## What it is
Chatbox AI is a comprehensive, multi-platform AI client that allows users to access a wide range of frontier models (including **Claude 4.8 Opus**, **GPT-5.5**, **Gemini 2.0**, and local models via **Ollama**) through a unified, privacy-focused interface. It is available on Windows, macOS, Linux, iOS, Android, and as a web-based client.

## What problem it solves
It centralizes AI interaction, eliminating the need to manage multiple browser tabs or individual subscriptions for different providers. By allowing users to "Bring Your Own Key" (BYOK), it provides a more cost-effective and privacy-conscious way to use high-end AI models while keeping conversation history and context synchronized across all devices.

## Where it fits in the stack
**AI Consumption & Interaction Layer**. It acts as the primary "cockpit" for human-AI collaboration, sitting on top of various API providers and local inference engines.

## Typical use cases
- **Cross-Platform Workflows**: Starting a complex coding prompt on a desktop and continuing the conversation on a mobile device.
- **Local LLM Interaction**: Using the Chatbox UI as a front-end for models running locally via Ollama or LM Studio.
- **Developer Productivity**: Leveraging the "Artifacts" and "Source Code Preview" features to iterate on web components or scripts.
- **Privacy-Sensitive Research**: Storing all conversation data locally rather than on provider servers.

## Strengths
- **Multi-Model Support**: Native integration with almost all major AI providers and local runners.
- **Seamless Sync**: Robust, encrypted synchronization of history and settings across desktop and mobile.
- **User Experience**: Clean, modern interface with support for image generation, file uploads, and voice-to-text.
- **Privacy First**: Strong emphasis on local data storage and end-to-end encryption for cloud sync.

## Limitations
- **Closed Source Client**: The core application is proprietary, which may be a concern for extreme privacy advocates.
- **Subscription for Sync**: While the client is free to use with your own keys, certain "Pro" features like cloud synchronization require a paid subscription.
- **Limited Autonomy**: Unlike agentic frameworks (e.g., [Aider](../development_ops/aider.md)), Chatbox is primarily a chat interface and does not autonomously modify local files.

## When to use it
- If you use multiple different AI models daily and want a single high-quality app to manage them.
- If you value having your AI history available on your phone as well as your workstation.
- When you want to use frontier models like Claude 4.8 Opus without using the official web interface.

## When not to use it
- For tasks requiring fully autonomous agentic behavior (use [Claude Code](../development_ops/claude-code.md)).
- If you require a 100% open-source software stack.

## Getting started

### Installation
1.  **Desktop**: Download the installer from the [Official Website](https://chatboxai.app/).
2.  **Mobile**: Install from the [App Store](https://apps.apple.com/app/chatbox-ai/id6471368056) or [Google Play](https://play.google.com/store/apps/details?id=xyz.chatboxapp.chatbox).
3.  **Setup**: Open **Settings** > **Model**, select your provider (e.g., Anthropic), and enter your API key.

## CLI examples

Chatbox is primarily a GUI application, but it can be configured via JSON configuration files on desktop systems.

### Inspecting Local Data (macOS/Linux)
```bash
# Locate the Chatbox data directory to inspect local sqlite history
ls ~/Library/Application\ Support/chatbox/ # macOS
ls ~/.config/chatbox/ # Linux
```

### Scripting Configuration
```bash
# Example of programmatically updating the configuration (JSON)
# Note: Use with caution while the app is closed
jq '.ai_provider = "Anthropic" | .api_key = "sk-ant-..." ' config.json > config.new.json
```

## API examples

### Connecting to Ollama (Local API)
In the Chatbox Settings:
1.  Select **Provider**: `Ollama`.
2.  **API Host**: `http://localhost:11434`.
3.  **Model**: Select your local model (e.g., `llama3.3-70b`).

### Custom OpenAI-Compatible Endpoint
```json
{
  "name": "Local Gateway",
  "api_key": "any",
  "base_url": "http://192.168.1.50:8000/v1",
  "model": "mistral-large-2026"
}
```

## Related tools / concepts
- [Jan.ai](../infrastructure/jan-ai.md) — Local-first AI desktop client.
- [LM Studio](../infrastructure/lm-studio.md) — Tool for running and discovering local models.
- [Ollama](../../services/ollama.md) — The standard local LLM runner.
- [Claude](claude.md) — Anthropic's flagship models supported by Chatbox.
- [ChatGPT](chatgpt.md) — OpenAI's models supported by Chatbox.
- [Perplexity](perplexity.md) — AI search integration.
- [Msty](../infrastructure/msty.md) — Another high-quality multi-model client.

## Sources / references
- [Chatbox AI Official Site](https://chatboxai.app/)
- [Chatbox AI GitHub (Issue Tracker/Wiki)](https://github.com/Bin-Huang/chatbox)
- [Chatbox Pro Features](https://chatboxai.app/pro)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
