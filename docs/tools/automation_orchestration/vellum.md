# Vellum

## What it is
Vellum is a personal AI assistant designed specifically for macOS. It lives on the user's computer and integrates deeply with local files, email, calendar, and other desktop applications. It aims to be a "proactive" assistant that learns user patterns and takes action on their behalf.

## What problem it solves
It bridges the gap between conversational AI and practical task execution. Unlike web-based chat tools, Vellum can see the user's screen (with permission), manage local files, and interact with other macOS apps directly to automate repetitive workflows. It leverages reasoning models like **Claude 4.7** and **GPT-5.5** for high-autonomy task completion.

## Where it fits in the stack
**Category**: Automation & Orchestration / Personal AI Assistant. It is a local agent that orchestrates various tools and services, often serving as the central hub for a user's [AI Tool Access Matrix](../../knowledge_base/ai_tool_access_matrix.md).

## Typical use cases
- **Inbox Management**: Automatically triaging and drafting replies to emails in Gmail using native connectors.
- **Backlog Grooming**: Auto-labeling and triaging GitHub issues or Linear tasks based on team rules.
- **Meeting Preparation**: Summarizing Slack conversations and documents to provide a briefing before a meeting.
- **Local Automation**: Cleaning up a cluttered desktop or organizing local files based on natural language commands.
- **Cross-App Orchestration**: Using [Model Context Protocol (MCP)](mcp.md) to bridge data between specialized tools.

## Strengths
- **Deep macOS Integration**: Leverages accessibility and screen recording for "computer use" capabilities.
- **Privacy-First Architecture**: Stores credentials in macOS Keychain; memories and workspace data remain local.
- **Proactive Intelligence**: Designed to act before being asked by noticing patterns in user behavior.
- **June 2026 Ready**: Native support for **Claude 4.7** reasoning, **GPT-5.5** canvas, and a broad [MCP](mcp.md) skill catalog.

## Limitations
- **Platform Restricted**: Currently only available for macOS (Apple Silicon and Intel).
- **Cost**: Uses a prepaid credit system for AI model usage or a subscription for managed features.
- **Resource Intensive**: Running a deep-integration assistant can impact system performance on older hardware.

## When to use it
- If you are a macOS user looking for a deeply integrated personal AI agent.
- If you want to automate routine digital tasks like email triage or issue management.
- If you value local data storage and privacy in your AI interactions.

## When not to use it
- If you are on Windows or Linux (consider [OpenHands](../development_ops/openhands.md) or [Aider](../development_ops/aider.md)).
- If you prefer a fully open-source, community-managed agent like [OpenClaw](../development_ops/openclaw.md).

## Licensing and cost
- **Open Source**: No (Proprietary)
- **Cost**: Paid (Prepaid credits / Subscription)
- **Self-hostable**: No (Managed desktop app)

## Getting started
Install the Vellum CLI globally:
```bash
pip install -g vellum
```

Initialize your assistant:
```bash
# This begins the onboarding and hatch process
vellum hatch
```

**Hello-world example**:
1. Run `vellum client` to open the terminal interface.
2. Type "Introduce yourself and tell me what you can see on my screen."
3. Vellum will analyze your active window and respond with its personality and a summary of your workspace.

## CLI examples
The CLI is the primary way to manage and interact with the Vellum runtime.

```bash
vellum wake        # Start background services
vellum ps          # List all running assistant instances
vellum client      # Open the interactive terminal client
vellum mcp add     # Add an MCP server to Vellum's skill set (June 2026)
```

## API examples
Vellum exposes a real-time SSE (Server-Sent Events) stream for programmatic interaction.

```javascript
const response = await fetch('http://localhost:3001/v1/events', {
  headers: { 'Authorization': 'Bearer YOUR_JWT_TOKEN' }
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const chunk = decoder.decode(value);
  console.log('Received event:', chunk);
}
```

## Related tools / concepts
- [Open Interpreter](open-interpreter.md)
- [Goose](goose.md)
- [Claude Code](../development_ops/claude-code.md)
- [Model Context Protocol (MCP)](mcp.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Claude 4.7](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)
- [Llama 4 Maverick](../ai_knowledge/local_llms.md)

## Sources / references
- [Vellum Official Website](https://www.vellum.ai/)
- [Vellum Documentation](https://www.vellum.ai/docs)
- [Vellum AI Assistant Review 2026](https://www.vellum.ai/llm-leaderboard/ai-assistants/vellum)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
