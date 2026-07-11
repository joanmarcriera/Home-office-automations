# LibreChat

## What it is
LibreChat is a free, open-source AI conversation platform that provides a unified interface for multiple AI models. As of July 2026, it has matured into a comprehensive "Agentic Data Analytics" platform following its acquisition by ClickHouse, offering multi-agent support, native multimodality, and robust administrative controls.

## What problem it solves
It eliminates the need to switch between multiple chat interfaces for different AI providers and solves the "interface fragmentation" problem for organizations. It provides a self-hosted, privacy-centric alternative to proprietary UIs, now enhanced with native "Agents" that can perform complex data analytics and handle multi-modal files (video, PDF, etc.) locally or via cloud providers.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Self-hosted Chat UI. It serves as the primary "Front-End Operating System" for AI in a homelab or enterprise environment, orchestrating multiple LLM backends and [MCP 3.0](../automation_orchestration/mcp.md) Task Protocol servers.

## Typical use cases
- **Unified AI Hub**: Accessing frontier models (GPT-5, Claude 4.8) and local models like [Gemma 3](local_llms.md) through a single, polished UI.
- **Agentic Data Analytics**: Utilizing the ClickHouse-backed infrastructure to run complex queries and visualizations over large datasets via specialized agents.
- **Multimodal Document Processing**: Using native OCR and video understanding to analyze diverse file types in-situ.
- **Organizational AI Gateway**: Providing secure, SSO-enabled access to AI tools with fine-grained Access Control Lists (ACLs) and an Admin Panel.

## Strengths
- **Native Multi-Agent Framework**: Supports app-agnostic agents that can share prompts and MCP servers between users.
- **Rich Multimodality**: Native handling for video understanding, PDFs, and inline Mermaid diagrams for visualization.
- **Persistence & Personalization**: Features "Resumable Chats" (preserving context through disconnects) and "User Memories" for long-term personalization.
- **Enterprise Ready**: Includes a robust Admin Panel (introduced in Q1 2026), ACLs, and seamless SSO integration.
- **Open Source Transparency**: Remains community-driven with over 35,000 GitHub stars and extensive customization options.

## Limitations
- **Deployment Complexity**: Setting up the full stack (including ClickHouse for advanced analytics) requires significant Docker and networking expertise.
- **Hardware Requirements**: Running the full suite of multimodal agents locally requires substantial GPU and memory resources.

## When to use it
- When you need a professional, single UI for a team or organization to access multiple AI models.
- When your workflow requires multi-agent collaboration and advanced data visualization.
- If you value "User Memories" and "Resumable Chats" for a persistent AI experience.

## When not to use it
- For very simple, single-user local chat where a lightweight app like [Jan.ai](../infrastructure/jan-ai.md) or Ollama CLI would suffice.
- If you prefer a zero-maintenance SaaS experience over a self-hosted platform.

## Getting started
1. **Clone**: `git clone https://github.com/danny-avila/LibreChat.git`.
2. **Environment**: Configure `.env` with your API keys; use `example.env` as a template.
3. **Configuration**: Edit `librechat.yaml` to define your MCP servers, custom endpoints, and ACLs.
4. **Deploy**: Run `docker compose up -d` to start the core services and the analytics engine.
5. **Access**: Navigate to `http://localhost:3080` and use the Admin Panel for initial setup.

## CLI examples
LibreChat is primarily managed via Docker Compose, but includes utility scripts for database maintenance and versioning.

```bash
# Update LibreChat and its dependencies to the latest release
docker compose pull && docker compose up -d

# View logs for the Agents framework to debug MCP connections
docker compose logs -f api

# Clear the global model cache inside the API container
docker compose exec api npm run clear-cache
```

## API examples
LibreChat features an OpenAI-compatible "Agents API" (Beta) for external integrations.

```yaml
# Example configuration for a custom MCP-enabled endpoint in librechat.yaml
endpoints:
  custom:
    - name: "Agentic Analytics"
      apiKey: "${ANALYTICS_API_KEY}"
      baseURL: "http://host.docker.internal:3080/v1"
      models:
        default: ["agents-analytics-v1"]
        fetch: true
      mcpServers:
        - name: "clickhouse-mcp"
          url: "http://clickhouse-server:8000"
```

## Related tools / concepts
- [Open WebUI](../../services/open-webui.md) — Main open-source competitor.
- [AnythingLLM](../ai_knowledge/anythingllm.md) — Focused on local RAG and desktop use.
- [Ollama](../../services/ollama.md) — Preferred local inference backend.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Core standard for LibreChat tool integration.
- [LobeHub](lobehub.md) — High-performance AI interface alternative.
- [Jan.ai](../infrastructure/jan-ai.md) — Local-first desktop alternative.
- [Dify](dify.md) — Alternative for building complex agentic workflows.

## Sources / references
- [LibreChat Official Site](https://www.librechat.ai/)
- [LibreChat 2026 Roadmap](https://www.librechat.ai/blog/2026-02-18_2026_roadmap)
- [LibreChat Documentation: Configuration Guide](https://www.librechat.ai/docs/configuration/librechat_yaml)

## Contribution Metadata
- Last reviewed: 2026-07-11
- Confidence: high
