# Vellum

## What it is
Vellum is a personal AI assistant designed specifically for macOS. It lives on the user's computer and integrates deeply with local files, email, calendar, and other desktop applications. It aims to be a "proactive" assistant that learns user patterns and takes action on their behalf.

## What problem it solves
It bridges the gap between conversational AI and practical task execution. Unlike web-based chat tools, Vellum can see the user's screen (with permission), manage local files, and interact with other macOS apps directly to automate repetitive workflows. It leverages reasoning models like **Claude 5.1** and **GPT-5.5** for high-autonomy task completion.

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
- **November 2026 Ready**: Native support for **Claude 5.1** reasoning, **GPT-5.5** canvas, and a broad [MCP 3.1](mcp.md) skill catalog.

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
- For enterprise-wide automation that requires a headless, server-side environment.

## Getting started
### Installation
Install the Vellum CLI globally:
```bash
pip install -g vellum
```

### Initialization
Initialize your assistant and begin the onboarding process:
```bash
vellum hatch
```

### Hello-world example
1. Run `vellum client` to open the terminal interface.
2. Type "Introduce yourself and tell me what you can see on my screen."
3. Vellum will analyze your active window and respond with its personality and a summary of your workspace.

## CLI examples
The CLI is the primary way to manage and interact with the Vellum runtime.

```bash
vellum wake        # Start background services
vellum ps          # List all running assistant instances
vellum client      # Open the interactive terminal client
vellum mcp add     # Add an MCP server to Vellum's skill set (Standard 3.1)
```

## API examples
Vellum exposes a real-time SSE (Server-Sent Events) stream for programmatic interaction. Under late 2026 requirements, Python-based trigger event handlers must utilize **Pydantic v2** validation to model desktop actions.

### Desktop Trigger Validation and Request Handling (Python)
```python
import json
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# Define Pydantic v2 schemas for desktop trigger verification
class VellumWorkflowTrigger(BaseModel):
    target_app: str = Field(..., min_length=2, description="Target application name (e.g. Finder, Chrome)")
    event_type: str = Field(..., description="Action type like 'file_added' or 'email_received'")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata associated with the action")
    priority: int = Field(default=3, ge=1, le=5, description="Trigger priority, 1 highest")

# Raw payload representing Finder workspace file creation event
raw_trigger = {
    "target_app": "Finder",
    "event_type": "file_added",
    "metadata": {
        "filename": "K3s_cluster_backup.yaml",
        "filepath": "/Users/jules/Desktop/K3s_cluster_backup.yaml"
    },
    "priority": 2
}

try:
    # Model validation under Pydantic v2 guidelines
    validated_trigger = VellumWorkflowTrigger.model_validate(raw_trigger)
    print(f"Validated desktop trigger: app='{validated_trigger.target_app}', event='{validated_trigger.event_type}'")

    # Process validated trigger to initiate Vellum agent stream
    # payload = validated_trigger.model_dump_json()
    # print(f"Serialized JSON payload: {payload}")
except Exception as e:
    print(f"Validation failed: {e}")
```

### Javascript SSE Consumer Example
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
- [Open Interpreter](open-interpreter.md) — Multi-platform terminal-based agent.
- [Goose](../agents/goose.md) — Open-source agentic orchestrator.
- [Claude Code](../development_ops/claude-code.md) — Terminal-based coding assistant with MCP.
- [Model Context Protocol (MCP)](mcp.md) — The standard for tool integration (v3.1).
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Patterns used by Vellum for task execution.
- [Claude 5.1](../providers/anthropic.md) — Primary reasoning model for high-autonomy tasks.
- [GPT-5.5](../ai_knowledge/openai.md) — High-performance alternative for document synthesis.
- [OpenClaw](../development_ops/openclaw.md) — Open-source desktop automation alternative.

## Sources / references
- [Vellum Official Website](https://www.vellum.ai/)
- [Vellum Documentation](https://www.vellum.ai/docs)
- [Vellum AI Assistant Review 2026](https://www.vellum.ai/llm-leaderboard/ai-assistants/vellum)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
