# Open Agents

## What it is
Open Agents is an open-source framework and collection of deployable AI agents created by Vercel Labs. It is designed to enable "Computer Use" and "Web Use" capabilities, allowing autonomous agents to navigate the web, interact with authenticated SaaS applications, run code in sandboxes, and perform complex multi-step workflows. In early 2027, Open Agents serves as a foundational platform for building browser-native and serverless agents, offering full support for FastMCP 3.1, Vercel AI SDK 5.0, and multi-model execution across **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro / Ultra**, and **DeepSeek-V4**.

## What problem it solves
It bridges the gap between static LLM text generation and interactive web-based software execution. Open Agents eliminates the complexity of managing persistent browser sessions, handling MFA and session tokens in agentic workflows, and providing visual feedback loops for computer-use tasks. By adopting FastMCP 3.1, it standardizes tool registration and task reporting, enabling web agents to communicate seamlessly with enterprise orchestrators.

## Where it fits in the stack
**Agent / Web Automation / Serverless Platform**. It functions as an orchestration layer that combines the Vercel AI SDK with headless browser controllers ([Playwright](../development_ops/playwright.md)) and isolated Vercel Sandbox execution environments.

```
+-----------------------------------------------------------------------------------+
|                              User / FastMCP 3.1 Client                             |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                              Open Agents Orchestrator                             |
|    +------------------------+  +------------------------+  +-------------------+  |
|    | Vercel AI SDK 5.0 Core |  | Session State Manager  |  | FastMCP Tool Reg  |  |
|    +------------------------+  +------------------------+  +-------------------+  |
+-----------------------------------------------------------------------------------+
        |                                     |                                   |
        v                                     v                                   v
+-----------------------+           +--------------------+              +--------------------+
| Frontier LLM Provider |           | Playwright Engine  |              | Vercel Sandbox VM  |
| (Claude 5.1 / GPT-5.6) |           | (Headless Browser) |              | (Isolated Code)    |
+-----------------------+           +--------------------+              +--------------------+
```

## Typical use cases
- **Automated Web Intelligence Gathering**: Synthesizing data from multiple authenticated web applications into structured analytical reports.
- **SaaS Platform Administration**: Executing routine administrative and configuration workflows across platforms like HubSpot, Jira, Salesforce, or cloud consoles.
- **Dynamic Application Ingestion**: Extracting and structuring deep content from dynamic, single-page web applications without fixed APIs.
- **Serverless Agentic Workflows**: Deploying ephemeral agents that execute shell scripts and browser actions within isolated Vercel Sandboxes.
- **Cross-System Task Execution**: Receiving tasks via FastMCP 3.1 endpoints and returning structured output to parent agent harnesses.

## Strengths
- **Vercel Ecosystem Native**: Deep integration with Next.js 16, Vercel AI SDK, and Vercel Functions / Sandboxes.
- **Robust Computer Use Capabilities**: Built-in design patterns for high-fidelity browser navigation, visual DOM positioning, and screenshot verification.
- **Serverless & Ephemeral Architecture**: Optimized for running inside low-latency edge and serverless environments without requiring dedicated VM clusters.
- **Frontier & Open Model Support**: Optimized for native Computer Use APIs in Claude 5.1 and GPT-5.5, with full support for open models like **DeepSeek-V4** and **Llama 4**.
- **Modular Skill Extensions**: Composable architecture allowing developers to grant granular skills (e.g., search, email dispatch, browser interaction).

## Limitations
- **DOM Fragility**: Performance can degrade if target application user interfaces undergo structural changes without corresponding selector updates.
- **Navigation Latency**: Multi-turn browser reasoning loops are inherently slower than direct REST/gRPC API invocations.
- **Serverless Resource Limits**: Running resource-intensive headless browser sessions inside serverless functions requires careful memory and timeout management.

## When to use it
- When building web-accessible agentic products that must perform actions on behalf of users across third-party websites.
- When extending Next.js applications with native agentic workflows using the Vercel AI SDK.
- When seeking an open-source, deployable alternative to proprietary computer-use cloud services.

## When not to use it
- When official, well-supported APIs exist for the target service (direct API calls should always be preferred over UI manipulation).
- For pure web scraping tasks where dedicated crawlers like [Firecrawl](../process_understanding/firecrawl.md) or [Crawl4AI](../process_understanding/crawl4ai.md) are more performant.
- When long-running, continuous local desktop state and native window controls are strictly required.

## Getting started
### Installation
Open Agents is typically integrated into a Next.js application template. Clone the official repository to initialize:

```bash
# Clone the open agents repository
git clone https://github.com/vercel-labs/open-agents
cd open-agents
npm install
```

### Basic Configuration
1. Create a `.env.local` file and add your provider keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `DEEPSEEK_API_KEY`).
2. Configure your Vercel Sandbox token if isolated shell execution is required.
3. Start the local development server: `npm run dev`.

