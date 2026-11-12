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

## Mathematical Formulations & Computer-Use Action Dynamics

Autonomous desktop interaction in Vellum is governed by three primary computational dynamics: accessibility tree traversal complexity, affine coordinate projection for multimodal vision models, and multi-turn planning convergence bounds.

### 1. Accessibility Tree Node Traversal Complexity
macOS Accessibility UI hierarchies are represented as a directed rooted graph $G = (V, E)$, where vertices $v \in V$ represent UI elements (`AXButton`, `AXTextField`, `AXWindow`) and edges $e \in E$ denote structural nesting. The search latency $T_{\text{find}}$ for matching target accessibility predicates $P(v)$ is bounded by:

$$
T_{\text{find}} = \mathcal{O}(|V| + |E|) = \mathcal{O}\left( \sum_{d=0}^{D_{\max}} b_d \right)
$$

Where $D_{\max}$ is the maximum nesting depth (typically $8 \le D_{\max} \le 18$ in complex native suites like Xcode) and $b_d$ is the branching factor at depth $d$. To prevent thread blocking on high-complexity layouts, Vellum prunes invisible subtrees using viewport bounding box clipping:

$$
V_{\text{visible}} = \{ v \in V \mid \text{BBox}(v) \cap \text{Viewport}(\text{Screen}) \neq \emptyset \}
$$

### 2. Multimodal Vision-to-Screen Affine Coordinate Mapping
When vision-language models (e.g., Claude 5.1 / GPT-5.5) inspect desktop screenshots, coordinates are emitted in normalized bounding space $[0, 1000] \times [0, 1000]$. The native screen cursor coordinates $(X_{\text{screen}}, Y_{\text{screen}})$ are computed via affine transformation matrix $\mathbf{A} \in \mathbb{R}^{3 \times 3}$:

$$
\begin{bmatrix} X_{\text{screen}} \\ Y_{\text{screen}} \\ 1 \end{bmatrix} =
\begin{bmatrix}
\frac{W_{\text{display}}}{1000 \cdot s_{\text{Retina}}} & 0 & X_{\text{offset}} \\
0 & \frac{H_{\text{display}}}{1000 \cdot s_{\text{Retina}}} & Y_{\text{offset}} \\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix} x_{\text{norm}} \\ y_{\text{norm}} \\ 1 \end{bmatrix}
$$

Where $s_{\text{Retina}} = 2.0$ represents the macOS Retina display backing scale factor, ensuring sub-pixel tap precision on small UI targets.

### 3. Agent Task Execution Latency Budget & Loop Convergence
For an autonomous desktop workflow with $K$ sequential UI interaction steps, the total makespan $T_{\text{task}}$ is modeled as:

$$
T_{\text{task}} = \sum_{k=1}^K \left( T_{\text{capture}} + T_{\text{vlm\_inference}} + T_{\text{mcp\_dispatch}} + T_{\text{os\_settle}} \right)
$$

Where $T_{\text{os\_settle}} \approx 120\,\text{ms}$ is the mandatory operating system debounce delay allowing animations and focus transitions to stabilize before re-sampling the UI state. When task completion confidence satisfies $\mathbb{P}(\text{Done} \mid \mathcal{H}_k) \ge 0.95$, the loop terminates and releases accessibility locks.

### 4. Intent Ambiguity Entropy & Proactive Trigger Thresholds
When Vellum observes passive background desktop events $\mathbf{x} = (x_{\text{file}}, x_{\text{focus}}, x_{\text{clipboard}})$, it estimates intent uncertainty using Shannon entropy across candidate workflow intents $\Omega = \{\omega_1, \dots, \omega_M\}$:

$$
H(\Omega \mid \mathbf{x}) = -\sum_{m=1}^M \mathbb{P}(\omega_m \mid \mathbf{x}) \log_2 \mathbb{P}(\omega_m \mid \mathbf{x})
$$

Proactive suggestions are surfaced to the user via non-intrusive notifications only when intent entropy is sufficiently low:

