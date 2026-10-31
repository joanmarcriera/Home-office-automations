# Skills in Chrome

## What it is
Skills in Chrome is a native browser feature (v145+) that transforms natural language prompts into one-click, reusable agentic tools directly integrated into the Google Chrome interface. Powered by **Gemini 4.0 Ultra** (cloud) and **Gemini 4.0 Nano** (local on-device), it allows users to codify complex instructions into "Agentic Hooks" that can be triggered via the omnibox, side panel, or right-click context menu. As of early **January 2027**, Skills in Chrome deeply integrates with the **FastMCP 3.1** protocol and multi-agent frameworks involving **Claude 5.6**, **GPT-5.6**, and **DeepSeek-V4**.

```
+-----------------------------------------------------------------------------------+
|                           Skills in Chrome Architecture                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ User Trigger: Omnibox / Shortcut / Context Menu / Agentic Hook ]              |
|                                     |                                             |
|                                     v                                             |
|  +-----------------------------------------------------------------------------+  |
|  | Google Chrome Engine (v145+) AI Sidecar Sandbox                           |  |
|  |                                                                             |  |
|  |  +---------------------------+       +------------------------------------+  |  |
|  |  | Active Tab DOM Parser     |       | Agentic Hook Rule Evaluator        |  |  |
|  |  | (Chrome CDP / Tree Walker)|       | (URL Pattern & Context Trigger)    |  |  |
|  |  +---------------------------+       +------------------------------------+  |  |
|  |                \                                   /                        |  |
|  |                 v                                 v                         |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | Model Execution Router                                                |  |  |
|  |  |                                                                       |  |  |
|  |  |  [ Local On-Device: Gemini 4.0 Nano ] <-> [ Cloud: Gemini 4.0 Ultra ]   |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|                                     |                                             |
|                                     v                                             |
|  +-----------------------------------------------------------------------------+  |
|  | FastMCP 3.1 Tool Gateway & External Agent Integration                      |  |
|  +-----------------------------------------------------------------------------+  |
|                                     |                                             |
|                                     v                                             |
|  [ Structured UI Output / Clipboard / Side Panel / Web Page Injections ]          |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It eliminates "prompt fatigue" and the repetitive friction of manually copying and pasting web content into external LLM interface windows. By bridging the gap between static conversational AI and actionable browser workflows, it enables power users, developers, and researchers to treat AI as a set of specialized, context-aware browser extensions without writing complex extension manifest code or managing local API server infrastructure.

In enterprise and compliance scenarios, copying page content into external chat portals frequently leads to unmonitored data loss. Skills in Chrome enforces "Identity-Aware Tool Routing" within Chrome's process isolation boundaries, ensuring web context processing complies with organizational DLP (Data Loss Prevention) policies.

## Where it fits in the stack
**AI Knowledge / Browser Agentic Layer**. It sits at the primary human-computer interaction edge of the web stack, providing a "Sidecar Agent" capability that can inspect active page DOM nodes, summarize multi-tab research content, perform automated form interactions, and dispatch structured tool payloads to local or remote FastMCP 3.1 endpoints using [Gemma 3](../ai_knowledge/local_llms.md) and [Gemini 4.0 Ultra](gemini.md).

## Typical use cases
- **Automated Research Curation**: One-click extraction of key findings, methodology, and limitations from dense technical papers or news articles into structured Markdown tables.
- **Data Structuring & Scraping**: Extracting product specifications, pricing data, or contact directories directly into JSON or CSV clipboard formats.
- **Developer Workflow Automation**: Generating contextual pull request code reviews or drafting bug reports based on open GitHub issues or console log outputs in active browser tabs.
- **Multi-Tab Information Synthesis**: Utilizing "Agentic Search" to compare vendor pricing, documentation, or product features across multiple active browser tabs into a single consolidated matrix.
- **FastMCP 3.1 Local Service Invocation**: Triggering local home automation, calendar entries, or database queries directly from web content triggers.
- **Form Automation & Data Entry**: Intelligently filling repetitive web forms using context extracted from reference spreadsheets or CRM tabs.
- **Accessibility & Translation Assistance**: Converting complex jargon or technical documentation into simplified summaries with voice playback.
- **Enterprise Policy Enforcement**: Automatically checking viewed vendor documentation against internal security compliance rules.

## Strengths
- **Zero-Latency Context Access**: Native browser integration allows the AI sidecar to access the active DOM, selected text, or media elements without manual copying.
- **Agentic Hooks**: Supports automated background triggers based on specific URL patterns (e.g., automatically offering to "Analyze Pull Request" when navigating to `github.com/*/pull/*`).
- **Security & Privacy Sandbox**: Operates within Chrome's isolated process sandbox, utilizing Google's "Identity-Aware Tool Routing" for secure permission checks.
- **Cross-Device Sync**: Configured skills and agentic hooks synchronize across desktop (Windows, macOS, Linux) and mobile (Android) via Google account sync.
- **FastMCP 3.1 Tool Native**: Directly exposes tool definitions to Model Context Protocol clients and servers.
- **On-Device Offline Fallback**: Generates summaries and text formatting via Gemini 4.0 Nano on-device even when internet access is disabled.
- **Declarative Manifest Model**: Allows developers to share browser skills as simple JSON manifests.
- **Zero Code Required**: Non-developers can create complex agentic skills through plain-language prompts in the sidepanel.

## Limitations
- **Ecosystem Lock-in**: Exclusively available on Google Chrome and Chromium-based browsers that adopt the `chrome.ai` extension API specifications.
- **DOM Context Truncation**: Extremely large web documents or multi-megabyte pages may exceed active model context limits, requiring chunking.
- **Sandbox Boundary Constraints**: Cannot execute raw shell commands or interact directly with the local OS filesystem without an external FastMCP local server bridge.

## When to use it
- For high-frequency, repetitive AI tasks performed during active web browsing sessions.
- When you need immediate AI assistance that is aware of the specific "here and now" DOM context of an active web page.
- When building simple agentic browser workflows without wanting to set up external workflow automation engines like [n8n](../../services/n8n.md).
- When operating on local network web interfaces (e.g., router portals, Grafana dashboards) that require quick AI explanation.
- For non-technical team members who benefit from one-click AI shortcuts built into their daily web tools.

## When not to use it
- For heavy repository-wide code edits or terminal command execution (use [Claude Code](everything-claude-code.md) or [Cursor](../development_ops/cursor.md)).
- When working with strict air-gapped sensitive data that prohibits cloud telemetry (use [Ollama](../../services/ollama.md) or [Local LLMs](local_llms.md) with local web scrapers).
- For complex headless web automation jobs requiring unattended background execution (use [Playwright](../development_ops/playwright.md) or [Browser Use](../automation_orchestration/browser-use.md)).

## Systemd Service Configuration
When running an unattended headless Chrome instance acting as an automated skills execution bridge on Linux application servers, systemd manages the background process:

```ini
[Unit]
Description=Chrome Skills Headless CDP Bridge Service
After=network.target xvfb.service
Wants=xvfb.service

[Service]
Type=simple
User=chrome-runner
Group=chrome-runner
WorkingDirectory=/opt/chrome-skills-bridge
Environment="DISPLAY=:99"
Environment="CHROME_BIN=/usr/bin/google-chrome-stable"
Environment="CDP_PORT=9222"
Environment="FASTMCP_PORT=8765"
ExecStart=/usr/bin/google-chrome-stable \
  --headless=new \
  --remote-debugging-port=9222 \
  --remote-debugging-address=0.0.0.0 \
  --disable-gpu \
  --no-sandbox \
  --enable-features=ChromeAISkills,GeminiNanoOnDevice \
  --user-data-dir=/opt/chrome-skills-bridge/profile
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Docker Compose Multi-Container Setup
Deploying a containerized headless Chrome CDP instance alongside a FastMCP 3.1 gateway bridge and Redis context cache:

```yaml
version: "3.8"

services:
  chrome-headless:
    image: chromedp/headless-shell:latest
    container_name: chrome-skills-headless
    restart: unless-stopped
    ports:
      - "9222:9222"
    environment:
      - CHROME_OPTS=--headless --disable-gpu --no-sandbox --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0
    shm_size: 2gb
    networks:
      - skills-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9222/json/version"]
      interval: 10s
      timeout: 5s
      retries: 5

  fastmcp-bridge:
    image: python:3.11-slim
    container_name: fastmcp-chrome-bridge
    restart: unless-stopped
    working_dir: /app
    volumes:
      - ./bridge:/app
    environment:
      - CDP_ENDPOINT=http://chrome-headless:9222
      - REDIS_URL=redis://redis-skills:6379/0
      - MCP_PORT=8765
    ports:
      - "8765:8765"
    command: >
      sh -c "pip install mcp[cli] pydantic httpx redis &&
             python3 -m bridge.server"
    depends_on:
      chrome-headless:
        condition: service_healthy
      redis-skills:
        condition: service_healthy
    networks:
      - skills-net

  redis-skills:
    image: redis:7-alpine
    container_name: redis-skills-cache
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--maxmemory", "512mb", "--maxmemory-policy", "allkeys-lru"]
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - skills-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  skills-net:
    driver: bridge

volumes:
  redis_data:
```

## Getting started
> [!IMPORTANT]
> Requires Google Chrome v145+ with Gemini features enabled in settings.

### Local Setup & Skill Creation
1. **Enable AI Features**: Navigate to `chrome://settings/ai` and ensure "Gemini Side Panel" and "Agentic Hooks" are toggled ON.
2. **Open the AI Side Panel**: Click the Gemini icon in the top-right corner of Chrome or press `Cmd+K` (macOS) / `Ctrl+K` (Windows).
3. **Create Your First Skill**:
   - Enter a prompt in the sidepanel chat (e.g., "Extract all technical specifications into a markdown table").
   - Click **Save as Skill**.
   - Assign a name (`Spec Extractor`), shortcut (`/specs`), and target URL trigger (`https://*/*`).

## CLI examples
Developers can query and trigger saved skills or configure agentic hooks via the Chrome DevTools Protocol (CDP):

```bash
# Example: Triggering a Chrome Skill via CDP (Headless Debug Instance)
curl -X POST http://localhost:9222/json/rpc \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "method": "AI.executeSkill",
    "params": { "skillId": "spec-extractor", "tabId": 101 }
  }'