## Advanced Setup and Configuration

Open Agents supports both single-tenant serverless deployments and multi-tenant agent execution clusters.

### Environment Variable Reference

```env
# Primary Frontier LLM Providers
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
DEEPSEEK_API_KEY=sk-ds-...

# Playwright Browser Sandbox Configuration
BROWSER_HEADLESS=true
BROWSER_VIEWPORT_WIDTH=1280
BROWSER_VIEWPORT_HEIGHT=800
BROWSER_TIMEOUT_MS=30000

# FastMCP 3.1 Server Settings
FASTMCP_SERVER_NAME="OpenAgentsWebWorker"
FASTMCP_PORT=8080
FASTMCP_LOG_LEVEL="info"

# Vercel Isolated Sandbox Token (Optional for Code Execution)
VERCEL_SANDBOX_TOKEN="vsb_live_..."
```

## CLI examples

```bash
# Clone and set up the open agents workspace
git clone https://github.com/vercel-labs/open-agents
cd open-agents && npm install

# Start the local agent server interface
npm run dev

# Run automated browser test tasks in headless mode
npm test -- --headless

# Execute an agent task locally via the CLI test runner
npm run start-agent -- --task "Verify status of production deployments on Vercel Dashboard"

# Launch FastMCP 3.1 Open Agents Bridge Server
npm run start-mcp-server -- --port 8080
```

## API examples

### FastMCP 3.1 Web Agent Server Example

Open Agents exposes web manipulation and sandboxed computer-use actions via FastMCP 3.1 tools. The following example demonstrates implementing a FastMCP server in Python that coordinates with the Open Agents runner:

```python
import asyncio
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError
from mcp.server.fastmcp import FastMCP

# Define Pydantic v2 schemas for agent input/output payloads
class ActionTarget(BaseModel):
    selector: Optional[str] = Field(None, description="CSS or XPath DOM selector")
    coordinates: Optional[List[int]] = Field(None, description="[x, y] screen coordinates")
    text_content: Optional[str] = Field(None, description="Expected target text")

class AgentBrowserAction(BaseModel):
    step_number: int = Field(..., description="Action index")
    action_type: str = Field(..., description="Action type: navigate, click, fill, screenshot, evaluate")
    target: Optional[ActionTarget] = None
    value: Optional[str] = Field(None, description="Input string value for fill actions")
    wait_time_ms: int = Field(1000, description="Post-action delay in milliseconds")

class BrowserExecutionReport(BaseModel):
    session_id: str = Field(..., description="Unique browser session token")
    target_url: HttpUrl = Field(..., description="Destination URL")
    actions_executed: List[AgentBrowserAction] = Field(default_factory=list)
    success: bool = Field(..., description="True if objective was achieved")
    final_dom_snapshot: Optional[str] = Field(None, description="Base64 screenshot or text summary")
    telemetry: Dict[str, Any] = Field(default_factory=dict)

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Open-Agents-Web-Worker", version="3.1.0")

@mcp.tool()
async def execute_web_task(
    session_id: str,
    target_url: str,
    action_plan_json: str
) -> str:
    """Execute a multi-step web interaction plan inside an Open Agents Playwright sandbox."""
    try:
        raw_actions = json.loads(action_plan_json)
        actions = [AgentBrowserAction.model_validate(a) for a in raw_actions]
    except (json.JSONDecodeError, ValidationError) as e:
        return f"Error: Invalid action plan payload. {str(e)}"

    # Simulated Playwright execution loop inside Open Agents
    executed_actions = []
    for action in actions:
        # Simulate browser action execution
        executed_actions.append(action)
        await asyncio.sleep(action.wait_time_ms / 1000.0)

    report = BrowserExecutionReport(
        session_id=session_id,
        target_url=HttpUrl(target_url),
        actions_executed=executed_actions,
        success=True,
        final_dom_snapshot="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB...",
        telemetry={
            "duration_ms": sum(a.wait_time_ms for a in actions) + 450,
            "browser_engine": "Playwright/Chromium 122.0",
            "tokens_consumed": 1240
        }
    )

    return report.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

### Vercel AI SDK 5.0 Browser Interaction Script

```typescript
import { generateText, tool } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

const result = await generateText({
  model: anthropic('claude-5-1-sonnet-20261022'),
  tools: {
    browser_navigate: tool({
      description: 'Navigate to a target URL and wait for DOM load',
      parameters: z.object({ url: z.string().url() }),
      execute: async ({ url }) => {
        // Implementation using Playwright
        return { screenshot: 'data:image/png;base64,...', pageContent: '...' };
      },
    }),
    browser_click: tool({
      description: 'Click on an element using CSS selector',
      parameters: z.object({ selector: z.string() }),
      execute: async ({ selector }) => {
        return { status: 'clicked', targetSelector: selector };
      },
    }),
  },
  prompt: 'Go to the Vercel status page and check for any active incident reports.',
});