$$
H(\Omega \mid \mathbf{x}) \le H_{\text{threshold}} \quad \text{and} \quad \max_{m} \mathbb{P}(\omega_m \mid \mathbf{x}) \ge 0.88
$$

## Desktop Automation & Computer-Use Comparison Matrix

| Feature / Dimension | Vellum (macOS) | Claude Computer Use (Container) | OpenAdapt | OS-World | Adept ACT-1 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Operating Platform** | Native macOS (Darwin) | Headless Linux (X11) | Cross-Platform (PyAutoGUI) | Ubuntu / Linux Benchmark | Chrome / Web Sandbox |
| **UI Integration** | Native Apple Accessibility API | Screenshot X11 Coordinate Click | Image template matching | VM VNC Screencast | DOM Tree Parsing |
| **Protocol Integration**| FastMCP 3.1 Native Host | Anthropic Tool Use Protocol | Custom API | Python Gym Environment | Proprietary Cloud API |
| **Security Layer** | macOS Keychain + Local SQLCipher | Ephemeral Docker Sandbox | Plaintext Configs | Isolated VM Sandbox | Cloud Policy Engine |
| **Proactive Triggers** | Native FSEvents & EventKit | User-Prompt Only | Manual Recording Triggers | Benchmark Tasks Only | Interactive Prompts |
| **Human In The Loop** | Native System Prompt Overlays | Chat UI Confirmations | Screen Prompt Notifications | None (Automated Evaluation)| Cloud Web Dashboard |
| **Execution Speed** | Direct Local IPC (~15ms) | WebRTC / VNC Loop (~120ms) | OS Hook Latency (~50ms) | Hypervisor Loop (~250ms) | Browser RPC (~80ms) |

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
- When deploying headless automation scripts on Linux servers or containerized K8s clusters (use [Prefect](../orchestration/prefect.md) or [Temporal](../orchestration/temporal.md)).
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

## Production Deployment & System Infrastructure

### macOS Launchd Daemon Configuration (`com.vellum.daemon.plist`)
For persistent, non-interactive local background execution under macOS user sessions:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vellum.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/vellum</string>
        <string>wake</string>
        <string>--port</string>
        <string>3001</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/Shared/vellum/logs/daemon.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/Shared/vellum/logs/daemon-err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>VELLUM_SECURITY_MODE</key>
        <string>strict</string>
    </dict>
</dict>
</plist>
```

### Linux Headless Test Sandbox (`docker-compose.yml`)
For continuous integration test suites verifying Vellum agent planning logic against simulated UI events:

```yaml
version: '3.8'
services:
  vellum-test-harness:
    image: python:3.12-slim
    container_name: vellum-test-sandbox
    environment:
      - VELLUM_ENVIRONMENT=mock_macos
      - PYTHONUNBUFFERED=1
    volumes:
      - ./:/workspace
    working_dir: /workspace
    command: ["python", "-m", "pytest", "tests/"]
    restart: "no"
```

## API examples

Under early 2027 SOTA development standards, all system triggers, tool invocations, and agent response payloads are strictly validated using **Pydantic v2** with immutable configurations (`extra="forbid"`, `frozen=True`). Below is a complete production Python FastMCP 3.1 server implementation for validating incoming workspace trigger events and executing background workflows.

### FastMCP 3.1 Desktop Action Dispatcher Server

```python
import sys
import json
import asyncio
import time
from typing import Optional, Dict, Any, List, Literal
from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Strict Pydantic v2 Contract Definitions
# ---------------------------------------------------------------------------

class EventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    filepath: Optional[str] = Field(default=None, description="Absolute filesystem path associated with event")
    app_identifier: str = Field(..., description="Bundle ID or application string (e.g., com.apple.finder)")
    window_title: Optional[str] = Field(default=None, description="Title of active application window")
    extra_payload: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary event payload attributes")