# List available installed AI skills via CDP
curl -X POST http://localhost:9222/json/rpc \
  -H "Content-Type: application/json" \
  -d '{ "id": 2, "method": "AI.listSkills" }'

# Set an agentic hook for specific URL pattern
curl -X POST http://localhost:9222/json/rpc \
  -H "Content-Type: application/json" \
  -d '{
    "id": 3,
    "method": "AI.setHook",
    "params": { "pattern": "https://github.com/*/pull/*", "skillId": "pr-review" }
  }'

# Query active Gemini 4.0 Nano local model status
curl -X POST http://localhost:9222/json/rpc \
  -H "Content-Type: application/json" \
  -d '{ "id": 4, "method": "AI.getOnDeviceModelStatus" }'

# Export configured skills manifest to local file
curl -X POST http://localhost:9222/json/rpc \
  -H "Content-Type: application/json" \
  -d '{ "id": 5, "method": "AI.exportSkillsManifest" }' > skills_backup.json
```

## API examples

### FastMCP 3.1 Skill Manifest Validator (Strict Pydantic v2)
Extensions and FastMCP bridge servers can parse and validate Chrome skill manifests using **Pydantic v2** with strict configuration (`extra="forbid"`):

```python
import json
from typing import Literal, Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_validator
from mcp.server.fastmcp import FastMCP

