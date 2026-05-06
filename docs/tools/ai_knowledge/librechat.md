# LibreChat

## What it is
LibreChat is a free, open-source AI conversation platform that provides a unified interface for multiple AI models. It is designed to be a highly customizable and privacy-centric alternative to proprietary chat interfaces like ChatGPT.

## What problem it solves
It eliminates the need to switch between multiple chat interfaces for different AI providers. It also provides a self-hosted option for organizations and individuals who want full control over their data and conversation history.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Self-hosted Chat UI. It serves as a front-end that connects to various LLM backends (OpenAI, Anthropic, Google, local models via Ollama, etc.).

## Typical use cases
- **Unified AI Hub**: A single interface for accessing GPT-4, Claude 3, and local Llama models.
- **Enterprise AI Portal**: Providing a secure, authenticated chat interface for employees with SSO integration.
- **Agentic Workflows**: Utilizing built-in agents with file handling and API actions.
- **Local AI Interface**: Serving as a polished UI for models running locally on a home lab server.

## Strengths
- **Open Source**: Community-driven and fully transparent.
- **Multi-Model Support**: Native support for almost every major AI provider and local inference engine.
- **Advanced Features**: Includes Artifacts (React/HTML/Mermaid), Code Interpreter, and Model Context Protocol (MCP) support.
- **Customizable**: Extensive configuration options for themes, plugins, and system prompts.
- **Privacy-First**: Can be entirely self-hosted with no data sent to third parties (when using local models).

## Limitations
- **Self-Hosting Overhead**: Requires technical knowledge to set up and maintain via Docker.
- **Complexity**: The vast number of configuration options can be overwhelming for casual users.

## When to use it
- When you want a single, polished UI for all your AI models.
- When privacy and data ownership are top priorities.
- When building a shared AI platform for a team or organization.

## When not to use it
- If you prefer a turnkey, zero-configuration SaaS experience.
- If you only use a single AI provider and don't mind their native interface.

## Getting started
1. Clone the repository: `git clone https://github.com/danny-avila/LibreChat.git`.
2. Create a `.env` file from the provided `example.env` and add your API keys.
3. (Optional) Customize `librechat.yaml` to configure specific endpoints, models, and MCP servers.
4. Run the stack: `docker compose up -d`.
5. Access the UI at `http://localhost:3080`.

## CLI examples
LibreChat is primarily managed via Docker Compose and environment variables, but it includes utility commands for maintenance.

```bash
# Update the LibreChat stack to the latest version
docker compose pull && docker compose up -d

# Check logs for the server container
docker compose logs -f api

# Execute a command inside the running API container to clear cache
docker compose exec api npm run clear-cache
```

## API examples
LibreChat provides a REST API for management and can also act as a proxy. Configuration is handled via `librechat.yaml`.

```yaml
# Example configuration for a custom OpenAI-compatible endpoint in librechat.yaml
endpoints:
  custom:
    - name: "Local Inference"
      apiKey: "${LOCAL_API_KEY}"
      baseURL: "http://host.docker.internal:11434/v1"
      models:
        default: ["llama3", "mistral"]
        fetch: true
```

## Related tools / concepts
- [Open WebUI](../../services/open-webui.md)
- [AnythingLLM](../ai_knowledge/anythingllm.md)
- [Ollama](../../services/ollama.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [TypingMind](typingmind.md)
- [LobeHub](lobehub.md)
- [Jan.ai](../infrastructure/jan-ai.md)

## Sources / references
- [Official Website](https://www.librechat.ai/)
- [GitHub Repository](https://github.com/danny-avila/LibreChat)
- [LibreChat Configuration Guide](https://www.librechat.ai/docs/configuration/librechat_yaml)

## Contribution Metadata
- Last reviewed: 2026-06-01
- Confidence: high
