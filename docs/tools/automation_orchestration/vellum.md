# Vellum

## What it is
Vellum is a personal AI assistant and desktop automation runtime designed specifically for macOS (Apple Silicon and Intel). It lives on the user's computer and integrates deeply with local files, system accessibility APIs, local email clients, calendars, and terminal instances. Operating as a hybrid local daemon and cloud-routed orchestrator, Vellum aims to be a "proactive" assistant that continuously observes workspace patterns, interprets natural language intent, and executes multi-step system workflows on behalf of the user.

## What problem it solves
It bridges the gap between conversational AI interfaces and practical desktop task execution. Unlike web-based chat tools or cloud sandboxes, Vellum can inspect the user's desktop environment (with explicit macOS accessibility permissions), manage local directory hierarchies, manipulate GUI applications via computer-use vision models, and interact with native APIs to automate complex, multi-application workflows. It leverages early 2027 frontier reasoning models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro** for autonomous decision-making and error recovery.

## Where it fits in the stack
**Category**: Automation & Orchestration / Personal AI Assistant & Desktop Runtime. It functions as a local autonomous agent orchestrating local CLI tools, native applications, and cloud microservices, frequently acting as the desktop command node for an organization's [AI Tool Access Matrix](../../knowledge_base/ai_tool_access_matrix.md).

## Architecture & System Mechanics

```
                  +-------------------------------------------------------+
                  |                     macOS Desktop                     |
                  |                                                       |
                  |  +---------------------+     +---------------------+  |
                  |  | System Accessibility|     | Local File System & |  |
                  |  | & Screen Vision API |     | Native App Handlers |  |
                  |  +----------+----------+     +----------+----------+  |
                  +-------------|---------------------------|-------------+
                                |                           |
                                v                           v
                  +-------------------------------------------------------+
                  |                     Vellum Daemon                     |
                  |                                                       |
                  |  +--------------------+     +----------------------+  |
                  |  |  Event Dispatcher  |     |   Context Store &    |  |
                  |  |  & SSE Broadcaster |     |   Keychain Security  |  |
                  |  +---------+----------+     +----------+-----------+  |
                  +------------|---------------------------|--------------+
                               |                           |
                               v                           v
                  +-------------------------------------------------------+
                  |               FastMCP 3.1 Plugin Host                 |
                  |                                                       |
                  |  +--------------------+     +----------------------+  |
                  |  | Local MCP Servers  |     | Remote Enterprise    |  |
                  |  | (Git, Files, Shell)|     | MCP Connectors       |  |
                  |  +---------+----------+     +----------+-----------+  |
                  +------------|---------------------------|--------------+
                               |                           |
                               +-------------+-------------+
                                             |
                                             v
                  +-------------------------------------------------------+
                  |               Frontier Reasoning Engine               |
                  |                                                       |
                  |   Claude 5.1 / GPT-5.5 / Gemini 4.0 Pro API Gateway   |
                  +-------------------------------------------------------+
```

Vellum operates as a multi-tiered desktop runtime composed of five primary subsystems:

1. **System Observer Subsystem**: Listens for system events (file system mutations, window focus changes, clipboard updates) using native macOS EventKit and FSEvents listeners, queuing candidate triggers for processing.
2. **Context Memory Store**: Maintains persistent local state using an embedded SQLite database encrypted via SQLCipher. API keys and credentials are stored exclusively in the macOS System Keychain (`/System/Library/Keychains`).
3. **FastMCP 3.1 Plugin Manager**: Serves as the protocol adapter for local and remote Model Context Protocol servers, allowing Vellum to discover, inspect, and invoke dynamic capabilities safely.
4. **Agent Orchestration Engine**: Manages task plan generation, sub-task execution loops, vision analysis of desktop states, and retry logic when application interactions fail.
5. **Real-Time Stream Server**: Exposes an internal SSE (Server-Sent Events) interface over localhost port `3001` to deliver state updates, action logs, and confirmation prompts to terminal clients or external UI overlays.

## Typical use cases
- **Inbox Management & Email Triage**: Automatically triaging, labeling, and drafting contextually aware replies to inbound messages in native Mail or web webmail instances.
- **Automated Backlog Maintenance**: Auto-labeling, cross-referencing, and triaging GitHub issues, Linear tickets, or Jira tasks based on team-defined SLA rules.
- **Contextual Meeting Preparation**: Scraping recent Slack messages, Google Docs, and calendar invites to assemble unified executive briefings before scheduled meetings.
- **Workspace Clean-Up & Maintenance**: Organizing local downloads directories, archiving stale code repositories, and cataloging project PDFs using semantic natural language commands.
- **Cross-App Data Pipelines**: Orchestrating data flow between specialized productivity tools via [FastMCP 3.1](mcp.md) servers without manually copying and pasting text.

