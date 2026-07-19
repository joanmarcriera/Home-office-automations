# Sourcegraph Cody

## What it is
Cody is an AI coding assistant developed by Sourcegraph that leverages a comprehensive 'Code Graph' to provide deep, context-aware assistance across entire repositories. As of July 2026 (Cody v6.8.x+), it has transitioned into an agentic 'Code Intelligence' platform, capable of multi-repository reasoning, autonomous context retrieval via Model Context Protocol (MCP 3.0/3.1), and native integration with frontier models like Claude 5.1, GPT-5.5, Llama 4, and Gemini 3.5 Pro.

## What problem it solves
It solves the 'context fragmentation' problem in AI-assisted development. While standard tools only see currently active editor files or simple local directories, Cody's integration with Sourcegraph's global index allows it to understand complex dependencies, architectural patterns, and internal APIs across millions of lines of code. It acts as a bridge between the model's general knowledge and the specific, often undocumented, realities of massive, multi-tenant enterprise codebases.

## Where it fits in the stack
**Code Intelligence / Context Layer**. Cody sits between the developer's IDE (VS Code, JetBrains, Windsurf, or Cursor) and the organization's remote code hosts (GitHub, GitLab, Bitbucket). It provides a unified 'Semantic Knowledge Base' that feeds high-fidelity context to autonomous developer agents and local IDE reasoning loops.

## Typical use cases
- **Multi-Repo Search and Refactor**: Asking questions or performing edits that span multiple interconnected microservices and tracking dependency cascades.
- **Agentic Context Fetching**: Using Cody as an MCP server backend for other agentic tools (e.g., Cline, OpenHands) to retrieve relevant code segments dynamically.
- **Onboarding and Exploration**: Quickly understanding data flow through a massive legacy monolith using natural language queries.
- **Automated PR Review and Validation**: Grounding AI pull request reviews in project-specific standards, internal APIs, and existing patterns rather than generic rules.

## Strengths
- **Global Codebase Awareness**: Unrivaled context retrieval powered by Sourcegraph's enterprise-grade indexing, hybrid search, and precise code graphs.
- **Model Agnostic and Modular**: Allows developers to switch seamlessly between frontier models (Claude 5.1, GPT-5.5, Gemini 3.5 Pro, or Llama 4 Maverick) based on complexity.
- **Enterprise-Grade Compliance**: Robust support for self-hosting (on-premise Sourcegraph instances) with fine-grained access control, security policies, and zero data-retention guarantees.
- **Native MCP 3.0/3.1 Support**: Acts as both a client that consumes MCP-hosted tools and a powerful MCP context server for external IDE clients.

## Limitations
- **Indexing Dependency**: Achieving maximum intelligence requires a deployed, fully synced Sourcegraph instance, representing significant infrastructure overhead for smaller teams.
- **Configuration Complexity**: Perfect context fetching often requires tuning indexing parameters and managing large-scale enterprise repository mappings.
- **Latency**: Fetching deep code-graph context from remote enterprise instances introduces higher round-trip latency compared to lightweight, local-only vector DBs.

## When to use it
- In large-scale enterprise environments characterized by complex, multi-repository microservice architectures.
- When you need an AI assistant that follows strict, internal coding standards and utilizes internal libraries accurately.
- When leveraging Sourcegraph as your primary code search and intelligence platform across the organization.

## When not to use it
- For small, self-contained, single-repository projects where local-first tools like Codeium or Cursor provide faster setup.
- If you do not have (or plan to deploy) a Sourcegraph instance or an enterprise Cloud subscription.
- For quick, ad-hoc scripting tasks where deep codebase context is not a critical requirement.

## Getting started

### IDE Integration
1. Install the **Cody AI** extension from the VS Code Marketplace or JetBrains Plugin Store.
2. Sign in via **Sourcegraph Cloud** or connect to your organization's **Sourcegraph Enterprise** instance.
3. Open a repository; Cody will automatically leverage the server-side index to provide context.

### Local-Only Mode
Cody also supports a local-only indexing mode for individual developers:
```bash
# Build a local embeddings index in ~/.cody/index
# This provides local codebase awareness without a server.
cody index create --src ./my-project
```

## CLI examples

### Cody CLI (Context Querying)
```bash
# Query your codebase from the terminal
cody chat -m "Where is the retry logic for the S3 intake service?"

# Generate a project summary based on the current context
cody explain --high-level
```

### Authentication and Setup
```bash
# Login to an enterprise instance
cody login --endpoint https://sourcegraph.company.com --token sgp_39b362198fa064_example
```

## API examples

### MCP 3.0/3.1 Client Configuration
Cody can act as an MCP server to provide code intelligence to other agent tools like Cline or Claude Desktop:
```json
{
  "mcpServers": {
    "sourcegraph-cody": {
      "command": "cody-mcp",
      "args": [
        "--endpoint", "https://sourcegraph.company.com",
        "--access-token", "sgp_39b362198fa064_example",
        "--enable-telemetry", "true"
      ]
    }
  }
}
```

### .cody/ignore (Context Management)
Exclude specific paths from Cody's context indexing directly in your repository:
```text
# .cody/ignore
# Exclude large binary data and legacy logs
data/bin/
logs/legacy/

# Exclude sensitive configuration templates
config/*.template.yml

# Exclude generated artifacts
dist/
build/
```

## Related tools / concepts
- [Sourcegraph](https://sourcegraph.com) (Enterprise Index)
- [Codeium](./codeium.md)
- [Cursor](./cursor.md)
- [OpenHands](./openhands.md)
- [Aider](./aider.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Filesystem Context](../../knowledge_base/patterns/filesystem-context.md)
- [RAG Pattern](../../knowledge_base/patterns/rag.md)
- [CodeGraphContext](../automation_orchestration/codegraphcontext.md)

## Sources / references
- [Cody Official Site](https://about.sourcegraph.com/cody)
- [Cody Documentation (Sourcegraph)](https://sourcegraph.com/docs/cody)
- [Sourcegraph Cody GitHub](https://github.com/sourcegraph/cody)
- [Sourcegraph Cody Roadmap: Agentic Intelligence](https://about.sourcegraph.com/blog/cody-roadmap-agentic)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
