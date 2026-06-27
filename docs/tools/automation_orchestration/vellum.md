# Vellum

## What it is
Vellum is a proactive, personal AI assistant designed specifically for macOS. As of June 2026, it serves as a central orchestrator for a user's local digital workspace, integrating deeply with files, email, calendar, and desktop applications. It is a proprietary managed desktop application that prioritizes local reasoning and deep OS integration.

## What problem it solves
It bridges the gap between conversational AI and practical task execution. Unlike web-based chat tools, Vellum can see the user's screen (with permission), manage local files, and interact with other macOS apps directly to automate repetitive workflows. It solves the "context gap" by leveraging reasoning models like **Claude 4.8 Opus** and **GPT-5.5** for high-autonomy task completion.

## Where it fits in the stack
**Category**: Automation & Orchestration / Personal AI Assistant. It acts as the local agent layer that orchestrates various tools and services, often serving as the central hub for the [AI Tool Access Matrix](../../knowledge_base/ai_tool_access_matrix.md).

## Typical use cases
- **Inbox Management**: Automatically triaging and drafting replies to emails in Gmail or Apple Mail using native connectors.
- **Backlog Grooming**: Auto-labeling and triaging GitHub issues or Linear tasks based on natural language team rules.
- **Meeting Preparation**: Summarizing Slack conversations and documents across apps to provide a briefing before a meeting.
- **Local Automation**: Cleaning up a cluttered desktop or organizing local files based on complex natural language commands.
- **Cross-App Orchestration**: Using [Model Context Protocol (MCP 3.0)](mcp.md) to bridge data between specialized tools like [Aider](../development_ops/aider.md) and [Linear](../calendar_tasks/index.md).

## Strengths
- **Deep macOS Integration**: Leverages accessibility and screen recording for high-fidelity "computer use" capabilities.
- **Privacy-First Architecture**: Stores credentials in macOS Keychain; memories and workspace data remain local.
- **Proactive Intelligence**: Designed to act before being asked by noticing patterns in user behavior and suggesting automations.
- **June 2026 Ready**: Native support for **Claude 4.8** reasoning, **GPT-5.5** multi-modal canvas, and a broad [MCP 3.0](mcp.md) skill catalog.

## Limitations
- **Platform Restricted**: Only available for macOS (Apple Silicon recommended).
- **Cost**: Uses a subscription-based model or a prepaid credit system for premium model usage.
- **Resource Intensive**: High system overhead when using real-time screen analysis and local embedding models.
- **Proprietary**: The core orchestration engine is closed-source, which may not suit "sovereign-only" users.

## When to use it
- If you are a macOS power user looking for a deeply integrated personal AI agent that can "see" and "do."
- If you want to automate routine digital tasks like email triage, issue management, or file organization.
- If you value local data storage and privacy in your primary AI interactions.
- When utilizing **Claude 4.8** or **GPT-5.5** for high-autonomy personal assistance.

## When not to use it
- If you are on Windows or Linux (consider [OpenHands](../development_ops/openhands.md) or [Aider](../development_ops/aider.md)).
- If you prefer a fully open-source, community-managed agent like [OpenClaw](../development_ops/openclaw.md).
- If your hardware lacks the resources (minimum 16GB RAM) for smooth background operation.

## Getting started
### Installation
Download the latest `.dmg` from the [Vellum Portal](https://www.vellum.ai/download). Alternatively, install the CLI:

```bash
# Install the Vellum CLI
pip install vellum-cli
```

### Initial Setup
```bash
# This begins the onboarding and secure 'hatch' process
vellum hatch
```

**Hello-world example**:
1. Run `vellum client` to open the terminal interface.
2. Type "Summarize my active windows and suggest a task list based on my current work."
3. Vellum will analyze your workspace and provide a proactive response.

## CLI examples
The Vellum CLI is the primary way to manage the background runtime and MCP skills.

### Runtime Management
```bash
# Start background services
vellum wake

# List all active assistant personas
vellum ps

# Open the interactive terminal client
vellum client
```

### Skill Management (MCP 3.0)
```bash
# Add a new MCP server to Vellum's skill set
vellum mcp add --name chronos-sync --transport stdio --command "npx @openclaw/chronos-mcp"
```

## API examples
Vellum exposes a local real-time stream for programmatic integration.

### Listening to Assistant Events (JavaScript)
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
  console.log('Vellum Event:', chunk);
}
```

### Health Check (Bash)
```bash
curl -X GET http://localhost:3001/v1/health
```

## Related tools / concepts
- [Open Interpreter](open-interpreter.md) — Local-first code execution assistant.
- [Goose](../agents/goose.md) — Multi-agent orchestrator for technical tasks.
- [Claude Code](../development_ops/claude-code.md) — High-fidelity coding agent from Anthropic.
- [Model Context Protocol (MCP)](mcp.md) — The standard for tool-based agent integration.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Design patterns for autonomous agents.
- [Claude](../ai_knowledge/claude.md) — Primary reasoning model for Vellum.
- [GPT-5.5](../ai_knowledge/openai.md) — Supported frontier model for multi-modal tasks.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) — Recommended local model for private reasoning.

## Sources / references
- [Vellum Official Website](https://www.vellum.ai/)
- [Vellum Documentation](https://www.vellum.ai/docs)
- [Vellum AI Assistant Review 2026](https://www.vellum.ai/llm-leaderboard/ai-assistants/vellum)

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
