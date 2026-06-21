# Curiosity

## What it is
Curiosity is a desktop-first AI search application and knowledge assistant that provides a unified interface for searching across local files, emails, and cloud storage. As of June 2026, it has expanded into the **Curiosity Workspace** platform, offering enhanced enterprise features, SSO support (OIDC/SAML), and deep integration with local LLMs (via Ollama) and multi-model vector indexing.
- **Licensing**: Proprietary (Freemium)
- **Cost**: Free (Personal) / Paid (Pro & Workspace)
- **Self-hostable**: Desktop app (Local data) / Workspace (On-premise option)

## What problem it solves
It solves the problem of "information fragmentation" where data is scattered across multiple SaaS apps (Slack, Jira, Notion) and local folders. Curiosity provides a single "source of truth" for search, combined with an AI assistant that reasons over indexed data locally, ensuring privacy and reducing the need to upload sensitive files to public clouds.

## Where it fits in the stack
**Enterprise AI / Personal Productivity / Desktop Search**. It acts as a human-facing "Agentic Interface" that bridges the gap between local files and cloud-based knowledge.

## Typical use cases
- **Unified Global Search**: Finding a specific email attachment, Slack thread, or Jira ticket using a single global keyboard shortcut.
- **Private Local RAG**: Asking questions about your local PDF library or code documentation using a local model via [Ollama](../../services/ollama.md).
- **Workspace Collaboration**: Grouping related files, notes, and emails into "Spaces" that can be shared across a team with centralized SSO.
- **Agentic Automation**: Utilizing AI agents that can retrieve information, summarize threads, and even "ask" the user for clarification mid-task.

## Strengths
- **Privacy-First Architecture**: Most indexing and AI processing (with local LLMs) occur on the user's machine.
- **Native Desktop Experience**: High-performance, keyboard-driven interface with instant "Launcher" access.
- **Extensive Connectors**: Supports 50+ cloud and local sources including Microsoft 365, Google Workspace, GitHub, and Notion.
- **June 2026 Features**: **LLM Usage Dashboard** (cost/token tracking), **Multi-Model Vector Indexing** (run embedding models side-by-side), and **Agentic Questioning** (human-in-the-loop support).
- **Advanced Filtering**: Robust inline filters (e.g., `@file`, `ext:`, `src:`) for precision search.

## Limitations
- **Closed Source**: The core application and Workspace server are proprietary.
- **Resource Intensity**: Indexing large datasets and running local LLMs can significantly impact system CPU and RAM.
- **Desktop Focus**: While a web version exists for Workspace, the primary power and local indexing require the desktop agent.

## When to use it
- If you value privacy and want to search local files alongside cloud data without centralized storage.
- If you find yourself constantly switching between browser tabs and local folders to find project info.
- If you want a desktop-native AI assistant that "knows" your work history across multiple apps.

## When not to use it
- If you strictly require 100% open-source software (consider [Khoj](../intake_storage/khoj.md)).
- If you prefer a pure web-based experience and do not want to install a local agent.
- For high-performance, cluster-wide enterprise search where a dedicated engine like [Elasticsearch](elastic.md) is required.

## Getting started

### Installation
Download the installer for your platform from [curiosity.ai](https://curiosity.ai/).
- **macOS**: DMG or Homebrew Cask.
- **Windows**: MSI/EXE.
- **Linux**: AppImage, DEB, or RPM.

### Connecting Local LLM (Ollama)
1. Ensure [Ollama](../../services/ollama.md) is running on your machine.
2. In Curiosity, navigate to **Settings > AI Assistant**.
3. Select **Local LLM (Ollama)** as the provider.
4. Choose your preferred model (e.g., `llama3.1:8b`) and click **Connect**.

## CLI & Keyboard Shortcuts
Curiosity is primarily GUI-driven but emphasizes "keyboard-first" efficiency.

```text
# Launcher Shortcuts
Alt + Space (Win/Linux) or Cmd + Space (Mac): Toggle Global Search Launcher.

# App Shortcuts
Cmd + K: Open Command Palette.
/ : Start a command or search filter (e.g., /type:pdf).

# Inline Filter Examples
@slack "Project Alpha"  # Search only in Slack
src:github ext:py       # Search Python files in GitHub
modified:today          # Find items changed today
```

## API examples
Curiosity Workspace provides an API for automating data ingestion and triggering AI tasks.

```bash
# Trigger an AI summarization task via Workspace API
curl -X POST "https://your-workspace.curiosity.ai/api/v1/tasks/summarize" \
     -H "Authorization: Bearer <API_TOKEN>" \
     -d '{
       "node_id": "slack-thread-12345",
       "prompt_template": "Executive Summary"
     }'
```

## Related tools / concepts
- [AnythingLLM](../ai_knowledge/anythingllm.md) — For flexible local RAG management.
- [Khoj](../intake_storage/khoj.md) — Open-source personal AI search.
- [Msty](../infrastructure/msty.md) — Desktop-native local LLM interface.
- [Ollama](../../services/ollama.md) — Primary local model provider for Curiosity.
- [Elasticsearch](elastic.md) — For large-scale enterprise search infrastructure.
- [Authentik](../../services/authentik.md) — For OIDC/SAML integration with Curiosity Workspace.
- [MCP Registry](../../architecture/multi_agent_knowledgeops.md) — For extending agentic context.

## Sources / References
- [Curiosity.ai Official Site](https://curiosity.ai/)
- [Curiosity Documentation](https://docs.curiosity.ai/)
- [Curiosity Blog: June 2026 Release Overview](https://blog.curiosity.ai/blog/release-overview-june-2026)
- [Curiosity Platform Release Notes](https://knowledge.curiositysoftware.ie/docs/curiosity-platform-release-notes)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
