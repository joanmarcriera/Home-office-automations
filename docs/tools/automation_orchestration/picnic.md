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
### 1. Download
Download the Picnic desktop app for your operating system (Windows, Linux, or Mac) from the [official site](https://picnicos.com/).

### 2. Connect
Log in and connect your AI provider credentials. Picnic works with standard subscriptions or direct API keys.

### 3. Create a Project
Start a new project (Business, Personal, or Blank) and begin adding your notes, files, and goals.

## CLI examples
> [!NOTE]
> Picnic is primarily a GUI-driven application. CLI access is managed via the underlying [OpenClaw](../development_ops/openclaw.md) runtime.
```bash
# Verify the OpenClaw core version Picnic is using
openclaw --version
```

## API examples
> [!NOTE]
> Picnic does not currently expose a direct public API. Interaction is handled via the GUI or by extending [OpenClaw](../development_ops/openclaw.md) skills.
```json
// Example of an OpenClaw skill used within Picnic
{
  "name": "picnic_context_helper",
  "description": "Assists with project organization inside Picnic"
}
```

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