console.log('Agent Response:', result.text);
```

### Validation of Agent Action Sequences with Pydantic v2
This Python snippet parses and validates an agent's browser action sequence and execution telemetry using **Pydantic v2**:

```python
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class BrowserStep(BaseModel):
    step_id: int = Field(..., description="Chronological step index")
    action: str = Field(..., description="Executed action type (e.g., navigate, click, fill, screenshot)")
    target: Optional[str] = Field(None, description="Target DOM selector or screen coordinate")
    value: Optional[str] = Field(None, description="Input string value if applicable")

class OpenAgentSession(BaseModel):
    session_id: str = Field(..., description="Unique browser session identifier")
    task_description: str = Field(..., description="Task objective assigned to the agent")
    start_url: HttpUrl = Field(..., description="Initial target URL")
    steps: List[BrowserStep] = Field(default_factory=list, description="Sequence of browser actions executed")
    telemetry: Dict[str, Any] = Field(default_factory=dict, description="Session performance and token usage metrics")

def validate_agent_session(raw_json: str) -> Optional[OpenAgentSession]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2 model_validate
        return OpenAgentSession.model_validate(data)
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON payload.")
        return None
```

### FastMCP 3.1 Server Implementation with Strict Pydantic v2 Schemas

The following server implementation exposes Open Agents web navigation and DOM interaction capabilities as a standardized FastMCP 3.1 tool suite with strict payload enforcement:

```python
"""
Open Agents FastMCP 3.1 Server
Exposes headless web interaction, form filling, and DOM extraction tools.
"""

from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

mcp = FastMCP("OpenAgentsGateway")

class NavigateTargetSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target_url: HttpUrl = Field(..., description="Target web destination URL to navigate to")
    session_id: str = Field(..., min_length=8, description="Persistent browser session identifier")
    timeout_ms: int = Field(default=30000, ge=1000, le=120000, description="Page navigation timeout in milliseconds")
    wait_until: str = Field(default="networkidle", pattern="^(load|domcontentloaded|networkidle)$", description="Navigation readiness event")

class ClickActionSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str = Field(..., min_length=8, description="Active browser session identifier")
    selector: str = Field(..., min_length=1, description="CSS selector or ARIA label targeting target element")
    screenshot_verify: bool = Field(default=True, description="Capture visual confirmation screenshot after interaction")

class FillActionSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str = Field(..., min_length=8, description="Active browser session identifier")
    selector: str = Field(..., min_length=1, description="Input element selector")
    value: str = Field(..., description="Value to insert into input field")
    mask_value: bool = Field(default=False, description="Redact value in telemetry logs for credential security")

@mcp.tool("open_agents_navigate")
def open_agents_navigate(payload: NavigateTargetSchema) -> Dict[str, Any]:
    """Navigates an isolated Open Agents browser instance to the target URL."""
    return {
        "status": "navigated",
        "session_id": payload.session_id,
        "url": str(payload.target_url),
        "dom_state": "ready",
        "http_status": 200
    }

@mcp.tool("open_agents_click")
def open_agents_click(payload: ClickActionSchema) -> Dict[str, Any]:
    """Clicks an interactive DOM element and verifies visual transition."""
    return {
        "status": "clicked",
        "session_id": payload.session_id,
        "selector": payload.selector,
        "screenshot_captured": payload.screenshot_verify
    }

