# Superinterface

## What it is
Superinterface is an open-source framework and platform for building and deploying AI assistants with production-ready user interfaces. It provides a set of React components and a backend infrastructure to handle streaming, tool calls, and conversation state. As of late November/December 2026, it supports advanced agentic features including **Computer Use**, native **MCP 3.1 Task Protocol** integration, and **Interactive Components** optimized for **Gemma 3** and **Claude 5.1**.

## What problem it solves
It bridges the gap between AI agents and the end-user by providing a structured way to build conversational and interactive interfaces. It eliminates the need to build custom UI components for complex agentic behaviors like file handling, multi-modal streaming, and **Computer Use** (controlling virtual environments). The integration with **FastMCP 3.1** ensures low-latency tool interactions.

## Where it fits in the stack
**Framework / UI Library / Assistant Backend**.

## Typical use cases
- **AI-Powered Customer Portals**: Building chat interfaces that support **Interactive Components** like forms, surveys, and cards for structured data entry.
- **Agentic Desktop Controls**: Utilizing **Computer Use** (via Anthropic, OpenRouter, or local VM endpoints) to allow assistants to control virtual machines or browsers.
- **Enterprise Assistant Backend**: Deploying a self-hosted backend (using `@superinterface/server`) that integrates with internal **MCP 3.1** tool servers.
- **Real-time Voice Assistants**: Implementing low-latency voice interactions using the OpenAI **Realtime API** or specialized **Gemma 3** and **Llama 4** audio pipelines.

## Strengths
- **Native MCP 3.1 Support**: Seamlessly connects assistants to any MCP tool server for expanded capabilities.
- **Rich UI Library**: Customizable React components for threads, messages, and complex media (image/video/audio).
- **Interactive Components**: Allows agents to present structured UI elements (forms, carousels) directly within the chat.
- **Developer-Centric Tools**: Comprehensive **Tools REST API** for managing assistant capabilities programmatically.

## Limitations
- **React Dependency**: The frontend library is strictly built for React/Next.js and Radix-UI ecosystems.
- **Infrastructure Requirements**: Self-hosting the full server stack requires managing a database and streaming infrastructure.

## When to use it
- When you want to build a feature-rich, multi-modal AI chat interface with minimal frontend development effort.
- When you require advanced agentic capabilities like **Computer Use** or native **MCP 3.1** tool integration.
- When you need to self-host your assistant infrastructure for data privacy and security compliance.

## When not to use it
- For backend-only AI tasks that do not require a user interface.
- If you are building a non-React application (e.g., Vue, Svelte, or native mobile without WebView).

## Getting started

### Installation
```bash
npm install @superinterface/react @tanstack/react-query @radix-ui/themes
```

### Self-Hosted Server (Docker)
```bash
docker run -d \
  --name superinterface-server \
  -p 3000:3000 \
  -e DATABASE_URL="your-db-url" \
  supercorp/superinterface-server:latest
```

## CLI examples

### Deployment via CLI
```bash
superinterface deploy --assistant-id <ASSISTANT_ID>
```

### Managing Tools
```bash
superinterface tools add web_search
```

### MCP Server Registration (v3.1)
```bash
superinterface mcp register --url http://localhost:8080/mcp
```

## API examples

### Python API Integration with Pydantic v2 Tool Validation
This copy-pasteable example demonstrates how to configure and register an assistant's tool definition programmatically via Superinterface's REST API, with schema validation backed by **Pydantic v2**.

```python
import os
import requests
from pydantic import BaseModel, Field, ValidationError

# Define structured schema for registering custom tools in Superinterface
class SuperinterfaceToolConfig(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$", description="Alpha-numeric name of the tool")
    description: str = Field(..., min_length=10, description="Detailed tool description for LLM prompting")
    type: str = Field("custom", description="The tool execution type")
    parameters_schema: dict = Field(..., description="The tool's parameters formatted as JSON schema (Pydantic-compliant)")

def register_assistant_tool(assistant_id: str, tool: SuperinterfaceToolConfig):
    api_key = os.getenv("SUPERINTERFACE_API_KEY", "your-api-key")
    url = f"https://api.superinterface.ai/api/cloud/assistants/{assistant_id}/tools"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": tool.name,
        "description": tool.description,
        "type": tool.type,
        "parameters": tool.parameters_schema
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Example Tool Arguments Pydantic Model
class SearchArgs(BaseModel):
    query: str = Field(..., description="The query to search for")
    max_results: int = Field(5, ge=1, le=20, description="Maximum results to return")

try:
    # Build tool config model with parameters_schema generated by Pydantic v2
    config = SuperinterfaceToolConfig(
        name="web_search",
        description="Search Google/Bing web indices for current late 2026 events",
        parameters_schema=SearchArgs.model_json_schema()
    )

    # Send request
    result = register_assistant_tool("assist_123456", config)
    print("Tool successfully registered on Superinterface platform.")
except ValidationError as e:
    print(f"Validation of Superinterface configuration failed: {e}")
except Exception as e:
    print(f"Error calling API: {e}")
```

### Configuring Message Truncation
```json
{
  "truncationType": "LAST_MESSAGES",
  "truncationLastMessagesCount": 15
}
```

## Related tools / concepts
- [Vercel AI SDK](../providers/vercel-ai-gateway.md) — Frontend framework for AI.
- [Dify](../ai_knowledge/dify.md) — LLM application platform.
- [Open WebUI](../../services/open-webui.md) — Popular self-hosted LLM interface.
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standardized tool-calling support.
- [OpenRouter](../ai_knowledge/openrouter.md) — Provider for Computer Use and diverse models.
- [Langflow](langflow.md) — Visual workflow builder.
- [Mastra](mastra.md) — TypeScript-native agent framework.
- [Rivet](rivet.md) — Visual AI programming environment.
- [Gemma 3](../ai_knowledge/local_llms.md) — Supported for local high-performance reasoning.

## Sources / References
- [Official Website](https://superinterface.ai/)
- [Superinterface Changelog](https://superinterface.ai/changelog)
- [GitHub Repository](https://github.com/superinterface/superinterface)
- [Self-hosting Documentation](https://superinterface.ai/docs/self-hosting)

## Contribution Metadata
- Last reviewed: 2026-12-11
- Confidence: high
