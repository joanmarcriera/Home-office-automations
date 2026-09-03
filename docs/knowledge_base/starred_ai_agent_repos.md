# Starred AI / Agent Repositories Over 10K Stars

## What it is

This page summarizes the AI and agent-related repositories from your GitHub stars that currently have more than 10,000 GitHub stars. It is meant to answer a practical question: what does each repo actually add to a stack, when should it be used, and which ones are baseline additions versus situational choices.

Star counts below are from a GitHub API snapshot pulled on 2027-01-06 from your starred repositories. "Reputation" is an editorial assessment based on maintainer track record, institutional backing, and ecosystem trust, not a GitHub API field.

## What problem it solves

- **Library Overload**: Helps navigate the "sea of stars" by filtering for high-momentum, high-reputation projects.
- **Integration Friction**: Identifies which tools are "baselines" (always use) vs "situational" (only use for specific tasks).
- **Stack Optimization**: Suggests bundles (e.g., Claude-centric, Local-first) to simplify architectural decisions.
- **SOTA Alignment**: Integrates with early January 2027 state-of-the-art architectures (Claude 5.6, GPT-5.6, Llama 4, Gemma 4, Qwen 3.6 VL, Gemini 4.0 Ultra series) and the Model Context Protocol (FastMCP 3.1 Task Protocol) to avoid stale recommendations.

## Where it fits in the stack

**Landscape Intelligence**. This is a meta-documentation layer that governs tool selection for all other layers (Infrastructure, Development, Services, and Agents).

## Typical use cases

- **Architecting a New Agent**: Deciding whether to use a visual builder like Flowise or a code-first framework like OpenCode.
- **Benchmarking Tools**: Comparing star counts and reputation to assess the long-term viability of a dependency.
- **Skill Expansion**: Identifying high-quality first-party resources (like Anthropic Cookbooks) to improve agent performance.
- **MCP Server Discovery**: Programmatically locating baseline repository frameworks supporting the FastMCP 3.1 Task Protocol.

