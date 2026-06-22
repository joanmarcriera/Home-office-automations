# Sourcegraph Cody

## What it is
Cody is an AI coding assistant developed by Sourcegraph that leverages a comprehensive 'Code Graph' to provide deep, context-aware assistance across entire repositories. As of June 2026 (Cody v6.x), it has transitioned into an agentic 'Code Intelligence' platform, capable of multi-repository reasoning, autonomous context retrieval via MCP 3.0, and native integration with frontier models like Claude 4.8 and GPT-5.5.

## What problem it solves
It solves the 'context fragmentation' problem in AI development. While many tools only see open files, Cody's integration with Sourcegraph's global index allows it to understand complex dependencies, architectural patterns, and internal APIs across millions of lines of code. It acts as a bridge between the model's general knowledge and the specific, often undocumented, realities of a private codebase.

## Where it fits in the stack
**Code Intelligence / Context Layer**. Cody sits between the developer's IDE (VS Code, JetBrains) and the organization's code hosts (GitHub, GitLab). It provides a unified 'Semantic Knowledge Base' that feeds high-fidelity context to agentic reasoning loops.

## Typical use cases
- **Multi-Repo Search and Refactor**: Asking questions or performing edits that span multiple interconnected services.
- **Agentic Context Fetching**: Using Cody as a backend for other agentic tools (e.g., Cline, OpenHands) to retrieve relevant code segments.
- **Onboarding and Exploration**: Quickly understanding the flow of data through a massive, legacy monolith using natural language.
- **Automated PR Review**: Grounding AI reviews in project-specific standards and existing patterns rather than generic best practices.

## Strengths
- **Global Codebase Awareness**: Unrivaled context retrieval powered by Sourcegraph's enterprise-grade indexing and search.
- **Model Agnostic**: Allows users to switch between frontier models (Claude 4.8, GPT-5.5, Gemini 1.5 Pro) based on the task's complexity.
- **Enterprise-Ready**: Robust support for self-hosting (Sourcegraph instance) and complex access control/compliance requirements.
- **Native MCP 3.0 Support**: Can serve as a 'Context Provider' for any agentic tool that speaks the Model Context Protocol.

## Limitations
- **Indexing Dependency**: Full power requires a Sourcegraph instance, which can be a significant infrastructure undertaking for small teams.
- **Configuration Complexity**: Getting 'perfect' context often requires fine-tuning indexing settings and managing large-scale enterprise permissions.
- **Latency**: Deep context fetching from remote Sourcegraph instances can introduce more latency than local-only indexing solutions.

## When to use it
- In large-scale enterprise environments with complex, multi-repository architectures.
- When you need an AI assistant that follows strict, internal coding standards and utilizes internal libraries accurately.
- When leveraging Sourcegraph as your primary code search and intelligence platform.

## When not to use it
- For small, self-contained projects where local-first tools like Codeium or Cursor provide faster setup.
- If you do not have (or plan to have) a Sourcegraph instance or an enterprise Cloud subscription.
- For quick, ad-hoc scripts where deep codebase context is not a requirement.

## Getting started

### IDE Integration
1. Install the **Cody AI** extension from the VS Code Marketplace or JetBrains Plugin Store.
2. Sign in via **Sourcegraph Cloud** or connect to your organization's **Sourcegraph Enterprise** instance.
3. Open a repository; Cody will automatically leverage the server-side index to provide context.

### Local-Only Mode
Cody also supports a local-only indexing mode for individual developers:
```bash
# Cody will build a local embeddings index in ~/.cody/index
# This provides a 'Lite' version of codebase awareness without a server.
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
cody login --endpoint https://sourcegraph.company.com --token <YOUR_TOKEN>
```

## API examples

### MCP 3.0 Context Provider
Cody can be used as an MCP server to provide context to other agents:
```json
{
  "mcpServers": {
    "sourcegraph-cody": {
      "command": "cody-mcp",
      "args": ["--endpoint", "https://sourcegraph.com", "--access-token", "sgp_xxx"]
    }
  }
}
```

### .cody/ignore (Context Management)
Control exactly what Cody 'sees' in your repository:
```text
# .cody/ignore
# Exclude large binary data and legacy logs
data/bin/
logs/legacy/
# Exclude sensitive configuration templates
config/*.template.yml
```

## Related tools / concepts
- [Sourcegraph](https://sourcegraph.com) (Enterprise Index)
- [Codeium](./codeium.md)
- [Cursor](./cursor.md)
- [OpenHands](./openhands.md)
- [Cline](https://cline.bot)
- [Aider](./aider.md)
- [MCP 3.0](../infrastructure/mcp.md)
- [Agentic Context Retrieval](../../knowledge_base/patterns/agentic-context.md)
- [CodeGraphContext](../automation_orchestration/codegraphcontext.md)

## Sources / references
- [Cody Official Site](https://about.sourcegraph.com/cody)
- [Cody Documentation (Sourcegraph)](https://sourcegraph.com/docs/cody)
- [Sourcegraph Cody GitHub](https://github.com/sourcegraph/cody)
- [June 2026 Roadmap: Agentic Intelligence](https://about.sourcegraph.com/blog/cody-v6-roadmap)

## Contribution Metadata

- Last reviewed: 2026-06-22
- Confidence: high
