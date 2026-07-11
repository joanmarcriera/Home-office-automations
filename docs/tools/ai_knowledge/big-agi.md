# big-AGI

## What it is
big-AGI is a local-first, vendor-neutral multi-model AI workspace designed for professionals (engineers, researchers, and founders). As of July 2026, it focuses on zero-latency interactions, advanced reasoning, and multi-model orchestration, fully supporting [Gemma 3](local_llms.md) and the [MCP 3.0](../automation_orchestration/mcp.md) Task Protocol.

## What problem it solves
It allows users to simultaneously use, compare, and merge outputs from multiple AI models through its unique "Beam" feature. This enables robust decision-making, defeats hallucinations, and prevents vendor lock-in by providing a unified interface for all major LLM providers.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Professional AI Workspace. It acts as a high-performance orchestration layer between users and various [LLM Providers](../providers/index.md), now enhanced with native [MCP 3.0](../automation_orchestration/mcp.md) tool integration.

## Typical use cases
- **Multi-Model Intelligence (Beam)**: Querying several models (e.g., Claude 4.8, GPT-5.5, [Gemma 3](local_llms.md)) simultaneously to find the best response.
- **Deep Research**: Using "Gemini Deep Research" (now fully resumable) and web search with citations for technical validation.
- **Agentic Workflows**: Leveraging "Anthropic Containers" for persistent files, bash sessions, and skills that span multiple turns.
- **Creative Production**: Image generation and editing via Nano Banana and GPT-Image-2.

## Key Features (July 2026 Update)
- **Beam 2**: Multi-modal, program-based reasoning with follow-ups and saveable presets.
- **Anthropic Containers**: 1-hour persistent sandbox for files and code execution (Bash) that maintains state across turns.
- **MCP 3.0 Native Support**: Seamless integration of Model Context Protocol tools for local and remote data access.
- **AIX Resume Framework**: Fully resumable sessions for long-running Deep Research or interrupted generation across providers.
- **Madly Optimized UI**: Terminal-fast performance with advanced code rendering and peeking side panels.

## Strengths
- **Zero Latency**: Local-first architecture that runs almost entirely in the browser for instant response.
- **Universal Connectivity**: Supports 100+ models from 20+ vendors, with auto-detection of features like "Thinking/Reasoning" and "Skills".
- **Human-in-the-Loop**: Designed for experts who need fine-grained control over the reasoning process.
- **Privacy & Security**: Local-first by default; encrypted reasoning supported for xAI/Grok models.

## Limitations
- **High Density**: The interface is optimized for productivity and might be complex for casual users.
- **Advanced-Only**: Features like "Chain of Thought" merging and "Reasoning Effort" control require understanding of modern LLM parameters.

## When to use it
- For high-stakes decisions where cross-model verification is required.
- When you need a persistent code execution environment (Sandbox) within your chat.
- When you want the fastest possible multi-model interface for "vibe coding" or research.

## When not to use it
- For basic, mobile-only casual chat (optimized for power users).
- If you prefer a "black box" experience without control over model parameters or reasoning steps.

## Getting started

### Web Access
1.  Navigate to [app.big-agi.com](https://app.big-agi.com/).
2.  Add your API keys in the **Models** section.
3.  Launch **Beam** to compare the latest frontier models.

### Self-Hosting (Docker)
```bash
docker run -p 3000:3000 ghcr.io/enricoros/big-agi
```

## CLI examples
While primarily a web UI, big-AGI can be managed and deployed via CLI tools.

```bash
# Deploy big-AGI to Vercel for private use
npx vercel --prod

# Pull and run the latest big-AGI Docker image
docker pull ghcr.io/enricoros/big-agi && docker run -p 3000:3000 ghcr.io/enricoros/big-agi

# Run big-AGI locally for development
git clone https://github.com/enricoros/big-AGI.git && cd big-AGI && npm install && npm run dev
```

## API examples
big-AGI exposes certain functionalities via local endpoints when self-hosted.

```bash
# Check the health of a local big-AGI instance
curl http://localhost:3000/api/health

# Trigger a model refresh via the management API (hypothetical)
curl -X POST http://localhost:3000/api/admin/refresh-models -H "Authorization: Bearer $ADMIN_TOKEN"
```

## Related tools / concepts
- [LobeHub](lobehub.md): Another powerful multi-model UI.
- [OpenRouter](openrouter.md): The recommended backend for big-AGI.
- [LiteLLM](../../services/litellm.md): Ideal for managing local model fallbacks.
- [Claude Code](../development_ops/claude-code.md): Complementary CLI-based agentic workflow.
- [PydanticAI](../frameworks/pydantic-ai.md): For building production-grade agents that can integrate with big-AGI.
- [Documentation Writer](../agents/documentation-writer.md): For maintaining the documentation of your big-AGI-based projects.
- [Superpowers](../agents/superpowers.md): Curated skill bundles that can be used within big-AGI via MCP 3.0.

## Sources / references
- [big-AGI Official Site](https://big-agi.com/)
- [big-AGI GitHub](https://github.com/enricoros/big-AGI)
- [big-AGI Changelog](https://big-agi.com/docs/changelog)
- [OpenRouter](https://openrouter.ai/)

## Contribution Metadata
- Last reviewed: 2026-07-11
- Confidence: high