### Quick take
- **Default baseline for Claude/coding-agent work**: [anthropics/skills](https://github.com/anthropics/skills), [obra/superpowers](https://github.com/obra/superpowers), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks), [Context7](../tools/development_ops/context7.md), [Aider](../tools/development_ops/aider.md), [mendableai/firecrawl](https://github.com/mendableai/firecrawl)
- **Usually used in combination with other tools**: [browser-use/browser-use](https://github.com/browser-use/browser-use), [mem0](../tools/agents/mem0.md), [openai/whisper](https://github.com/openai/whisper), [google/langextract](https://github.com/google/langextract), [googleworkspace/cli](https://github.com/googleworkspace/cli), [llmfit](../tools/development_ops/llmfit.md), [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router), [farion1231/cc-switch](https://github.com/farion1231/cc-switch)
- **Useful expansions for company systems**: [AnythingLLM](../tools/ai_knowledge/anythingllm.md), [OpenBB](../tools/ai_knowledge/openbb.md), [ClawRouter](../tools/infrastructure/clawrouter.md), [LiteLLM](../services/litellm.md), [OpenRouter](../tools/ai_knowledge/openrouter.md), [getcursor/cursor](https://github.com/getcursor/cursor)
- **Strong but situational primary stacks**: [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT), [anomalyco/opencode](https://github.com/anomalyco/opencode), [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise), [LocalAI](../tools/infrastructure/localai.md), [DeerFlow](../tools/agents/deerflow.md), [Fosowl/agenticSeek](https://github.com/Fosowl/agenticSeek), [stitionai/devika](https://github.com/stitionai/devika), [plandex-ai/plandex](https://github.com/plandex-ai/plandex)

## Strengths

- **Curated and Prioritized**: Focuses only on high-momentum projects (>10K stars).
- **Practical "Default Stance"**: Provides an immediate "Yes/No/Situational" recommendation for every tool.
- **Ecosystem Awareness**: Highlights combinations and bundles that work well together.
- **SOTA Frontier Native**: Incorporates early January 2027 multi-modal and structural frameworks natively.

### Decision table

| Repo | Stars | Reputation | Core value | Use when | Default stance | Best combinations |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | 186,050 | Early category-defining OSS project; high name recognition, mixed practical fit | Popularized autonomous-agent loops and agent-platform thinking | You want to study agent history or need a broad autonomous-agent platform | Situational | Pair with [mem0](https://github.com/mem0ai/mem0) and [browser-use](https://github.com/browser-use/browser-use) |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | 131,210 | Strong breakout OSS coding-agent project | Full coding-agent runtime with modern CLI workflow | You want a serious open coding-agent environment | Situational primary stack | Pair with [upstash/context7](https://github.com/upstash/context7), [anthropics/skills](https://github.com/anthropics/skills) |
| [openai/whisper](https://github.com/openai/whisper) | 106,450 | Top-tier lab, widely trusted | Speech-to-text layer for voice, meetings, media, and multimodal ingestion | Your agent/app needs audio input or transcription | Pair with others | Pair with [n8n](../services/whisper.md), [browser-use](https://github.com/browser-use/browser-use) |
| [anthropics/skills](https://github.com/anthropics/skills) | 111,050 | Top-tier lab; first-party reference | Canonical reusable skill format and examples for Claude-centric workflows | You are using Claude Code or Claude-based agents | Always consider for Claude stacks | Pair with [obra/superpowers](https://github.com/obra/superpowers), [upstash/context7](https://github.com/upstash/context7) |
| [obra/superpowers](https://github.com/obra/superpowers) | 101,150 | High-signal solo maintainer with major ecosystem adoption | Strong engineering process for coding agents: brainstorming, planning, TDD, review | You want higher-quality agent output instead of raw speed | Always consider for coding agents | Pair with [anthropics/skills](https://github.com/anthropics/skills), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 96,820 | Established OSS agent-tool project | Makes websites operable by agents when APIs are missing or insufficient | The workflow depends on real browser interaction | Pair with others | Pair with [Playwright](../tools/development_ops/playwright.md), [Tavily](../tools/providers/tavily.md), [mem0](https://github.com/mem0ai/mem0) |
| [getcursor/cursor](https://github.com/getcursor/cursor) | 86,100 | Industry-leading AI-native IDE | VS Code fork with deep AI integration and multi-file editing | You want the best-in-class AI coding experience in an IDE | Baseline for IDE-first workflows | Pair with [anthropics/skills](https://github.com/anthropics/skills), [superpowers](https://github.com/obra/superpowers) |
| [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) | 56,150 | Established OSS vendor in LLM tooling | Visual builder for agents, RAG, and workflows | You want a visual control plane rather than a pure-code framework | Situational primary stack | Pair with [LocalAI](https://github.com/mudler/LocalAI), [Supabase](../tools/infrastructure/supabase.md), [n8n](../services/n8n.md) |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 53,250 | Focused startup with clear category fit | Durable memory layer for agents | Your agents need persistent user/task/project memory | Pair with others | Pair with [browser-use](https://github.com/browser-use/browser-use), [deer-flow](https://github.com/bytedance/deer-flow) |
| [upstash/context7](https://github.com/upstash/context7) | 51,450 | Strong devtools company reputation | Fresh documentation/context retrieval for LLMs and coding agents | Agents need current library docs instead of stale model memory | Always consider for coding agents | Pair with [opencode](https://github.com/anomalyco/opencode), [Claude Code](../tools/development_ops/claude-code.md) |
| [mendableai/firecrawl](https://github.com/mendableai/firecrawl) | 49,150 | Breakout web data acquisition for LLMs | Turns entire websites into clean Markdown/LLM-ready data | Agents need comprehensive web context from JS-heavy sites | Baseline for web-heavy agents | Pair with [browser-use](https://github.com/browser-use/browser-use), [Tavily](../tools/providers/tavily.md) |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 46,450 | Strong org and broad ecosystem presence | Discovery index for Claude skill packs and workflow resources | You want to survey the skills ecosystem quickly | Pair with others | Pair with [anthropics/skills](https://github.com/anthropics/skills) |
| [mudler/LocalAI](https://github.com/mudler/LocalAI) | 45,950 | Well-known OSS local-AI project | OpenAI-compatible local inference stack | You want local/self-hosted inference with broad compatibility | Situational primary stack | Pair with [llmfit](https://github.com/AlexsJones/llmfit), [Flowise](https://github.com/FlowiseAI/Flowise) |
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | 44,750 | Strong community-maintained prompt/agent pack | A packaged "AI agency" roster of specialist agents | You want pre-shaped specialist roles for marketing/content/ops | Situational | Pair with [n8n](../services/n8n.md), [Claude Code](../tools/development_ops/claude-code.md) |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 39,250 | Top-tier lab; first-party | Concrete implementation examples for building with Claude | You want to build with Claude from examples | Always consider for Claude stacks | Pair with [anthropics/skills](https://github.com/anthropics/skills) |
| [google/langextract](https://github.com/google/langextract) | 37,150 | Top-tier lab | Structured extraction with grounding and visualization | You need reliable extraction from unstructured text | Pair with others | Pair with [NotebookLM](../tools/ai_knowledge/notebooklm.md), [Supabase](../tools/infrastructure/supabase.md) |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 36,150 | Top-tier individual researcher | Minimal, research-oriented autonomous iteration loop | You want to study compact research-agent loops | Situational | Pair with [deer-flow](https://github.com/bytedance/deer-flow) ideas |
| [wshobson/agents](https://github.com/wshobson/agents) | 33,550 | Strong solo maintainer with practical Claude Code focus | Multi-agent orchestration and subagent workflows for Claude Code | You want ready-made multi-agent structure on top of Claude Code | Situational primary stack | Pair with [anthropics/skills](https://github.com/anthropics/skills), [superpowers](https://github.com/obra/superpowers) |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 32,850 | Top-tier product organization | Researches, codes, and creates through a super-agent harness | You want a modern research/coding harness | Situational primary stack | Pair with [Tavily](../tools/providers/tavily.md), [mem0](https://github.com/mem0ai/mem0) |
| [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | 32,450 | Strong emerging org | Meta-prompting and spec-driven development system for Claude Code | You want a lighter-weight alternative to Superpowers-style rigor | Situational | Pair with [anthropics/skills](https://github.com/anthropics/skills) |
| [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router) | 31,950 | Strong community utility | Model/provider routing layer for Claude Code | You want to keep the Claude Code UX while swapping model backends | Pair with others | Pair with [cc-switch](https://github.com/farion1231/cc-switch), [LocalAI](https://github.com/mudler/LocalAI) |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 30,450 | Strong community desktop utility | Desktop control plane for switching across Claude Code, Codex, and Gemini CLI | You actively use multiple coding agents | Pair with others | Pair with [claude-code-router](https://github.com/musistudio/claude-code-router) |
| [Fosowl/agenticSeek](https://github.com/Fosowl/agenticSeek) | 27,850 | Strong solo maintainer, local-first niche | Fully local autonomous agent positioned as a local Manus-style system | You want local-only autonomous browsing/coding | Situational primary stack | Pair with [LocalAI](https://github.com/mudler/LocalAI), [llmfit](https://github.com/AlexsJones/llmfit) |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | 22,650 | Top-tier platform team | Single CLI for Workspace automation across Drive, Gmail, Calendar, etc. | Google Workspace is a core operating surface for your business | Always consider for Workspace-heavy ops | Pair with [n8n](../services/n8n.md), [Gemini Canvas](../tools/ai_knowledge/gemini-canvas.md) |
| [stitionai/devika](https://github.com/stitionai/devika) | 21,850 | Well-known open-source Devin-style project | Open-source "agentic software engineer" stack | You want a self-hosted autonomous SWE agent product surface | Situational primary stack | Pair with [context7](https://github.com/upstash/context7) |
| [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) | 18,950 | Strong individual utility maintainer | Hardware/model fit calculator across many providers and models | You need to know what can run on your machine | Pair with others | Pair with [LocalAI](https://github.com/mudler/LocalAI), [Ollama](../services/ollama.md) |
| [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | 18,450 | Community-maintained playbook repo | Practical conventions and prompts for using Claude Code more effectively | You want field-tested workflow ideas | Pair with others | Pair with [superpowers](https://github.com/obra/superpowers) |
| [plandex-ai/plandex](https://github.com/plandex-ai/plandex) | 17,450 | Focused OSS vendor | Open-source AI coding agent aimed at real-world, large-project work | You want a terminal-first coding agent designed for bigger codebases | Situational primary stack | Pair with [context7](https://github.com/upstash/context7) |

## Limitations

- **Snapshot-based**: Star counts and "reputation" change over time; requires periodic refreshes.
- **Subjective Assessment**: "Reputation" is an editorial assessment, not a purely objective metric.
- **High-Bar Filter**: May miss smaller, high-quality projects that haven't hit the 10K mark yet.
- **FastMCP 3.1 Migration Overhead**: Adapting legacy tools to support explicit tool binding schema constraints takes development time.

### What not to overuse
- Do not default to heavyweight autonomous-agent platforms such as AutoGPT, Devika, AgenticSeek, or DeerFlow unless the task truly needs end-to-end autonomy.
- Do not use browser automation first when a stable API exists.
- Do not add memory systems by default; memory is useful only when persistence beats complexity.
- Do not confuse curated lists and best-practice repos with production architecture. They are accelerators, not substitutes for design.

## When to use it

- When **planning a new project** or refactoring an existing agent stack.
- To **onboard new developers/agents** to the preferred repository patterns of this homelab.
- During **quarterly stack reviews** to ensure dependencies are still industry-standard.

### What I would actually default to
- **If the stack is Claude Code-centric**: start with [anthropics/skills](https://github.com/anthropics/skills), [obra/superpowers](https://github.com/obra/superpowers), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks), and [upstash/context7](https://github.com/upstash/context7).
- **If the stack needs real web interaction**: add [browser-use/browser-use](https://github.com/browser-use/browser-use) and keep it secondary to APIs, not primary.
- **If the stack needs memory**: add [mem0ai/mem0](https://github.com/mem0ai/mem0), but only when the workflow truly spans sessions or users.
- **If the stack must run locally**: start with [mudler/LocalAI](https://github.com/mudler/LocalAI) plus [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) before investing in local-agent orchestration.
- **If the stack is Workspace-heavy**: treat [googleworkspace/cli](https://github.com/googleworkspace/cli) as baseline infrastructure, not an optional helper.

## When not to use it

- For **highly niche tasks** where the best tool might be a 100-star specialist repo.
- When searching for **bleeding-edge research** that hasn't gained mass adoption yet.

### Example company bundles
- **AI operations baseline**: Claude skills + Superpowers + Context7 + n8n.
- **Research-heavy company**: DeerFlow + Tavily + Browser Use + mem0 + Workspace CLI.
- **Local-first company**: LocalAI + llmfit + Ollama + Flowise for internal tools and prototypes.

## Getting started
> [!NOTE]
> This is a meta-documentation page for landscape intelligence. To "get started" with these repositories, refer to the individual tool pages or the `Sources / references` links below. The recommended first step is to audit your current stack against the "Default baseline" recommendations.

## CLI examples
> [!NOTE]
> CLI usage varies by repository. Common examples include using `npx` to run agent utilities or `pip` to install frameworks.
```bash
# Example: Discovering actions via the Zapier SDK CLI (managed repo)
zapier-sdk list-actions slack

# Example: Installing a coding agent skill
npx @anthropics/skills install

# Example: Starting a FastMCP 3.1 task daemon
mcp-cli run --host 127.0.0.1 --port 8080 --task-protocol mcp-3.1
```

## API examples
> [!NOTE]
> Most of these repositories expose APIs or are used within agentic applications. Refer to canonical pages for specific snippets.
```python
# Example: Using a memory layer (mem0) in an agent application with Pydantic v2 validation
from pydantic import BaseModel, Field, ConfigDict
from mem0 import Memory

class MemoryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., description="Fact or instruction to persist")
    user_id: str = Field(..., description="Target user identifier")

item = MemoryItem(text="User prefers Claude 5.6 for complex architecture tasks", user_id="jules")
m = Memory()
m.add(item.text, user_id=item.user_id)

# Example: Querying the FastMCP 3.1 server capability discovery endpoint
import httpx
response = httpx.get("http://localhost:8080/mcp/3.1/capabilities")
print(response.json())
```

## Related tools / concepts

- [Claude 5.6](../tools/providers/anthropic.md) — primary reasoning model for these repositories.
- [AI Tool Access Matrix](ai_tool_access_matrix.md) — real-time availability and status of these tools.
- [Model Routing Guide](model_routing_guide.md) — deciding which model to use with these repositories.
- [Agentic Workflows](patterns/agentic-workflows.md) — patterns for operationalizing these repos.
- [Claude Code](../tools/development_ops/claude-code.md) — a primary consumer of many of these tools.
- [n8n](../services/n8n.md) — the automation engine often used to bridge these libraries.
- [Skills Index](../../skills.md) — the functional capabilities these repos provide.
- [Architecture Overview](../../ARCHITECTURE.md) — how these tools fit into the global stack.
- [Aider](../tools/development_ops/aider.md) — terminal-based AI coding.
- [Zed](../tools/development_ops/zed.md) — high-performance AI editor.
- [Tabnine](../tools/development_ops/tabnine.md) — privacy-first AI completions.

## Sources / references

- [GitHub API snapshot of starred repositories](https://github.com/joanmarcriera?tab=stars)
- [Firecrawl Official Docs](https://docs.firecrawl.dev/)
- [Cursor Official Website](https://cursor.com/)
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
- Last reviewed: 2027-01-07
- Confidence: high
