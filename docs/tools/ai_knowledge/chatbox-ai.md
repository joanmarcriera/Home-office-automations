# Chatbox AI

## What it is
Chatbox AI is a cross-platform AI desktop and mobile application providing a unified, privacy-focused client interface to frontier models (Claude 5.1, GPT-5.5, Gemini 4.0 Pro) and local runtimes (Ollama, LM Studio). By early January 2027, Chatbox AI acts as a multi-model workspace featuring native **FastMCP 3.1** host capabilities, artifact previews, and end-to-end encrypted session synchronization across macOS, Windows, Linux, iOS, and Android.

## What problem it solves
It centralizes model interaction, eliminating the need to maintain multiple browser tabs, web subscriptions, or separate developer tool interfaces. By allowing users to Bring Your Own Key (BYOK), Chatbox AI provides cost-effective model switching, local history encryption, and zero data-retention training guarantees across personal devices.

## Where it fits in the stack
**AI Assistants & Knowledge / Multi-Provider Client**. It acts as a desktop and mobile frontend for cloud LLM APIs and local inference servers. Through native FastMCP 3.1 integration, it host tools and data connectors for interactive chat agents.

## Typical use cases
- **Multi-Device Research**: Initiating technical prompts on a workstation and continuing research seamlessly on mobile devices via encrypted sync.
- **Local Model GUI**: Providing a high-performance desktop interface for self-hosted SLMs running on local hardware via Ollama or LM Studio.
- **FastMCP 3.1 Tool Workflows**: Connecting local file systems, databases, and APIs directly to model chats using FastMCP 3.1 servers.
- **Artifact Preview & Rendering**: Interactive rendering of generated code snippets, SVG graphics, Markdown documents, and Mermaid diagrams.

## Strengths
- **Native Multi-Platform Ecosystem**: Dedicated, responsive applications across macOS, Windows, Linux, iOS, and Android.
- **FastMCP 3.1 Host Support**: Built-in support for discovering and executing tools from FastMCP 3.1 servers.
- **Broad Model Support**: Direct integration with OpenAI, Anthropic, Google Gemini, OpenRouter, and local OpenAI-compatible endpoints.
- **Interactive Artifacts Viewer**: Clean side-by-side rendering of code, documents, and visual diagrams.
- **Privacy First (BYOK)**: User API keys and conversation histories remain stored locally or securely encrypted in cloud sync.

## Limitations
- **Semi-Proprietary Architecture**: While issue tracking and community plugins are open, core client binaries remain closed-source.
- **Sync Features Require Account**: Multi-device synchronization and premium agent presets require a Chatbox Pro tier.
- **Chat-Centric Scope**: Lacks the deep filesystem automation and terminal control of CLI agents like [Claude Code](../development_ops/claude-code.md).

## When to use it
- When requiring a polished, multi-device chat client to switch seamlessly between Claude 5.1, GPT-5.5, and local models.
- When wanting to utilize FastMCP 3.1 tools in a visual chat desktop interface without building custom UI wrappers.
- When needing encrypted, cross-platform history sync for research and coding notes.

## When not to use it
- For autonomous, terminal-driven code refactoring or repository modification (use [Claude Code](../development_ops/claude-code.md) or [Aider](../development_ops/aider.md)).
- If strict corporate compliance mandates 100% open-source software (prefer [LibreChat](librechat.md)).

## Getting started

### Installation
1. **Desktop**: Download the installer for your OS from [ChatboxAI.app](https://chatboxai.app/).
2. **Mobile**: Install from Apple App Store or Google Play Store.
3. **Configuration**: Open **Settings** > **Model**, choose your provider (e.g., Anthropic or Ollama), and enter your credentials.

### Connecting FastMCP 3.1 Servers
1. Open **Settings** > **MCP Servers**.
2. Register a new server using its endpoint URL (e.g., `http://localhost:3000/mcp`).
3. Chatbox will discover available tools and present them for user authorization during chat turns.

## CLI examples

```bash
# Locate Chatbox local sqlite database and settings on macOS
ls ~/Library/Application\ Support/chatbox/

# Inspect Chatbox configuration on Linux
ls ~/.config/chatbox/

# Backup local Chatbox configuration file
cp ~/.config/chatbox/config.json ~/.config/chatbox/config.json.bak
```

## API examples
### Python: Pydantic v2 Configuration Profile Schema
```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class MCPServerConfig(BaseModel):
    name: str = Field(..., description="Server name")
    url: HttpUrl = Field(..., description="FastMCP 3.1 endpoint")
    enabled: bool = Field(True, description="Active status")

class ProviderProfile(BaseModel):
    name: str = Field(..., description="Profile identifier")
    api_key: str = Field(..., description="Provider secret key or placeholder")
    base_url: Optional[HttpUrl] = Field(None, description="Custom base endpoint URL")
    model: str = Field(..., description="Default model, e.g., claude-5.1-sonnet")
    mcp_servers: List[MCPServerConfig] = Field(default_factory=list, description="Associated FastMCP 3.1 servers")

class ChatboxConfig(BaseModel):
    version: str = Field("2.1.0", description="Configuration schema version")
    active_profile: str = Field(..., description="Active profile name")
    profiles: List[ProviderProfile] = Field(..., description="Registered connection profiles")

def validate_config(raw_json: str) -> Optional[ChatboxConfig]:
    try:
        data = json.loads(raw_json)
        return ChatboxConfig.model_validate(data)
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None

# Test validation
raw_data = '''
{
    "version": "2.1.0",
    "active_profile": "anthropic-prod",
    "profiles": [
        {
            "name": "anthropic-prod",
            "api_key": "sk-ant-...",
            "model": "claude-5.1-sonnet",
            "mcp_servers": [
                {"name": "local-tools", "url": "http://localhost:3000/mcp", "enabled": true}
            ]
        }
    ]
}
'''
config = validate_config(raw_data)
if config:
    print(f"Validated configuration for active profile: {config.active_profile}")
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard protocol for client tool connection.
- [Ollama](../../services/ollama.md) — Local model engine supported by Chatbox.
- [Claude](claude.md) — Anthropic frontier models supported by Chatbox.
- [ChatGPT](chatgpt.md) — OpenAI models supported by Chatbox.
- [LibreChat](librechat.md) — Open-source multi-model web client.
- [Jan.ai](../infrastructure/jan-ai.md) — Local-first AI desktop client.

## Sources / references
- [Chatbox AI Official Site](https://chatboxai.app/)
- [Chatbox AI GitHub Repository](https://github.com/Bin-Huang/chatbox)
- [Chatbox MCP Integration Guide](https://chatboxai.app/docs/mcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
