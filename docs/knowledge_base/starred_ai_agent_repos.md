# Starred AI / Agent Repositories Over 10K Stars

This page summarizes the AI and agent-related repositories from your GitHub stars that currently have more than 10,000 GitHub stars. It is meant to answer a practical question: what does each repo actually add to a stack, when should it be used, and which ones are baseline additions versus situational choices.

Star counts below are from a GitHub API snapshot pulled on 2026-03-14 from your starred repositories. "Reputation" is an editorial assessment based on maintainer track record, institutional backing, and ecosystem trust, not a GitHub API field.

## Quick take
- **Default baseline for Claude/coding-agent work**: [anthropics/skills](https://github.com/anthropics/skills), [obra/superpowers](https://github.com/obra/superpowers), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks), [Context7](../tools/development_ops/context7.md)
- **Usually used in combination with other tools**: [browser-use/browser-use](https://github.com/browser-use/browser-use), [mem0](../tools/agents/mem0.md), [openai/whisper](https://github.com/openai/whisper), [google/langextract](https://github.com/google/langextract), [googleworkspace/cli](https://github.com/googleworkspace/cli), [llmfit](../tools/development_ops/llmfit.md), [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router), [farion1231/cc-switch](https://github.com/farion1231/cc-switch)
- **Strong but situational primary stacks**: [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT), [anomalyco/opencode](https://github.com/anomalyco/opencode), [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise), [LocalAI](../tools/infrastructure/localai.md), [DeerFlow](../tools/agents/deerflow.md), [Fosowl/agenticSeek](https://github.com/Fosowl/agenticSeek), [stitionai/devika](https://github.com/stitionai/devika), [plandex-ai/plandex](https://github.com/plandex-ai/plandex)

## Decision table

| Repo | Stars | Reputation | Core value | Use when | Default stance | Best combinations |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | 182,452 | Early category-defining OSS project; high name recognition, mixed practical fit | Popularized autonomous-agent loops and agent-platform thinking | You want to study agent history or need a broad autonomous-agent platform | Situational | Pair with [mem0](https://github.com/mem0ai/mem0) and [browser-use](https://github.com/browser-use/browser-use) if you actually operationalize it |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | 122,146 | Strong breakout OSS coding-agent project | Full coding-agent runtime with modern CLI workflow | You want a serious open coding-agent environment rather than a prompt pack | Situational primary stack | Pair with [upstash/context7](https://github.com/upstash/context7), [anthropics/skills](https://github.com/anthropics/skills), and [browser-use](https://github.com/browser-use/browser-use) |
| [openai/whisper](https://github.com/openai/whisper) | 95,946 | Top-tier lab, widely trusted | Speech-to-text layer for voice, meetings, media, and multimodal ingestion | Your agent/app needs audio input or transcription | Pair with others | Pair with [n8n](../services/whisper.md), [browser-use](https://github.com/browser-use/browser-use), or content pipelines |
| [anthropics/skills](https://github.com/anthropics/skills) | 93,449 | Top-tier lab; first-party reference | Canonical reusable skill format and examples for Claude-centric workflows | You are using Claude Code or Claude-based agents | Always consider for Claude stacks | Pair with [obra/superpowers](https://github.com/obra/superpowers), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks), and [upstash/context7](https://github.com/upstash/context7) |
| [obra/superpowers](https://github.com/obra/superpowers) | 83,255 | High-signal solo maintainer with major ecosystem adoption | Strong engineering process for coding agents: brainstorming, planning, TDD, review | You want higher-quality agent output instead of raw speed | Always consider for coding agents | Pair with [anthropics/skills](https://github.com/anthropics/skills), [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks), and your preferred coding agent |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 80,774 | Established OSS agent-tool project | Makes websites operable by agents when APIs are missing or insufficient | The workflow depends on real browser interaction | Pair with others | Pair with [Playwright](../tools/development_ops/playwright.md), [Tavily](../tools/providers/tavily.md), and [mem0](https://github.com/mem0ai/mem0) |
| [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) | 50,749 | Established OSS vendor in LLM tooling | Visual builder for agents, RAG, and workflows | You want a visual control plane rather than a pure-code framework | Situational primary stack | Pair with [LocalAI](https://github.com/mudler/LocalAI), [Supabase](../tools/infrastructure/supabase.md), or [n8n](../services/n8n.md) |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 49,821 | Focused startup with clear category fit | Durable memory layer for agents | Your agents need persistent user/task/project memory | Pair with others | Pair with [browser-use](https://github.com/browser-use/browser-use), [deer-flow](https://github.com/bytedance/deer-flow), or coding agents |
| [upstash/context7](https://github.com/upstash/context7) | 49,032 | Strong devtools company reputation | Fresh documentation/context retrieval for LLMs and coding agents | Agents need current library docs instead of stale model memory | Always consider for coding agents | Pair with [opencode](https://github.com/anomalyco/opencode), [Claude Code](../tools/development_ops/claude-code.md), and [superpowers](https://github.com/obra/superpowers) |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 44,053 | Strong org and broad ecosystem presence | Discovery index for Claude skill packs and workflow resources | You want to survey the skills ecosystem quickly | Pair with others | Pair with [anthropics/skills](https://github.com/anthropics/skills) and [superpowers](https://github.com/obra/superpowers) |
| [mudler/LocalAI](https://github.com/mudler/LocalAI) | 43,605 | Well-known OSS local-AI project | OpenAI-compatible local inference stack | You want local/self-hosted inference with broad provider compatibility | Situational primary stack | Pair with [llmfit](https://github.com/AlexsJones/llmfit), [Flowise](https://github.com/FlowiseAI/Flowise), and [Supabase](../tools/infrastructure/supabase.md) |
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | 43,446 | Strong community-maintained prompt/agent pack | A packaged "AI agency" roster of specialist agents | You want pre-shaped specialist roles for marketing/content/ops | Situational | Pair with [n8n](../services/n8n.md), [Claude Code](../tools/development_ops/claude-code.md), and your own SOPs |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 34,951 | Top-tier lab; first-party | Concrete implementation examples for building with Claude | You want to build with Claude from examples rather than guess from API docs | Always consider for Claude stacks | Pair with [anthropics/skills](https://github.com/anthropics/skills) and [superpowers](https://github.com/obra/superpowers) |
| [google/langextract](https://github.com/google/langextract) | 34,701 | Top-tier lab | Structured extraction with grounding and visualization | You need reliable extraction from unstructured text, not general chat | Pair with others | Pair with [NotebookLM](../tools/ai_knowledge/notebooklm.md), [Supabase](../tools/infrastructure/supabase.md), or document pipelines |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 33,913 | Top-tier individual researcher | Minimal, research-oriented autonomous iteration loop | You want to study compact research-agent loops | Situational | Pair with [deer-flow](https://github.com/bytedance/deer-flow) ideas or [Tavily](../tools/providers/tavily.md) |
| [wshobson/agents](https://github.com/wshobson/agents) | 31,235 | Strong solo maintainer with practical Claude Code focus | Multi-agent orchestration and subagent workflows for Claude Code | You want ready-made multi-agent structure on top of Claude Code | Situational primary stack | Pair with [anthropics/skills](https://github.com/anthropics/skills), [superpowers](https://github.com/obra/superpowers), and [context7](https://github.com/upstash/context7) |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 30,532 | Top-tier product organization with strong AI engineering capability | Researches, codes, and creates through a super-agent harness with tools, memories, and subagents | You want a modern research/coding harness rather than a simple chatbot | Situational primary stack | Pair with [Tavily](../tools/providers/tavily.md), [mem0](https://github.com/mem0ai/mem0), and [browser-use](https://github.com/browser-use/browser-use) |
| [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | 30,028 | Strong emerging org around spec-driven Claude workflows | Meta-prompting and spec-driven development system for Claude Code | You want a lighter-weight alternative to Superpowers-style rigor | Situational | Pair with [anthropics/skills](https://github.com/anthropics/skills) and [context7](https://github.com/upstash/context7) |
| [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router) | 29,650 | Strong community utility with clear operational value | Model/provider routing layer for Claude Code | You want to keep the Claude Code UX while swapping model backends or cost profiles | Pair with others | Pair with [cc-switch](https://github.com/farion1231/cc-switch), [LocalAI](https://github.com/mudler/LocalAI), and [OpenRouter](../tools/ai_knowledge/openrouter.md) |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 28,132 | Strong community desktop utility | Desktop control plane for switching across Claude Code, Codex, OpenCode, OpenClaw, and Gemini CLI | You actively use multiple coding agents and want one switchboard | Pair with others | Pair with [claude-code-router](https://github.com/musistudio/claude-code-router) and [anthropics/skills](https://github.com/anthropics/skills) |
| [Fosowl/agenticSeek](https://github.com/Fosowl/agenticSeek) | 25,504 | Strong solo maintainer, local-first niche | Fully local autonomous agent positioned as a local Manus-style system | You want local-only autonomous browsing/coding without paid APIs | Situational primary stack | Pair with [LocalAI](https://github.com/mudler/LocalAI), [llmfit](https://github.com/AlexsJones/llmfit), and [browser-use](https://github.com/browser-use/browser-use) |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | 20,276 | Top-tier platform team | Single CLI for Workspace automation across Drive, Gmail, Calendar, Docs, Sheets, Chat, and Admin | Google Workspace is a core operating surface for your business | Always consider for Workspace-heavy ops | Pair with [n8n](../services/n8n.md), [Gemini Canvas](../tools/ai_knowledge/gemini-canvas.md), and agent skills |
| [stitionai/devika](https://github.com/stitionai/devika) | 19,495 | Well-known open-source Devin-style project | Open-source "agentic software engineer" stack | You want a self-hosted autonomous SWE agent product surface | Situational primary stack | Pair with [context7](https://github.com/upstash/context7) and code-review guardrails |
| [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) | 16,612 | Strong individual utility maintainer | Hardware/model fit calculator across many providers and models | You need to know what can run on your machine before building locally | Pair with others | Pair with [LocalAI](https://github.com/mudler/LocalAI), [Ollama](../services/ollama.md), or [LM Studio](../tools/ai_knowledge/lm-studio.md) |
| [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | 16,043 | Community-maintained playbook repo | Practical conventions and prompts for using Claude Code more effectively | You want field-tested workflow ideas without adopting a whole framework | Pair with others | Pair with [superpowers](https://github.com/obra/superpowers) or [get-shit-done](https://github.com/gsd-build/get-shit-done) |
| [plandex-ai/plandex](https://github.com/plandex-ai/plandex) | 15,078 | Focused OSS vendor | Open-source AI coding agent aimed at real-world, large-project work | You want a terminal-first coding agent designed for bigger codebases | Situational primary stack | Pair with [context7](https://github.com/upstash/context7), [browser-use](https://github.com/browser-use/browser-use), and repo-specific planning conventions |

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
- Last reviewed: 2026-03-14
- Confidence: medium
