# Vellum

## What it is
Vellum is a personal AI assistant designed specifically for macOS. It lives on the user's computer and integrates deeply with local files, email, calendar, and other desktop applications. It aims to be a "proactive" assistant that learns user patterns and takes action on their behalf.

## What problem it solves
It bridges the gap between conversational AI and practical task execution. Unlike web-based chat tools, Vellum can see the user's screen (with permission), manage local files, and interact with other macOS apps directly to automate repetitive workflows.

## Where it fits in the stack
**Category**: Automation & Orchestration / Personal AI Assistant. It is a local agent that orchestrates various tools and services.

## Typical use cases
- **Inbox Management**: Automatically triaging and drafting replies to emails in Gmail.
- **Backlog Grooming**: Auto-labeling and triaging GitHub issues or Linear tasks based on team rules.
- **Meeting Preparation**: Summarizing Slack conversations and documents to provide a briefing before a meeting.
- **Local Automation**: Cleaning up a cluttered desktop or organizing local files based on natural language commands.

## Strengths
- **Deep macOS Integration**: Leverages accessibility and screen recording for "computer use" capabilities.
- **Privacy-First Architecture**: Stores credentials in macOS Keychain; memories and workspace data remain local.
- **Proactive Intelligence**: Designed to act before being asked by noticing patterns in user behavior.
- **Extensible**: Ships with 60+ built-in skills and supports custom skill development.

## Limitations
- **Platform Restricted**: Currently only available for macOS (Apple Silicon and Intel).
- **Cost**: Uses a prepaid credit system for AI model usage.
- **Resource Intensive**: Running a deep-integration assistant can impact system performance on older hardware.

## When to use it
- If you are a macOS user looking for a deeply integrated personal AI agent.
- If you want to automate routine digital tasks like email triage or issue management.
- If you value local data storage and privacy in your AI interactions.

## When not to use it
- If you are on Windows or Linux.
- If you prefer a fully open-source, community-managed agent like OpenClaw.

## Related tools / concepts
- [Open Interpreter](../automation_orchestration/open-interpreter.md)
- [Goose](../automation_orchestration/goose.md)
- [Claude Code](../development_ops/claude-code.md)
- [Personal AI Agents](../../knowledge_base/patterns/index.md)

## Sources / references
- [Official Website](https://www.vellum.ai/)
- [Vellum Documentation](https://www.vellum.ai/docs)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
