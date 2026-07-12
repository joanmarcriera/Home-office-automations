# Superinterface

## What it is
Superinterface is an open-source framework and platform for building and deploying AI assistants with production-ready user interfaces. It provides a set of React components and a backend infrastructure to handle streaming, tool calls, and conversation state. As of July 2026, it supports advanced agentic features including **Computer Use**, native **MCP 3.0 Task Protocol** integration, and **Interactive Components** optimized for **Gemma 3**.

## What problem it solves
It bridges the gap between AI agents and the end-user by providing a structured way to build conversational and interactive interfaces. It eliminates the need to build custom UI components for complex agentic behaviors like file handling, multi-modal streaming, and **Computer Use** (controlling virtual environments). The integration with **FastMCP 3.0** ensures low-latency tool interactions.

## Where it fits in the stack
**Framework / UI Library / Assistant Backend**.

## Typical use cases
- **AI-Powered Customer Portals**: Building chat interfaces that support **Interactive Components** like forms, surveys, and cards for structured data entry.
- **Agentic Desktop Controls**: Utilizing **Computer Use** (via Anthropic or OpenRouter) to allow assistants to control virtual machines or browsers.
- **Enterprise Assistant Backend**: Deploying a self-hosted backend (using `@superinterface/server`) that integrates with internal **MCP 3.0** tool servers.
- **Real-time Voice Assistants**: Implementing low-latency voice interactions using the OpenAI **Realtime API** or specialized **Gemma 3** audio pipelines.

## Strengths
- **Native MCP 3.0 Support**: Seamlessly connects assistants to any MCP tool server for expanded capabilities.
- **Rich UI Library**: Customizable React components for threads, messages, and complex media (image/video/audio).
- **Interactive Components**: Allows agents to present structured UI elements (forms, carousels) directly within the chat.
- **Developer-Centric Tools**: Comprehensive **Tools REST API** for managing assistant capabilities programmatically.

## Limitations
- **React Dependency**: The frontend library is strictly built for React/Next.js and Radix-UI ecosystems.
- **Infrastructure Requirements**: Self-hosting the full server stack requires managing a database and streaming infrastructure.

## When to use it
- When you want to build a feature-rich, multi-modal AI chat interface with minimal frontend development effort.
- When you require advanced agentic capabilities like **Computer Use** or native **MCP** tool integration.
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

### MCP Server Registration
```bash
superinterface mcp register --url http://localhost:8080/mcp
```

## API examples

### Creating a Tool via REST API
```bash
curl -X POST https://api.superinterface.ai/api/cloud/assistants/{assistantId}/tools \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"type": "web_search"}'
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
- Last reviewed: 2026-07-21
- Confidence: high