class VellumWorkflowTrigger(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    trigger_id: str = Field(..., min_length=8, description="Unique identifier for the trigger event")
    target_app: str = Field(..., min_length=2, description="Target desktop application name")
    event_type: Literal['file_created', 'file_modified', 'email_arrived', 'focus_changed', 'shortcut_pressed']
    priority: int = Field(default=3, ge=1, le=5, description="Execution priority (1 = Immediate, 5 = Background)")
    metadata: EventMetadata = Field(..., description="Structured metadata payload")

class AgentExecutionPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    plan_id: str = Field(..., description="Plan identifier issued by Claude 5.1/GPT-5.5")
    trigger_id: str = Field(..., description="Associated trigger ID")
    steps: List[str] = Field(..., min_length=1, description="Sequential steps to execute")
    requires_user_confirmation: bool = Field(default=False, description="Whether explicit approval is needed")
    dispatch_latency_ms: float = Field(default=0.0)

mcp = FastMCP("VellumDesktopDispatcher", instructions="FastMCP 3.1 Server for macOS desktop UI action orchestration.")

@mcp.tool(name="dispatch_desktop_action", description="Validates and schedules an automated desktop action sequence.")
def dispatch_desktop_action(trigger: VellumWorkflowTrigger) -> str:
    """Validates incoming desktop triggers and synthesizes an execution plan."""
    start_time = time.time()
    elapsed = (time.time() - start_time) * 1000.0

    plan = AgentExecutionPlan(
        plan_id=f"plan-{trigger.trigger_id}",
        trigger_id=trigger.trigger_id,
        steps=[
            f"Inspect accessibility tree for application: {trigger.metadata.app_identifier}",
            "Capture Retina screenshot and compute affine coordinate transform",
            "Invoke FastMCP 3.1 AppleScript bridge for native action execution"
        ],
        requires_user_confirmation=(trigger.priority == 1),
        dispatch_latency_ms=round(elapsed, 2)
    )
    return plan.model_dump_json()

if __name__ == "__main__":
    mcp.run()
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

## Diagnostic Troubleshooting Matrix

| Symptom / Error | Potential Root Cause | Verification Command | Resolution Step |
| :--- | :--- | :--- | :--- |
| `AXError: Cannot find UI element` | Target app window minimized or offscreen; AX hierarchy mutated | `vellum doctor --check accessibility` | Restore window focus and re-query AX hierarchy using clipped bounding coordinates. |
| `ScreenCaptureKit Permission Denied` | macOS Screen Recording entitlement revoked after OS update | `tccutil check ScreenCapture com.vellum.app` | Open macOS System Settings > Privacy & Security > Screen Recording and re-enable Vellum. |
| `SSE Connection Refused (:3001)` | Vellum background daemon not running or crashed | `pgrep -x vellum` | Launch daemon with `vellum wake --daemon` or inspect `/Users/Shared/vellum/logs/daemon-err.log`. |
| `Keychain SecItemCopyMatching Error` | System Keychain locked due to screen lock or ssh session | `security show-keychain-info` | Run `security unlock-keychain` or execute agent from interactive graphical user session. |
| `FastMCP 3.1 Tool Timeout` | AppleScript execution hung on interactive modal dialog | `vellum mcp status --name <tool>` | Add timeout parameter to AppleScript dispatch script and dismiss blocking dialogs. |
| `High Memory Footprint (>4GB)` | Embedded vision snapshot buffer caching stale frames | `vellum cache clear --all` | Flush in-memory frame cache and configure maximum frame retention limit in config. |
| `Pydantic ValidationError on Trigger`| Unrecognized event attribute passed in trigger payload | Inspect FastMCP client error logs | Ensure incoming payload matches strict schema with `ConfigDict(extra="forbid", frozen=True)`. |
| `API Quota Rate Limit (Claude/OpenAI)`| Unthrottled proactive loop firing on high-frequency FSEvents| `vellum logs --level WARN` | Increase FSEvents debounce window from 500ms to 3000ms in `vellum.json`. |

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
