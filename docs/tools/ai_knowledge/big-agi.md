# big-AGI

## What it is
big-AGI is a local-first, vendor-neutral multi-model AI workspace designed for professionals (engineers, researchers, and founders). It focuses on zero-latency interactions, advanced reasoning, and multi-model orchestration.

## What problem it solves
It allows users to simultaneously use, compare, and merge outputs from multiple AI models through its unique "Beam" feature. This enables robust decision-making, defeats hallucinations, and prevents vendor lock-in.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Professional AI Workspace. It acts as a high-performance orchestration layer between users and various [LLM Providers](../providers/index.md).

## Typical use cases
- **Multi-Model Intelligence (Beam)**: Querying several models (e.g., Claude 4.7, GPT-5.5, Gemini 3.5) simultaneously to find the best response.
- **Deep Research**: Using "Gemini Deep Research" (now fully resumable) and web search with citations for technical validation.
- **Agentic Workflows**: Leveraging "Anthropic Containers" for persistent files, bash sessions, and skills that span multiple turns.
- **Creative Production**: Image generation and editing via Nano Banana and GPT-Image-2.

## Key Features (May 2026 Update)
- **Beam 2**: Multi-modal, program-based reasoning with follow-ups and saveable presets.
- **Anthropic Containers**: 1-hour persistent sandbox for files and code execution (Bash) that maintains state across turns.
- **Gemini Antigravity Support**: Integration with the latest agentic models featuring Linux sandbox support.
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

## Licensing and cost
- **Open Source**: MIT License.
- **Cost**: Free (Community/Open) / Paid (Pro for Cloud Sync and advanced features).
- **Self-hostable**: Yes (Docker, Vercel, or local build).

## Related tools / concepts
- [LobeHub](lobehub.md): Another powerful multi-model UI.
- [OpenRouter](../providers/openrouter.md): The recommended backend for big-AGI.
- [LiteLLM](../../services/litellm.md): Ideal for managing local model fallbacks.
- [Claude Code](../development_ops/claude-code.md): Complementary CLI-based agentic workflow.

## Sources / References
- [big-AGI Official Site](https://big-agi.com/)
- [big-AGI GitHub](https://github.com/enricoros/big-AGI)
- [big-AGI Changelog](https://big-agi.com/docs/changelog)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