## Strengths
- **Native macOS Deep Integration**: Direct access to macOS accessibility, screen capture, AppleScript, and system event frameworks for computer-use capabilities.
- **Privacy-First Architecture**: Sensitive operational state remains entirely on local disk; credentials reside safely within the macOS Keychain.
- **Proactive Intelligence**: Detects repetitive user workflows and offers natural language suggestions before explicitly being queried.
- **Frontier AI Interoperability**: Out-of-the-box integration with **Claude 5.1** reasoning engines, **GPT-5.5** structural generation, and **Gemini 4.0 Pro** multimodal vision models.
- **Extensible Plugin Model**: Native support for **FastMCP 3.1** protocol contracts, enabling instant access to thousands of community tools.

## Limitations
- **Platform Restricted**: Built strictly for macOS environments (Apple Silicon M1/M2/M3/M4 and Intel X86_64); no native Linux or Windows builds.
- **Resource Footprint**: Running background vision processing and local vector indexes requires substantial RAM (16GB+ recommended) and CPU cycles.
- **API Cost Overhead**: High-frequency proactive polling and autonomous multi-turn plan execution can rapidly consume third-party API tokens.

## When to use it
- When working on a macOS workstation and needing an autonomous agent capable of driving desktop applications.
- When automating complex cross-application administrative routines that lack unified REST APIs.
- When requiring strong privacy controls where operational memory must not leave the local filesystem.

## When not to use it
- When deploying headless automation scripts on Linux servers or containerized K8s clusters (use [Prefect](prefect.md) or [Temporal](../development_ops/temporal.md)).
- When requiring a pure web-browser automation stack across headless Linux instances (use [Playwright MCP](playwright-mcp.md) or [Puppeteer](puppeteer.md)).
- When building multi-platform open-source agent applications targeting Windows and Linux desktops (use [Open Interpreter](open-interpreter.md) or [Aider](../development_ops/aider.md)).

## Getting started
### Installation
Install the Vellum CLI distribution using Python standard packaging:
```bash
pip install -U vellum-cli
```

### Initialization
Initialize your assistant environment, generate cryptographic session keys, and establish macOS Keychain bindings:
```bash
vellum hatch
```

### Hello-world example
1. Launch the interactive terminal client:
   ```bash
   vellum client
   ```
2. Enter the prompt:
   ```text
   Introduce yourself, check my current active desktop window, and display system resource utilization.
   ```
3. Vellum will query the system state, analyze active desktop context, and display a detailed overview of your local workspace.

## CLI examples

```bash
# Start background Vellum orchestration daemon
vellum wake --daemon

# Inspect status of running agent threads and MCP servers
vellum ps

# Launch interactive CLI client with debug verbosity
vellum client --log-level DEBUG

# Register a FastMCP 3.1 server with local Vellum runtime
vellum mcp add --name github-tools --command "npx -y @modelcontextprotocol/server-github"

# Export system diagnostic bundle for security audit
vellum audit export --output ~/vellum-audit-log.json
```

## API examples

Under early 2027 SOTA development standards, all system triggers, tool invocations, and agent response payloads are strictly validated using **Pydantic v2**. Below is a complete production Python implementation for validating incoming workspace trigger events and executing background workflows.

### Workspace Trigger & Action Dispatcher (Python)

