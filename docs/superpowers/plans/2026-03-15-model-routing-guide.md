# Model Routing Guide Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a source-backed model routing guide covering Anthropic Haiku/Sonnet/Opus, GPT-5.4 effort levels, and GPT-5.3 Codex usage decisions.

**Architecture:** Create one knowledge-base decision page and extend the existing Anthropic, OpenAI, and Codex canonical pages with concise routing guidance and links back to the central guide. Wire the new guide into the knowledge-base overview, model comparison page, home page, and MkDocs nav.

**Tech Stack:** Markdown docs, MkDocs nav, docs contract checks, catalog consistency checks.

---

### Implementation Status

- [x] Create central `docs/knowledge_base/model_routing_guide.md`.
- [x] Extend `docs/tools/ai_knowledge/openai.md` with effort-level routing.
- [x] Extend `docs/tools/development_ops/codex.md` with model routing.
- [x] Extend `docs/tools/ai_knowledge/claude.md` with tier routing.
- [x] Wire into `docs/index.md`.
- [x] Wire into `docs/knowledge_base/README.md`.
- [x] Wire into `docs/knowledge_base/model_comparison_and_evaluation.md`.
- [x] Add to `mkdocs.yml` navigation.

---

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
