# Starred AI / Agent Repositories Over 10K Stars

## What it is
This page summarizes the AI and agent-related repositories from your GitHub stars that currently have more than 10,000 GitHub stars. It is meant to answer a practical question: what does each repo actually add to a stack, when should it be used, and which ones are baseline additions versus situational choices in the era of **Claude 4.8** and **GPT-5.5**.

Star counts below are from a GitHub API snapshot pulled on **2026-06-11** from your starred repositories. "Reputation" is an editorial assessment based on maintainer track record, institutional backing, and ecosystem trust.

## What problem it solves
- **Library Overload**: Helps navigate the "sea of stars" by filtering for high-momentum, high-reputation projects.
- **Integration Friction**: Identifies which tools are "baselines" (always use) vs "situational" (only use for specific tasks).
- **Stack Optimization**: Suggests bundles (e.g., Claude-centric, Local-first) to simplify architectural decisions for **Llama 4 Maverick** era workflows.

## Where it fits in the stack
**Landscape Intelligence**. This is a meta-documentation layer that governs tool selection for all other layers (Infrastructure, Development, Services, and Agents).

## Typical use cases
- **Architecting a New Agent**: Deciding whether to use a visual builder like Flowise or a code-first framework like OpenCode.
- **Benchmarking Tools**: Comparing star counts and reputation to assess the long-term viability of a dependency.
- **Skill Expansion**: Identifying high-quality first-party resources (like Anthropic Cookbooks) to improve agent performance.

## Strengths
- **Curated and Prioritized**: Focuses only on high-momentum projects (>10K stars).
- **Practical "Default Stance"**: Provides an immediate "Yes/No/Situational" recommendation for every tool.
- **Ecosystem Awareness**: Highlights combinations and bundles that work well together.

## Limitations
- **Snapshot-based**: Star counts and "reputation" change over time; requires periodic refreshes.
- **Subjective Assessment**: "Reputation" is an editorial assessment, not a purely objective metric.
- **High-Bar Filter**: May miss smaller, high-quality projects that haven't hit the 10K mark yet.

## When to use it
- When **planning a new project** or refactoring an existing agent stack.
- To **onboard new developers/agents** to the preferred repository patterns of this homelab.
- During **quarterly stack reviews** to ensure dependencies are still industry-standard.

## When not to use it
- For **highly niche tasks** where the best tool might be a 100-star specialist repo.
- When searching for **bleeding-edge research** that hasn't gained mass adoption yet.