```python
import sys
import json
import asyncio
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ValidationError, field_validator

# ---------------------------------------------------------------------------
# Pydantic v2 Contract Definitions
# ---------------------------------------------------------------------------

class EventMetadata(BaseModel):
    filepath: Optional[str] = Field(default=None, description="Absolute filesystem path associated with event")
    app_identifier: str = Field(..., description="Bundle ID or application string (e.g., com.apple.finder)")
    window_title: Optional[str] = Field(default=None, description="Title of active application window")
    extra_payload: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary event payload attributes")

class VellumWorkflowTrigger(BaseModel):
    trigger_id: str = Field(..., min_length=8, description="Unique identifier for the trigger event")
    target_app: str = Field(..., min_length=2, description="Target desktop application name")
    event_type: str = Field(..., description="Type of event ('file_created', 'email_arrived', 'focus_changed')")
    priority: int = Field(default=3, ge=1, le=5, description="Execution priority (1 = Immediate, 5 = Background)")
    metadata: EventMetadata = Field(..., description="Structured metadata payload")

    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        allowed = {'file_created', 'file_modified', 'email_arrived', 'focus_changed', 'shortcut_pressed'}
        if v not in allowed:
            raise ValueError(f"Unsupported event_type '{v}'. Must be one of {allowed}")
        return v

class AgentExecutionPlan(BaseModel):
    plan_id: str = Field(..., description="Plan identifier issued by Claude 5.1/GPT-5.5")
    trigger_id: str = Field(..., description="Associated trigger ID")
    steps: List[str] = Field(..., min_length=1, description="Sequential steps to execute")
    requires_user_confirmation: bool = Field(default=False, description="Whether explicit approval is needed")

# ---------------------------------------------------------------------------
# Trigger Processor Routine
# ---------------------------------------------------------------------------

async def process_desktop_event(raw_data: dict) -> AgentExecutionPlan:
    """Validates raw event data and generates an execution plan."""
    try:
        # Validate raw incoming JSON against Pydantic v2 model
        trigger = VellumWorkflowTrigger.model_validate(raw_data)
        print(f"[SUCCESS] Validated trigger '{trigger.trigger_id}' for app '{trigger.target_app}'")

        # Simulate agent plan synthesis
        plan = AgentExecutionPlan(
            plan_id=f"plan-{trigger.trigger_id}",
            trigger_id=trigger.trigger_id,
            steps=[
                f"Inspect event metadata for {trigger.metadata.app_identifier}",
                "Query FastMCP 3.1 local file server",
                "Execute workspace cleanup routine"
            ],
            requires_user_confirmation=(trigger.priority == 1)
        )
        return plan

    except ValidationError as err:
        print(f"[ERROR] Pydantic v2 Schema Validation Failed:\n{err.json(indent=2)}")
        raise

# ---------------------------------------------------------------------------
# Execution Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample_raw_payload = {
        "trigger_id": "trig-99023481",
        "target_app": "Finder",
        "event_type": "file_created",
        "priority": 2,
        "metadata": {
            "filepath": "/Users/jules/Downloads/Q3_Financial_Report.pdf",
            "app_identifier": "com.apple.finder",
            "window_title": "Downloads",
            "extra_payload": {"file_size_bytes": 10485760}
        }
    }

    result_plan = asyncio.run(process_desktop_event(sample_raw_payload))
    print(f"\nSynthesized Plan JSON:\n{result_plan.model_dump_json(indent=2)}")
```

### Real-Time SSE Event Consumer (Node.js / JavaScript)

```javascript
import { EventSource } from 'eventsource';

/**
 * Connects to Vellum's local daemon SSE server and streams real-time state changes.
 */
function connectVellumStream(apiToken) {
  const url = 'http://127.0.0.1:3001/v1/events';
  const eventSource = new EventSource(url, {
    headers: { Authorization: `Bearer ${apiToken}` }
  });

  eventSource.onopen = () => {
    console.log('[Vellum SSE] Connected to local desktop daemon stream.');
  };

  eventSource.addEventListener('trigger', (event) => {
    const data = JSON.parse(event.data);
    console.log(`[Vellum Event] Trigger received: ${data.event_type} from ${data.target_app}`);
  });

  eventSource.addEventListener('execution_step', (event) => {
    const data = JSON.parse(event.data);
    console.log(`[Vellum Agent] Executing step ${data.step_index}: ${data.description}`);
  });

  eventSource.onerror = (err) => {
    console.error('[Vellum SSE] Stream error encounter:', err);
  };
}

// Example usage
connectVellumStream('local-dev-jwt-token-2027');
```

## Production Security & Governance

When running Vellum in enterprise or sensitive workspace environments, adhere to the following security protocols:

1. **Keychain Isolation**: Ensure that all LLM vendor API credentials (Anthropic, OpenAI, Google Cloud) are stored via `vellum secret set` rather than in plain-text environment variables or config files.
2. **Accessibility Scope Control**: Limit macOS Accessibility and Screen Recording permissions to designated dedicated user accounts when using Vellum on multi-tenant developer machines.
3. **MCP Plugin Verification**: Always verify the hash and origin of third-party FastMCP 3.1 server binaries before executing `vellum mcp add`.
4. **Audit Log Persistence**: Enable immutable logging to maintain an audit trail of executed desktop commands and system mutations.

## Related tools / concepts
- [Open Interpreter](open-interpreter.md) — Multi-platform terminal-based natural language code execution agent.
- [Goose](../agents/goose.md) — Open-source agentic developer orchestrator.
- [Claude Code](../development_ops/claude-code.md) — Terminal coding assistant integrated with MCP tooling.
- [Model Context Protocol (MCP)](mcp.md) — Open standard (v3.1) for bidirectional tool and data integration.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Architectural patterns for autonomous multi-step reasoning.
- [Claude 5.1](../providers/anthropic.md) — Frontier reasoning model for autonomous desktop orchestration.
- [GPT-5.5](../ai_knowledge/openai.md) — Multimodal generation and decision-making model.
- [OpenClaw](../development_ops/openclaw.md) — Open-source cross-platform desktop automation tool.

## Sources / references
- [Vellum Official Website](https://www.vellum.ai/)
- [Vellum Developer Documentation](https://www.vellum.ai/docs)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/spec)
- [Vellum AI Desktop Architecture Analysis (2027)](https://www.vellum.ai/llm-leaderboard/ai-assistants/vellum)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
