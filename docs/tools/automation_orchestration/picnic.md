# Picnic

## What it is
Picnic is a structured, project-centered GUI built on top of [OpenClaw](../development_ops/openclaw.md) for managing notes, files, goals, and AI-assisted workflows in a calm environment.

## What problem it solves
Raw agent environments can be chaotic and overwhelming. Picnic provides a human-friendly interface for [OpenClaw](../development_ops/openclaw.md), allowing users to organize work into projects and keep sensitive browsing behavior isolated within Picnic's own built-in browser. It makes AI collaboration safer and more deliberate for [Gemma 3](../ai_knowledge/local_llms.md), Claude 4.8 Opus, and GPT-5.5 users.

## Where it fits in the stack
**Automation runtime / desktop orchestration layer**. Picnic sits above the [OpenClaw](../development_ops/openclaw.md) core, providing a structured workspace for business, personal, and family work.

## Typical use cases
- Organizing complex business projects with AI-assisted notes and files.
- Running browser-based agent workflows safely using the built-in browser.
- Maintaining long-term context for family planning or personal journals.
- Collaborative thinking and planning where structure emerges over time.

## Strengths
- **Project Isolation**: Keeps work organized and prevents context drift.
- **Built-in Browser**: Isolates agent browsing from your primary browser session.
- **Gradual Structure**: Start with a blank page and add context cards only when needed.
- **Open Source Core**: Leverages the power and public scrutiny of [OpenClaw](../development_ops/openclaw.md).
- **MCP 3.0 Integration**: Native support for [MCP](mcp.md) tool discovery and execution.

## Limitations
- Still in beta; features and project structures are subject to change.
- Primarily GUI-driven; lacks a robust public-facing CLI or API for direct manipulation.
- Requires local resources to run the desktop application and underlying agent runtime.

## When to use it
- When you want a calmer, more organized interface for your AI work.
- When you need to manage multiple projects without mixing their context.
- When safety and browser isolation are high priorities.

## When not to use it
- If you require a headless, API-only automation engine (use [OpenClaw](../development_ops/openclaw.md) directly).
- If you prefer a simple chat interface without project management features.

## Getting started
Picnic is a desktop GUI application and does not have official developer documentation, CLI tools, or programmatic APIs.

To get started with the desktop interface:
1. **Download**: Obtain the desktop application for Windows, Linux, or macOS from the [official website](https://picnicos.com/).
2. **Setup**: Authenticate and configure your preferred LLM provider credentials (e.g., Anthropic, OpenAI, or local models).
3. **Organize**: Create a new project space and begin managing notes, files, and goals.

## CLI examples
> [!NOTE]
> Picnic does not provide an official command-line interface (CLI). All operational workflows and configurations are managed within the desktop application GUI. Accordingly, CLI code examples are skipped.

## API examples
> [!NOTE]
> Picnic does not expose a public programmatic API or developer SDK. Interaction and automation are handled entirely through the built-in workspace and browser integration. Accordingly, API code examples are skipped.

## Related tools / concepts
- [OpenClaw](../development_ops/openclaw.md)
- [Browser Use](browser-use.md)
- [n8n](../../services/n8n.md)
- [Home Assistant](../../services/home-assistant.md)
- [LiteLLM](../../services/litellm.md)
- [ClawRouter](../infrastructure/clawrouter.md)
- [OpenClaw Security Operations](../../knowledge_base/patterns/openclaw-security-operations.md)
- [Claude Code](../development_ops/claude-code.md)
- [Model Context Protocol](mcp.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Picnic Official Site](https://picnicos.com/)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