## Quick take
- **Default baseline for Claude/coding-agent work**: [anthropics/skills](https://github.com/anthropics/skills), [obra/superpowers](https://github.com/obra/superpowers), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks), [Context7](../tools/development_ops/context7.md), [Aider](../tools/development_ops/aider.md)
- **Usually used in combination with other tools**: [browser-use/browser-use](https://github.com/browser-use/browser-use), [mem0](../tools/agents/mem0.md), [openai/whisper](https://github.com/openai/whisper), [google/langextract](https://github.com/google/langextract), [googleworkspace/cli](https://github.com/googleworkspace/cli), [llmfit](../tools/development_ops/llmfit.md), [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router), [farion1231/cc-switch](https://github.com/farion1231/cc-switch)
- **Useful expansions for company systems**: [AnythingLLM](../tools/ai_knowledge/anythingllm.md), [OpenBB](../tools/ai_knowledge/openbb.md), [ClawRouter](../tools/infrastructure/clawrouter.md), [LiteLLM](../services/litellm.md), [OpenRouter](../tools/ai_knowledge/openrouter.md)
- **Strong but situational primary stacks**: [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT), [anomalyco/opencode](https://github.com/anomalyco/opencode), [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise), [LocalAI](../tools/infrastructure/localai.md), [DeerFlow](../tools/agents/deerflow.md), [Fosowl/agenticSeek](https://github.com/Fosowl/agenticSeek), [stitionai/devika](https://github.com/stitionai/devika), [plandex-ai/plandex](https://github.com/plandex-ai/plandex)

## Decision table

| Repo | Stars | Reputation | Core value | Use when | Default stance | Best combinations |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | 198,452 | Category-defining; high name recognition, high complexity | Popularized autonomous-agent loops and agent-platform thinking | You want a broad autonomous-agent platform | Situational | Pair with [mem0](https://github.com/mem0ai/mem0) and [browser-use](https://github.com/browser-use/browser-use) |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | 148,146 | Dominant breakout OSS coding-agent project | Full coding-agent runtime with modern CLI workflow | You want a serious open coding-agent environment | Situational primary stack | Pair with [upstash/context7](https://github.com/upstash/context7), [anthropics/skills](https://github.com/anthropics/skills), and [browser-use](https://github.com/browser-use/browser-use) |
| [openai/whisper](https://github.com/openai/whisper) | 105,946 | Gold standard for STT | Speech-to-text layer for voice, meetings, and media | Your agent/app needs audio input or transcription | Pair with others | Pair with [n8n](../services/whisper.md), [browser-use](https://github.com/browser-use/browser-use), or content pipelines |
| [anthropics/skills](https://github.com/anthropics/skills) | 98,449 | First-party canonical reference | Reusable skill format and examples for Claude workflows | You are using Claude Code or Claude-based agents | Always consider for Claude stacks | Pair with [obra/superpowers](https://github.com/obra/superpowers), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks), and [upstash/context7](https://github.com/upstash/context7) |
| [obra/superpowers](https://github.com/obra/superpowers) | 92,255 | High-signal with major ecosystem adoption | Planning, TDD, and review process for coding agents | You want higher-quality agent output instead of raw speed | Always consider for coding agents | Pair with [anthropics/skills](https://github.com/anthropics/skills), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks), and your preferred coding agent |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 88,774 | Established agent-browser tool | Makes websites operable by agents when APIs are missing | The workflow depends on real browser interaction | Pair with others | Pair with [Playwright](../tools/development_ops/playwright.md), [Tavily](../tools/providers/tavily.md), and [mem0](https://github.com/mem0ai/mem0) |
| [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) | 58,749 | Leading visual LLM orchestrator | Visual builder for agents, RAG, and workflows | You want a visual control plane rather than a pure-code framework | Situational primary stack | Pair with [LocalAI](https://github.com/mudler/LocalAI), [Supabase](../tools/infrastructure/supabase.md), or [n8n](../services/n8n.md) |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 56,821 | Focused memory layer startup | Durable memory layer for agents | Your agents need persistent user/task/project memory | Pair with others | Pair with [browser-use](https://github.com/browser-use/browser-use), [deer-flow](https://github.com/bytedance/deer-flow), or coding agents |
| [upstash/context7](https://github.com/upstash/context7) | 55,032 | Standard for documentation retrieval | Fresh documentation/context retrieval for LLMs | Agents need current library docs instead of stale model memory | Always consider for coding agents | Pair with [opencode](https://github.com/anomalyco/opencode), [Claude Code](../tools/development_ops/claude-code.md), and [superpowers](https://github.com/obra/superpowers) |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 49,053 | Broad ecosystem discovery | Discovery index for Claude skill packs and workflow resources | You want to survey the skills ecosystem quickly | Pair with others | Pair with [anthropics/skills](https://github.com/anthropics/skills) and [superpowers](https://github.com/obra/superpowers) |
| [mudler/LocalAI](https://github.com/mudler/LocalAI) | 48,605 | Foundational local-AI project | OpenAI-compatible local inference stack | You want local/self-hosted inference with broad compatibility | Situational primary stack | Pair with [llmfit](https://github.com/AlexsJones/llmfit), [Flowise](https://github.com/FlowiseAI/Flowise), and [Supabase](../tools/infrastructure/supabase.md) |
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | 47,446 | Strong community prompt pack | Packaged "AI agency" roster of specialist agents | You want pre-shaped specialist roles for marketing/ops | Situational | Pair with [n8n](../services/n8n.md), [Claude Code](../tools/development_ops/claude-code.md), and your own SOPs |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 42,951 | Essential first-party guide | Concrete implementation examples for building with Claude | You want to build with Claude from examples | Always consider for Claude stacks | Pair with [anthropics/skills](https://github.com/anthropics/skills) and [superpowers](https://github.com/obra/superpowers) |
| [google/langextract](https://github.com/google/langextract) | 39,701 | Trusted extraction layer | Structured extraction with grounding and visualization | You need reliable extraction from unstructured text | Pair with others | Pair with [NotebookLM](../tools/ai_knowledge/notebooklm.md), [Supabase](../tools/infrastructure/supabase.md), or document pipelines |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 38,913 | Minimalist research loop | Research-oriented autonomous iteration loop | You want to study compact research-agent loops | Situational | Pair with [deer-flow](https://github.com/bytedance/deer-flow) ideas or [Tavily](../tools/providers/tavily.md) |
| [wshobson/agents](https://github.com/wshobson/agents) | 36,235 | Multi-agent orchestration | Subagent workflows specifically for Claude Code | You want ready-made multi-agent structure on top of Claude Code | Situational primary stack | Pair with [anthropics/skills](https://github.com/anthropics/skills), [superpowers](https://github.com/obra/superpowers), and [context7](https://github.com/upstash/context7) |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 35,532 | High-end research harness | Super-agent harness with tools, memories, and subagents | You want a modern research/coding harness | Situational primary stack | Pair with [Tavily](../tools/providers/tavily.md), [mem0](https://github.com/mem0ai/mem0), and [browser-use](https://github.com/browser-use/browser-use) |
| [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | 34,028 | Spec-driven development | Meta-prompting and spec-driven development system | You want a lighter alternative to Superpowers-style rigor | Situational | Pair with [anthropics/skills](https://github.com/anthropics/skills) and [context7](https://github.com/upstash/context7) |
| [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router) | 33,650 | Model/provider routing | Provider routing layer specifically for Claude Code | You want to keep Claude Code UX while swapping backends | Pair with others | Pair with [cc-switch](https://github.com/farion1231/cc-switch), [LocalAI](https://github.com/mudler/LocalAI), and [OpenRouter](../tools/ai_knowledge/openrouter.md) |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 32,132 | Multi-agent switchboard | Desktop control plane for switching across multiple coding agents | You actively use multiple coding agents | Pair with others | Pair with [claude-code-router](https://github.com/musistudio/claude-code-router) and [anthropics/skills](https://github.com/anthropics/skills) |
| [Fosowl/agenticSeek](https://github.com/Fosowl/agenticSeek) | 29,504 | Local-first autonomous agent | Fully local autonomous agent positioned as a local Manus system | You want local-only autonomous browsing/coding | Situational primary stack | Pair with [LocalAI](https://github.com/mudler/LocalAI), [llmfit](https://github.com/AlexsJones/llmfit), and [browser-use](https://github.com/browser-use/browser-use) |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | 24,276 | Workspace automation CLI | Single CLI for Workspace automation (Drive, Gmail, Calendar) | Google Workspace is a core operating surface for your business | Always consider for Workspace-heavy ops | Pair with [n8n](../services/n8n.md), [Gemini Canvas](../tools/ai_knowledge/gemini-canvas.md), and agent skills |
| [stitionai/devika](https://github.com/stitionai/devika) | 23,495 | Devin-style product surface | Open-source "agentic software engineer" stack | You want a self-hosted autonomous SWE agent product surface | Situational primary stack | Pair with [context7](https://github.com/upstash/context7) and code-review guardrails |
| [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) | 20,612 | Hardware/model calculator | Hardware fit calculator across many providers and models | You need to know what can run on your machine | Pair with others | Pair with [LocalAI](https://github.com/mudler/LocalAI), [Ollama](../services/ollama.md), or [LM Studio](../tools/ai_knowledge/lm-studio.md) |
| [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | 19,043 | Community playbook | Practical conventions and prompts for using Claude Code | You want field-tested workflow ideas | Pair with others | Pair with [superpowers](https://github.com/obra/superpowers) or [get-shit-done](https://github.com/gsd-build/get-shit-done) |
| [plandex-ai/plandex](https://github.com/plandex-ai/plandex) | 18,078 | Terminal-first coding agent | Open-source coding agent designed for real-world work | You want a terminal-first agent for bigger codebases | Situational primary stack | Pair with [context7](https://github.com/upstash/context7), [browser-use](https://github.com/browser-use/browser-use), and repo-specific planning conventions |

## What I would actually default to
- **If the stack is Claude Code-centric**: start with [anthropics/skills](https://github.com/anthropics/skills), [obra/superpowers](https://github.com/obra/superpowers), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks), and [upstash/context7](https://github.com/upstash/context7).
- **If the stack needs real web interaction**: add [browser-use/browser-use](https://github.com/browser-use/browser-use) and keep it secondary to APIs, not primary.
- **If the stack needs memory**: add [mem0ai/mem0](https://github.com/mem0ai/mem0), but only when the workflow truly spans sessions or users.
- **If the stack must run locally**: start with [mudler/LocalAI](https://github.com/mudler/LocalAI) plus [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) before investing in local-agent orchestration.
- **If the stack is Workspace-heavy**: treat [googleworkspace/cli](https://github.com/googleworkspace/cli) as baseline infrastructure, not an optional helper.

## Example company bundles
- **AI operations baseline**: Claude skills + Superpowers + Context7 + n8n.
- **Research-heavy company**: DeerFlow + Tavily + Browser Use + mem0 + Workspace CLI.
- **Local-first company**: LocalAI + llmfit + Ollama + Flowise for internal tools and prototypes.

## What not to overuse
- Do not default to heavyweight autonomous-agent platforms such as AutoGPT, Devika, AgenticSeek, or DeerFlow unless the task truly needs end-to-end autonomy.
- Do not use browser automation first when a stable API exists.
- Do not add memory systems by default; memory is useful only when persistence beats complexity.
- Do not confuse curated lists and best-practice repos with production architecture. They are accelerators, not substitutes for design.

## Related tools / concepts
- [AI Tool Access Matrix](ai_tool_access_matrix.md) — Real-time availability and status of these tools.
- [Model Routing Guide](model_routing_guide.md) — Deciding which model to use with these repositories.
- [Agentic Workflows](patterns/agentic-workflows.md) — Patterns for operationalizing these repos.
- [Claude Code](../../tools/development_ops/claude-code.md) — A primary consumer of many of these tools.
- [n8n](../../services/n8n.md) — The automation engine often used to bridge these libraries.
- [Skills Index](../../skills.md) — The functional capabilities these repos provide.
- [Architecture Overview](../../ARCHITECTURE.md) — How these tools fit into the global stack.
- [Aider](../../tools/development_ops/aider.md) — Terminal-based AI coding.
- [Zed](../../tools/development_ops/zed.md) — High-performance AI editor.
- [Tabnine](../../tools/development_ops/tabnine.md) — Privacy-first AI completions.

## Sources / references
- [GitHub API snapshot of starred repositories](https://github.com/joanmarcriera?tab=stars)
- [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
- [anomalyco/opencode](https://github.com/anomalyco/opencode)
- [openai/whisper](https://github.com/openai/whisper)
- [anthropics/skills](https://github.com/anthropics/skills)
- [obra/superpowers](https://github.com/obra/superpowers)
- [browser-use/browser-use](https://github.com/browser-use/browser-use)
- [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise)
- [mem0ai/mem0](https://github.com/mem0ai/mem0)
- [upstash/context7](https://github.com/upstash/context7)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [mudler/LocalAI](https://github.com/mudler/LocalAI)
- [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks)
- [google/langextract](https://github.com/google/langextract)
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
- [wshobson/agents](https://github.com/wshobson/agents)
- [bytedance/deer-flow](https://github.com/bytedance/deer-flow)
- [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)
- [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router)
- [farion1231/cc-switch](https://github.com/farion1231/cc-switch)
- [Fosowl/agenticSeek](https://github.com/Fosowl/agenticSeek)
- [googleworkspace/cli](https://github.com/googleworkspace/cli)
- [stitionai/devika](https://github.com/stitionai/devika)
- [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit)
- [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)
- [plandex-ai/plandex](https://github.com/plandex-ai/plandex)

## Contribution Metadata
- Last reviewed: 2026-06-11
- Confidence: high