# Define strict Pydantic v2 schemas for Chrome Skill manifests
class AgenticHookTrigger(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url_pattern: str = Field(..., description="Glob or regex matching target web URLs")
    trigger_event: Literal["page_load", "selection", "manual_shortcut"] = Field("manual_shortcut")
    debounce_ms: int = Field(default=300, ge=50, le=5000, description="Debounce delay in milliseconds")

class ChromeSkillManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_id: str = Field(..., pattern=r"^[a-z0-9\-]+$")
    name: str = Field(..., min_length=3, max_length=60)
    shortcut: str = Field(..., pattern=r"^/[a-zA-Z0-9]+$")
    context_mode: Literal["active_tab_dom", "selected_text", "all_open_tabs"] = "active_tab_dom"
    target_hook: AgenticHookTrigger
    prompt_template: str = Field(..., min_length=20)
    output_format: Literal["markdown", "json", "plain_text"] = "markdown"
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    max_tokens: int = Field(default=2048, ge=64, le=16384)

    @field_validator("prompt_template")
    @classmethod
    def validate_prompt_variables(cls, v: str) -> str:
        if "{{page_content}}" not in v and "{{selection}}" not in v:
            raise ValueError("Prompt template must include at least one context placeholder: {{page_content}} or {{selection}}")
        return v

# FastMCP 3.1 Server for Chrome Skill Management
mcp = FastMCP("chrome-skills-bridge")

@mcp.tool()
async def register_chrome_skill(manifest_json: str) -> str:
    """Validates and registers a new Chrome agentic skill manifest."""
    manifest = ChromeSkillManifest.model_validate_json(manifest_json)

    # Process manifest registration logic
    return json.dumps({
        "status": "registered",
        "skill_id": manifest.skill_id,
        "shortcut": manifest.shortcut,
        "hook_pattern": manifest.target_hook.url_pattern,
        "context_mode": manifest.context_mode
    })

@mcp.tool()
async def execute_remote_skill(skill_id: str, tab_id: int, context_payload: str) -> str:
    """Invokes a Chrome skill via headless CDP execution."""
    return json.dumps({
        "status": "executed",
        "skill_id": skill_id,
        "tab_id": tab_id,
        "result_length": len(context_payload)
    })

if __name__ == "__main__":
    # Test manifest validation
    sample_manifest = {
        "skill_id": "pr-code-reviewer",
        "name": "GitHub PR Code Auditor",
        "shortcut": "/prreview",
        "context_mode": "active_tab_dom",
        "target_hook": {
            "url_pattern": "https://github.com/*/pull/*",
            "trigger_event": "page_load",
            "debounce_ms": 500
        },
        "prompt_template": "Audit the code diff in {{page_content}} for security vulnerabilities.",
        "output_format": "markdown",
        "temperature": 0.1,
        "max_tokens": 4096
    }

    validated = ChromeSkillManifest.model_validate(sample_manifest)
    print(f"Validated skill: {validated.name} (Shortcut: {validated.shortcut})")
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Failure Mode | Probable Root Cause | Verification Command | Resolution Strategy |
| :--- | :--- | :--- | :--- |
| **Agentic Hooks Fail to Trigger** | Malformed URL pattern or missing scheme wildcard (e.g. `github.com/*` instead of `https://github.com/*`) | Inspect hook trigger table via CDP `curl http://localhost:9222/json/rpc -d '{"id":1,"method":"AI.listHooks"}'` | Always include explicit scheme matching (`https://*` or `http://*`) in the skill manifest URL pattern triggers. |
| **CDP Port Unreachable (`Connection Refused`)** | Headless Chrome crashed due to shared memory exhaustion (`/dev/shm`) | `docker logs chrome-skills-headless` or `journalctl -u chrome-skills-bridge -n 50` | Increase container shared memory via `shm_size: 2gb` in docker-compose.yml or launch with `--disable-dev-shm-usage`. |
| **On-Device Gemini Nano Model Unload** | Excessive active tabs causing Chrome Memory Saver to purge local weights | Check on-device status: `curl http://localhost:9222/json/rpc -d '{"id":2,"method":"AI.getOnDeviceModelStatus"}'` | Pin model weights in settings, enable persistent memory allocation, or configure automatic fallback to cloud Gemini 4.0 Ultra. |
| **DOM Context Truncation Error** | Web page DOM exceeds max context token window (>32k tokens) | Check CDP response status code `413 ContextExceeded` | Switch `context_mode` to `selected_text` or implement client-side DOM pruning via tree walker script before AI ingestion. |
| **FastMCP Schema Validation Error** | Manifest JSON contains unexpected fields forbidden by strict Pydantic model | Run local manifest validation `python3 -m bridge.validator --file manifest.json` | Ensure manifest adheres to `extra="forbid"` schema, removing unrecognized third-party metadata properties. |
| **CORS / Cross-Origin Isolation Blocks** | Chrome security sandbox blocking FastMCP bridge WebSocket connection | Inspect browser DevTools Console for `SecurityError: Content Security Policy directive violated` | Add local bridge host (`localhost:8765`) to Chrome extension `externally_connectable` permissions manifest. |

## Related tools / concepts
- [Google Search](google-search.md) — Grounding platform for web search capabilities.
- [Gemini](gemini.md) — The frontier multimodal model powering Skills in Chrome.
- [Gemma 3](../ai_knowledge/local_llms.md) — Open-weights local language model family.
- [Browser Use](../automation_orchestration/browser-use.md) — Agentic browser automation framework.
- [Stagehand](../automation_orchestration/stagehand.md) — AI-first web scraping and interaction engine.
- [FastMCP](../automation_orchestration/mcp.md) — Model Context Protocol tool discovery framework.
- [n8n](../../services/n8n.md) — Self-hosted workflow automation platform.

## Sources / references
- [Google I/O: Powering the Agentic Web in Chrome](https://developer.chrome.com/blog/chrome-at-io26)
- [Turn AI Prompts into One-Click Tools in Chrome](https://blog.google/products-and-platforms/products/chrome/skills-in-chrome/)
- [Chrome Developer AI Documentation](https://developer.chrome.com/docs/ai/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