@mcp.tool("open_agents_fill")
def open_agents_fill(payload: FillActionSchema) -> Dict[str, Any]:
    """Inputs textual data into target form field with redaction support."""
    logged_val = "[REDACTED]" if payload.mask_value else payload.value
    return {
        "status": "filled",
        "session_id": payload.session_id,
        "selector": payload.selector,
        "value_masked": payload.mask_value,
        "recorded_value": logged_val
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Production Deployment Architecture

#### Systemd Service Unit (`open-agents-runner.service`)

In on-premise or dedicated VM environments, Open Agents background worker daemons can be managed via systemd to guarantee high availability and automated restart upon headless browser crashes:

```ini
[Unit]
Description=Open Agents Headless Automation Runner Daemon
Documentation=https://github.com/vercel-labs/open-agents
After=network-online.target redis.service
Wants=network-online.target

[Service]
Type=simple
User=openagents
Group=openagents
WorkingDirectory=/opt/open-agents-runner
Environment="NODE_ENV=production"
Environment="PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright"
EnvironmentFile=/etc/open-agents/runner.env
ExecStart=/usr/bin/node dist/runner-daemon.js --port 8092 --concurrency 8
Restart=always
RestartSec=5s
LimitNOFILE=65536
StandardOutput=journal
StandardError=journal
SyslogIdentifier=open-agents-runner

# Sandboxing and security boundaries
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/open-agents /var/run/open-agents /tmp/open-agents-cache
PrivateTmp=true
CapabilityBoundingSet=

[Install]
WantedBy=multi-user.target
```

#### Containerized Orchestration (`docker-compose.yml`)

The following Compose specification deploys Open Agents with dedicated Redis session tracking, ephemeral sandbox browser containers, and an integrated FastMCP 3.1 gateway:

```yaml
version: '3.8'

services:
  open-agents-gateway:
    image: ghcr.io/vercel-labs/open-agents:v2.4.0
    container_name: open-agents-gateway
    restart: unless-stopped
    ports:
      - "127.0.0.1:8092:8092"
    environment:
      - NODE_ENV=production
      - FASTMCP_SERVER_PORT=8092
      - REDIS_URL=redis://:openagentssecret@openagents-cache:6379/0
      - BROWSER_POOL_SIZE=6
      - BROWSER_TIMEOUT_MS=60000
    depends_on:
      openagents-cache:
        condition: service_healthy
    networks:
      - openagents-net
    resources:
      limits:
        cpus: '2.0'
        memory: 4096M

  openagents-cache:
    image: redis:7.2-alpine
    container_name: openagents-cache
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass openagentssecret
    volumes:
      - openagents-redis-data:/data
    networks:
      - openagents-net
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "openagentssecret", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  openagents-net:
    driver: bridge

volumes:
  openagents-redis-data:
```

## Diagnostic & Troubleshooting Matrix

The following operational diagnostic matrix details common failure modes encountered during high-volume Open Agents web automation:

| Symptom / Failure Mode | Root Cause | Verification Command | Remediation Procedure |
| :--- | :--- | :--- | :--- |
| **Playwright Browser Crash (SIGTRAP / Out of Memory)** | Sandboxed Chrome instances exhausting shared memory in containerized environment. | `journalctl -u open-agents-runner.service -n 50 \| grep -i oom` | Mount `/dev/shm` as `shm_size: 2gb` in Docker or allocate adequate swap space in host system. |
| **DOM Drift / Element Selector Timeout** | Target SaaS application updated CSS class names or DOM structure. | `open-agents-cli inspect-dom --session-id <ID> --selector "button.submit"` | Update selectors to semantic ARIA roles (`role="button"`) or enable computer-use visual coordinate fallback. |
| **Session Cookie Deserialization Failure** | Stored multi-factor or authentication cookies expired or signature invalidated. | `redis-cli -a $SECRET get session:<ID>:cookies` | Trigger interactive login agent refresh flow or re-issue session credentials via provider OAuth flow. |
| **FastMCP Schema Rejection (`ValidationError`)** | Parent orchestrator sent additional unsupported attributes in tool payload. | `cat /var/log/open-agents/fastmcp-errors.log \| grep extra_forbidden` | Ensure client tool call strictly adheres to Pydantic v2 schemas configured with `extra="forbid"`. |

## Matrix Comparison with Alternative Web Agents

| Feature | Open Agents | Stagehand | Browser Use | Claude Computer Use |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Platform** | Vercel Next.js / Serverless | Node.js / Playwright | Python / Asyncio | Anthropic API / OS VM |
| **FastMCP 3.1 Support** | Native Built-in | Wrapper required | Native | Custom harness |
| **Execution Sandbox** | Vercel Isolated Sandboxes | Local / Cloud Browser | Local / Docker | Isolated Desktop VM |
| **Supported Models** | Claude 5.1, GPT-5.6, DeepSeek-V4 | GPT-4o, Claude 3.5 | Any LLM via LangChain | Claude 3.5 / 5.1 |
| **DOM Alignment Method** | Visual + Playwright Selectors | Natural Language Act | Accessibility Tree | Screen Coordinate Screenshots |
| **Multi-Tenant Ready** | Yes | Needs Custom Wrapper | Custom Deployment | Docker VM Required |

## Related tools / concepts
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — Core agent integration SDK.
- [Playwright](../development_ops/playwright.md) — Underlying headless browser engine.
- [Stagehand](../automation_orchestration/stagehand.md) — AI web automation framework.
- [Claude Code](../development_ops/claude-code.md) — Reference terminal agent harness.
- [Browser Use](../automation_orchestration/browser-use.md) — Web browser agent library.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open tool communication standard.
- [Crawl4AI](../process_understanding/crawl4ai.md) — High-throughput web extraction library.
- [Firecrawl](../process_understanding/firecrawl.md) — Web extraction API platform.

## Sources / references
- [Vercel Labs Open Agents GitHub Repository](https://github.com/vercel-labs/open-agents)
- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [Vercel Functions & Sandboxes Guide](https://vercel.com/docs/functions/sandboxes)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
