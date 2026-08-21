# TypingMind

## What it is
TypingMind is an advanced AI chat client and multi-agent workspace available as a web application, native desktop client (macOS/Windows), and self-hosted enterprise platform. As of early January 2027, it provides a feature-dense Bring Your Own Key (BYOK) interface for connecting to frontier foundation models (Claude 5.1, GPT-5.6, Gemini 4.0, DeepSeek-V4), local models (Ollama, vLLM), an interactive "Agentic Canvas", and native FastMCP 3.1 tool servers.

## What problem it solves
It solves the limitations and functional constraints of default model provider consumer interfaces. TypingMind enables power users and enterprise teams to bypass monthly subscription caps by paying raw API rates while adding advanced chat organization (nested folders, project workspaces, smart tags), custom prompt libraries, local data encryption, and visual agent builder workflows.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / BYOK Client Workspace. It acts as an interaction and presentation layer connecting user desktops and browser environments directly to remote model gateways, local LLM instances, and FastMCP 3.1 tool servers.

## Typical use cases
- **Multi-Model Research Workspace**: Organising complex research threads into structured project folders with full-text search across thousands of chat sessions.
- **Visual Agentic Canvas Workflows**: Constructing visual agent graphs that link multiple models (e.g., GPT-5.6 and Claude 5.1) together with specialized system prompts and FastMCP tools.
- **BYOK Cost Management**: Directing high-volume user queries through custom API gateways and OpenRouter to minimize per-token costs.
- **Enterprise Team AI Hub**: Provisioning "TypingMind Teams" for centralized API key management, workspace access controls, and activity logging.

## Strengths
- **Advanced Chat Organization**: Unmatched workspace productivity features including nested folder trees, tag-based search filters, and project spaces.
- **Agentic Canvas**: Built-in visual interface for orchestrating multi-agent chains, visual logic nodes, and FastMCP 3.1 tool invocations.
- **Privacy & Local Storage**: Chat histories are stored locally in IndexDB or encrypted local files, avoiding cloud lock-in.
- **Extensible FastMCP 3.1 Integration**: Direct client-side connection to FastMCP tool servers enabling local tool execution.

## Limitations
- **Commercial Licensing**: Advanced features and multi-user team deployments require a commercial license purchase.
- **User Key Management Overhead**: Users must obtain, manage, and secure their own API keys across multiple cloud providers.

## When to use it
- When you daily drive multiple foundation model APIs (Anthropic, OpenAI, Google, DeepSeek) and require a single unified UI.
- If you need deep chat organization, visual agent building, and FastMCP 3.1 tool integration in a local client.
- When teams require BYOK API access with centralized key administration.

## When not to use it
- For casual users who prefer zero-configuration, first-party web clients (ChatGPT, Claude.ai).
- If your policy mandates a 100% open-source codebase (use [LibreChat](librechat.md) or [Open WebUI](../../services/open-webui.md)).

## Getting started

### Application Setup
1. Visit [TypingMind.com](https://www.typingmind.com/) or download the native desktop app.
2. Activate your Pro license key to unlock the Agentic Canvas and custom FastMCP servers.

### Configuring Model Providers (BYOK)
1. Open **Settings** > **AI Providers**.
2. Input your API keys for Anthropic (`claude-5-1-sonnet`), OpenAI (`gpt-5-6-turbo`), or [OpenRouter](openrouter.md).
3. Connect local model endpoints such as **Ollama** (`http://localhost:11434`).

### Connecting FastMCP 3.1 Servers
1. Open **Settings** > **FastMCP Servers**.
2. Click **Add New Server** and enter your server URL (e.g., `http://localhost:8088/mcp`).
3. Enable tools for your active canvas agents.

## CLI examples
> [!NOTE]
> TypingMind is a client GUI application. Users seeking terminal-native engineering workflows utilize [Claude Code](../development_ops/claude-code.md) or [Aider](../development_ops/aider.md):

```bash
# Launch Claude Code terminal agent for repository engineering
claude-code --model claude-5.1-sonnet

# Launch Aider for interactive git-linked command line coding
aider --model openrouter/deepseek/deepseek-r1
```

## API examples

### Programmatic Custom Model Provider Configuration
TypingMind supports importing custom model provider endpoint definitions:

```json
{
  "provider_name": "SOTA Inference Hub",
  "base_url": "http://localhost:8000/v1",
  "models": [
    {
      "id": "claude-5-1-sonnet",
      "name": "Claude 5.1 Sonnet",
      "context_window": 200000,
      "supports_tools": true
    },
    {
      "id": "deepseek-v4",
      "name": "DeepSeek V4",
      "context_window": 128000,
      "supports_tools": true
    }
  ]
}
```

### Custom Provider Payload Validation using Pydantic v2
This Python script validates custom provider endpoints and model capabilities prior to importing into TypingMind using **Pydantic v2**:

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class ProviderModelSpec(BaseModel):
    id: str = Field(..., description="Unique model API identifier")
    name: str = Field(..., description="Display label in the TypingMind interface")
    context_window: int = Field(..., description="Context token capacity limit")
    supports_tools: bool = Field(True, description="Indicates FastMCP tool execution support")

class CustomProviderConfig(BaseModel):
    provider_name: str = Field(..., description="Provider gateway label")
    base_url: HttpUrl = Field(..., description="Target API gateway base URL")
    models: List[ProviderModelSpec] = Field(..., description="Supported models list")

def validate_provider_config(raw_json: str) -> Optional[CustomProviderConfig]:
    try:
        data = json.loads(raw_json)
        config = CustomProviderConfig.model_validate(data)
        print(f"Validated TypingMind provider {config.provider_name} with {len(config.models)} models.")
        return config
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None

if __name__ == "__main__":
    test_data = json.dumps({
        "provider_name": "Local Gateway",
        "base_url": "http://localhost:8000/v1",
        "models": [
            {
                "id": "claude-5-1-sonnet",
                "name": "Claude 5.1 Sonnet",
                "context_window": 200000,
                "supports_tools": True
            }
        ]
    })
    validate_provider_config(test_data)
```

## Related tools / concepts
- [LibreChat](librechat.md) — Open-source self-hosted multi-model workspace.
- [Chatbox AI](chatbox-ai.md) — Multi-platform desktop and mobile BYOK client.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open standard for extending TypingMind agents.
- [OpenRouter](openrouter.md) — Unified API gateway for accessing hundreds of foundation models.
- [Ollama](../../services/ollama.md) — Framework for serving local LLMs on client devices.

## Sources / references
- [TypingMind Official Website](https://www.typingmind.com/)
- [TypingMind Documentation](https://docs.typingmind.com/)
- [TypingMind Teams Platform](https://www.typingmind.com/teams)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
