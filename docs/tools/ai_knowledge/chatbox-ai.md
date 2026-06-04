# Chatbox AI

## What it is
Chatbox AI is a powerful, multi-platform AI client application that connects users with leading AI models (OpenAI, Claude, Gemini, and more) through a consistent interface on desktop, mobile, and web.

## What problem it solves
It eliminates the need to switch between different AI provider websites by providing a universal, privacy-focused client that stores data locally and synchronizes across all devices.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Multi-model Client

## Typical use cases
- **Cross-Platform AI Access**: Having the same AI context and history available on Windows, macOS, Android, and iOS.
- **Local Data Management**: Ensuring conversations are stored securely on your own device rather than on provider servers.
- **Developer Productivity**: Using specialized features like artifact previews and syntax highlighting for coding tasks.

## Strengths
- **Universal Availability**: Works on almost any platform (Windows, MacOS, Linux, Android, iOS, Web).
- **Privacy-First**: Strong emphasis on local data storage and secure cross-device sync.
- **Intuitive Interface**: Clean, accessible UI that supports file uploads, image generation, and real-time web search.

## Limitations
- **Proprietary Software**: The client application is not fully open source.
- **Cost for Pro Features**: While basic usage is free (BYO API key), advanced features like cloud sync may require a subscription.

## When to use it
- If you use multiple AI models throughout the day and want a single, high-quality app to manage them all.
- If you need a reliable mobile AI client that stays in sync with your desktop work.

## When not to use it
- If you require a fully open-source stack for auditing or contribution.
- If you are looking for an agentic framework that can perform autonomous actions on your local filesystem (see [Aider](../development_ops/aider.md)).

## Getting started

### Installation
1.  **Desktop**: Download the installer for Windows (.exe), macOS (.dmg), or Linux (.AppImage) from the [Official Downloads](https://chatboxai.app/).
2.  **Mobile**: Install via the [Apple App Store](https://apps.apple.com/app/chatbox-ai/id6471368056) or [Google Play Store](https://play.google.com/store/apps/details?id=xyz.chatboxapp.chatbox).
3.  **Web**: Access the client directly at [chatboxai.app](https://chatboxai.app/).

### Basic Configuration
1.  Launch Chatbox and open **Settings** (gear icon).
2.  Navigate to **AI Provider**.
3.  Select your provider (e.g., OpenAI) and enter your **API Key**.
4.  Choose your desired **Model** (e.g., gpt-4o) and click **Save**.

## Technical configuration

Chatbox allows for advanced configuration, including connecting to local LLMs or custom API endpoints.

### Connecting to Ollama (Local)
1.  Ensure [Ollama](../../services/ollama.md) is running locally.
2.  In Chatbox Settings, set **AI Provider** to `Ollama`.
3.  Set the **API Host** to `http://localhost:11434/v1`.
4.  Select your local model (e.g., `llama3`) from the dropdown.

### Custom API Configuration (JSON)
For providers not natively listed, use the "Custom OpenAI-compatible" option:

```json
{
  "provider": "OpenAI-Compatible",
  "api_key": "your-api-key",
  "base_url": "https://your-custom-proxy.com/v1",
  "model": "your-model-name"
}
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Free (Client download) / Paid (Cloud services and premium features)
- **Self-hostable**: No (Client-side application)

## Related tools / concepts
- [Jan.ai](../infrastructure/jan-ai.md) — Local-first AI desktop client.
- [LM Studio](../infrastructure/lm-studio.md) — Tool for discovering and running local LLMs.
- [Msty](../infrastructure/msty.md) — Multi-model AI client with focus on local privacy.
- [Aider](../development_ops/aider.md) — Terminal-based pair programmer.
- [Ollama](../../services/ollama.md) — Local LLM runner.
- [Perplexity](perplexity.md) — AI-powered search engine.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's official CLI coding assistant.

## Sources / References
- [Chatbox AI Official Site](https://chatboxai.app/)
- [Chatbox AI GitHub](https://github.com/Bin-Huang/chatbox)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
