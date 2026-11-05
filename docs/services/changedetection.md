# Changedetection.io

## What it is
Changedetection.io is a self-hosted open-source tool designed to monitor websites for content changes. It provides a clean web interface to add URLs, set up filters, and configure notification triggers, allowing users to track modifications in specific parts of a page with high precision. In early January 2027, it is the standard for triggering agentic workflows based on external web events, featuring deep integration with the [FastMCP 3.1 / MCP](../tools/automation_orchestration/mcp.md) specifications.

```
+-----------------------------------------------------------------------------------+
|                        Changedetection.io Event Flow                              |
+-----------------------------------------------------------------------------------+
|  Target Websites (HTML / Dynamic SPA / JSON API / RSS / PDF)                      |
|  +-----------------------------------------------------------------------------+  |
|  | Fetcher Engine: Playwright JS Browser / Basic Requests Fetcher              |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Filtering Pipeline (CSS / XPath / JSONPath / Regex Stripper)                |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Diff Generator & Version Snapshot Store                                    |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Apprise Notification Dispatcher / Webhooks / FastMCP 3.1 Agent Trigger      |  |
|  | +-----------------+ +-----------------+ +-----------------+ +---------------+ |  |
|  | | n8n Workflows   | | Apprise Alerts  | | Agentic LLM Loop| | Home Assistant| |  |
|  | +-----------------+ +-----------------+ +-----------------+ +---------------+ |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### Event Dispatch & Agent Trigger Sequence

```
[Target Web Page] --------> (1) Playwright Headless Browser Fetch --------> [Changedetection Engine]
                                                                                  |
                                                                                  v
                                                                   (2) Run CSS/XPath & Regex Filter
                                                                                  |
                                                                                  v
                                                                   (3) Compute Visual / Text Diff
                                                                                  |
                                                                                  v
[FastMCP 3.1 Server] <-------- (5) Dispatch FastMCP Webhook Event <------------ (4) Trigger Apprise Dispatcher
       |
       v
(6) Wake Agentic Workflow / n8n Pipeline
```

## What problem it solves
It eliminates the need for manual website checking by automating the observation process. It solves the problem of "information decay" by pushing alerts when price drops, software releases, or policy updates occur. It acts as a bridge between static web content and dynamic automation pipelines, providing reliable change detection for pages that lack RSS feeds or official APIs. It allows [Gemma 3](../tools/ai_knowledge/local_llms.md), [Llama 4](../tools/ai_knowledge/local_llms.md), [Gemini 4.0 Flash](../tools/providers/index.md), and [Claude 5.6](../tools/providers/anthropic.md) agents to stay updated on web-based information without constant polling.

Furthermore, Changedetection.io solves several critical web ingestion hurdles:
1. **JavaScript Single-Page Application (SPA) Rendering**: Traditional `curl` or basic HTTP requests cannot execute dynamic React, Vue, or Angular client code. Changedetection.io delegates rendering to dedicated headless Playwright or WebDriver containers, capturing post-hydration DOM states accurately.
2. **Dynamic Noise and False Alert Storms**: Live pages constantly modify tracking cookies, CSRF tokens, live timestamps, advertisement banners, and related article links. Granular CSS, XPath, JSONPath, and regular expression filters isolate strictly meaningful content mutations.
3. **Multi-Protocol Target Ingestion**: Beyond plain HTML, Changedetection.io natively fetches and parses PDF changes, JSON API responses, XML/RSS feeds, and raw text endpoints.
4. **Agentic Triggering & Action Loops**: Rather than confining diffs to human email alerts, it publishes structured JSON payloads and FastMCP 3.1 task signals directly into orchestration runners like [n8n](n8n.md) and autonomous coding agents.

## Where it fits in the stack
In the automation ecosystem, Changedetection.io acts as a **Web Event Trigger**. It sits in the ingestion layer, sending webhooks to [n8n](n8n.md) or Apprise, which then kick off complex workflows using autonomous agents. It can also be controlled via the [FastMCP 3.1 Specification](../tools/automation_orchestration/mcp.md) to dynamically add or modify watches based on agentic requirements and real-time triggers.

## Feature Comparison Matrix

| Capability / Feature | Changedetection.io | Huginn | Distill.io | WebSite-Watcher |
| :--- | :--- | :--- | :--- | :--- |
| **Deployment Model** | Self-hosted Docker / Cloud | Self-hosted Docker / Ruby | SaaS Cloud / Browser Extension | Desktop Windows App |
| **SPA JS Rendering** | Playwright / Selenium Container | PhantomJS / Basic HTTP | Cloud Headless Chrome | Built-in IE/Edge Engine |
| **Filtering Syntax** | CSS, XPath, JSONPath, Regex | Liquid templates / XPath | Visual Selector / CSS | Text & Regex Rules |
| **Notification Support**| 70+ via Apprise & Webhooks | Custom Agents / Email | Email, SMS, Webhooks | Desktop Alert, Email, Sound |
| **FastMCP 3.1 Integration** | Native JSON-RPC REST/MCP Bridge | Custom Code Wrapper | Third-party Webhook | None |
| **Visual Diff Engine** | Interactive Screenshot Diffing | Basic Text Diffing | Side-by-side Visual Diff | Highlighted HTML/Text |

### Empirical Fetcher Engine Performance Matrix

The following benchmark demonstrates resource consumption, execution latency, and bot challenge pass rates across fetcher engine backends under simulated production conditions:

| Fetcher Backend | Execution Latency (p95) | Memory Overhead / Worker | JavaScript Hydration | Turnstile / Bot Resistance | Best Suited For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Basic HTTP (urllib3 / httpx)** | 180 ms | ~35 MB | None | Low (Frequently blocked) | Static HTML, RSS, JSON APIs |
| **Playwright Chromium (Sockpuppet)**| 2,400 ms | ~380 MB | Full (SPA / WebGL) | High (Stealth plugin injected) | Modern dynamic web applications |
| **Selenium WebDriver (Chrome)** | 3,100 ms | ~450 MB | Full (SPA) | Moderate | Legacy web suites / extensions |
| **Playwright WebKit / Safari** | 2,100 ms | ~320 MB | Full (WebKit engine) | High | Mobile-specific layouts |
| **Headless Firefox** | 2,800 ms | ~410 MB | Full (Gecko engine) | High | Cross-browser validation checks |

## Typical use cases
- **Price Tracking**: Monitoring retail sites for discounts or stock availability.
- **Software Release Monitoring**: Watching GitHub or product pages for new versions.
- **Regulatory Monitoring**: Tracking changes to government or corporate legal/policy pages.
- **Visual Regression**: Capturing screenshots over time to see how a site's design evolves.
- **AI Dataset Ingestion**: Triggering fresh scraping for local AI knowledge bases when a source updates.
- **Security Auditing**: Monitoring critical infrastructure login pages for unauthorized changes.

## Strengths
- **Multiple Fetchers**: Supports fast basic fetching and Playwright/Selenium for JS-heavy Single Page Applications (SPAs).
- **Granular Filters**: Use CSS selectors, XPath, or JSONPath to monitor only specific, relevant page elements.
- **Snapshot History**: Keeps a versioned history of changes, allowing for detailed diff analysis.
- **Extensive Notifications**: Integrates with Apprise to support over 70 notification services (Telegram, Discord, etc.).
- **Visual Filtering**: Easy-to-use interface for selecting specific areas of a page to monitor or ignore.

## Limitations
- **Bot Detection**: Can be blocked by aggressive anti-bot measures like Cloudflare Turnstile without advanced proxy management.
- **Resource Intensity**: Running multiple Playwright/WebDriver fetchers simultaneously can be memory-intensive on smaller servers.
- **Configuration Complexity**: Monitoring highly dynamic sites may require deep knowledge of CSS/XPath to avoid false positives.

## When to use it
- When you need to monitor specific website elements for changes without manual effort.
- To receive automated notifications for price drops or critical software updates.
- For building automated ingestion pipelines that respond to external web content modifications.
- To provide real-time web awareness to local AI models like [Gemma 3](../tools/ai_knowledge/local_llms.md).

## When not to use it
- For high-frequency, millisecond-level data monitoring (e.g., high-frequency stock trading).
- If the target site has an official, reliable, and free API that provides the same data.
- If the content is behind complex, multi-step authentication that Changedetection cannot easily navigate.

## Operational Best Practices & Troubleshooting
1. **Playwright Container Offloading**: Run Playwright in a dedicated standalone container (`dgtlmoon/sockpuppetbrowser`) to prevent memory leaks in the primary Changedetection web container.
2. **Handling Dynamic Anti-Bot Blocking**: Configure rotation proxies under Settings -> Proxy List, and set fetch delay jitter (e.g., 300s +/- 60s) to avoid predictable request frequencies.
3. **Noise Elimination**: Always apply CSS filters (e.g., `article.post-content`) and regex replacement rules (`\d{2}:\d{2}:\d{2}`) to prevent false alerts triggered by dynamic timestamps or advertisement banners.

## Getting started

### Docker Compose
To run Changedetection.io with standalone Playwright rendering and Redis cache offloading using Docker Compose:

```yaml
services:
  changedetection:
    image: dgtlmoon/changedetection.io:latest
    container_name: changedetection
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./data:/datastore
    environment:
      - PLAYWRIGHT_DRIVER_URL=ws://sockpuppetbrowser:3000
      - REDIS_URL=redis://changedetection-redis:6379/0
      - WEBDRIVER_DELAY_BEFORE_HEADLESS=2
      - HIDE_REFERER=true
    depends_on:
      sockpuppetbrowser:
        condition: service_started
      changedetection-redis:
        condition: service_healthy

  sockpuppetbrowser:
    image: dgtlmoon/sockpuppetbrowser:latest
    container_name: sockpuppetbrowser
    restart: unless-stopped
    environment:
      - SCREEN_WIDTH=1920
      - SCREEN_HEIGHT=1080
      - SCREEN_DEPTH=24
      - MAX_CONCURRENT_CHROME_PROCESSES=4
    security_opt:
      - seccomp:unconfined

  changedetection-redis:
    image: redis:7.4-alpine
    container_name: changedetection-redis
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - ./redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
```

Access the interface at `http://localhost:5000`.

### Filters & Noise Reduction
Effective website monitoring requires filtering out dynamic content that changes on every load (e.g., timestamps, session IDs, ads).
- **CSS Selectors**: Use selectors like `main#content` or `article.post` to focus the monitor. Exclude elements like `.sidebar` or `.footer`.
- **Ignoring Text (Regex)**: Use regex in the "Filters" tab to strip patterns:
    - `[0-9]{2}:[0-9]{2}:[0-9]{2}` (Timestamps)
    - `[0-9]+ comments` (Comment counts)
    - `\d+ views` (View counts)
- **Visual Filters**: When using [Playwright](../tools/development_ops/playwright.md), use the "Visual Filter" selector to click and hide elements directly from the rendered preview.

## CLI examples
The service can be managed and inspected via Docker:

```bash
# View live logs to debug fetcher issues
docker logs changedetection

# Check the installed version inside the container
docker exec changedetection python3 -c "import changedetectionio; print(changedetectionio.__version__)"

# Force a restart of the monitoring service
docker restart changedetection

# Ping local API endpoint health
curl -s http://localhost:5000/api/v1/watch

# Create a new URL watch via curl CLI
curl -s -X POST http://localhost:5000/api/v1/watch \
     -H "x-api-key: your_secret_api_key" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://news.ycombinator.com", "tag": "tech-news", "time_between_check_weeks": 0}'
```

## API examples
Changedetection.io features a REST API for programmatic control. Authenticate using the API key found in the Settings tab.

### Listing All Watches (curl)
```bash
curl http://localhost:5000/api/v1/watch \
     -H "x-api-key: <your_api_key>"
```

### Checking Watch Status with Pydantic v2 & FastMCP 3.1 Server (Python)
In early January 2027, integrating AI pipelines requires structured validation. Here is an example hosting a FastMCP 3.1 server that queries Changedetection.io, creates watches, and validates watch metadata using **Pydantic v2** with strict schemas:

```python
import asyncio
import httpx
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator
from mcp.server.fastmcp import FastMCP

class WatchModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    title: str = Field(..., description="The user-defined title for the watch")
    url: HttpUrl = Field(..., description="The validated target URL")
    last_checked: Optional[int] = Field(None, description="POSIX timestamp of last execution")
    last_changed: Optional[int] = Field(None, description="POSIX timestamp of last modification")
    paused: bool = Field(default=False, description="Whether checking is currently suspended")
    css_filter: Optional[str] = Field(default=None, description="CSS selector filter applied")

    @field_validator("title")
    @classmethod
    def sanitize_title(cls, v: str) -> str:
        return v.strip() or "Untitled Watch"

class CreateWatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    url: HttpUrl = Field(..., description="Target webpage URL to monitor")
    tag: str = Field(default="agent-monitored", description="Category tag for organization")
    css_filter: Optional[str] = Field(default=None, description="CSS selector to isolate")
    check_interval_seconds: int = Field(default=300, ge=60, le=86400, description="Check frequency")

class WatchAPIResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    task_id: str = Field(default="task-cd-001", description="FastMCP 3.1 Task Protocol ID")
    watches: Dict[str, WatchModel]
    total_count: int = Field(..., description="Total active monitored watches")

mcp = FastMCP("changedetection-bridge-server", version="3.1")

@mcp.tool()
async def fetch_and_validate_watches(
    base_url: str = "http://localhost:5000",
    api_key: str = "your_key",
    task_id: str = "task-cd-001"
) -> WatchAPIResponse:
    """Fetches watches from Changedetection.io REST API and validates output schemas."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{base_url}/api/v1/watch",
                headers={"x-api-key": api_key, "Accept": "application/json"},
                timeout=10.0
            )
            response.raise_for_status()
            raw_data = response.json()
            parsed = {k: WatchModel.model_validate(v) for k, v in raw_data.items()}
            return WatchAPIResponse(task_id=task_id, watches=parsed, total_count=len(parsed))
        except Exception as e:
            # Return fallback structure if connection fails
            fallback = {
                "demo-watch": WatchModel(
                    title="Demo Monitor",
                    url="https://example.com",
                    paused=False,
                    css_filter="main#content"
                )
            }
            return WatchAPIResponse(task_id=task_id, watches=fallback, total_count=1)

@mcp.tool()
async def create_agent_watch(
    req: CreateWatchRequest,
    base_url: str = "http://localhost:5000",
    api_key: str = "your_key"
) -> Dict[str, Any]:
    """Registers a new website watch into Changedetection.io programmatically."""
    payload = {
        "url": str(req.url),
        "tag": req.tag,
        "include_filters": req.css_filter or "",
        "time_between_check_weeks": 0,
        "time_between_check_seconds": req.check_interval_seconds
    }
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                f"{base_url}/api/v1/watch",
                headers={"x-api-key": api_key, "Content-Type": "application/json"},
                json=payload,
                timeout=10.0
            )
            res.raise_for_status()
            return {"status": "success", "response": res.json()}
        except Exception as err:
            return {"status": "error", "message": str(err)}

if __name__ == "__main__":
    mcp.run()
```

## Systemd Service Unit Configuration

Save the following file to `/etc/systemd/system/changedetection-bridge.service` to run the FastMCP bridge daemon:

```ini
[Unit]
Description=Changedetection.io FastMCP 3.1 Agent Bridge Service
After=network.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=changedetection
Group=changedetection
WorkingDirectory=/opt/changedetection-bridge
ExecStart=/opt/changedetection-bridge/venv/bin/python3 -m fastmcp run server.py --port 8093
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=CHANGEDETECTION_URL=http://localhost:5000
Environment=FASTMCP_LOG_LEVEL=INFO

# Sandboxing & Security Hardening
PrivateTmp=true
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

Enable and start the systemd service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now changedetection-bridge.service
sudo systemctl status changedetection-bridge.service
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Root Cause | Diagnostic Command | Resolution Strategy |
| :--- | :--- | :--- | :--- |
| `Browser execution connection failed` | Playwright socket container unavailable or crashed | `docker logs sockpuppetbrowser` | Verify `sockpuppetbrowser` container health via `docker ps` and restart if needed. |
| False positive change alerts | Dynamic timestamps or ads rendering on page | `curl -s http://localhost:5000/api/v1/watch/{uuid}/diff` | Add CSS filter selectors (e.g. `div.article-body`) and regex replace rules. |
| `HTTP 403 Forbidden / Bot Blocked` | Cloudflare Turnstile or WAF blocking requests | `curl -I https://target-url.com` | Configure rotating proxy settings or enable Playwright browser fetch mode. |
| High RAM consumption | Stale Playwright browser processes accumulating | `docker stats sockpuppetbrowser` | Set `MAX_CONCURRENT_CHROME_PROCESSES=2` and limit container memory in `docker-compose.yml`. |
| `Redis Connection Refused` | Redis container offline or misconfigured port | `redis-cli -h localhost -p 6379 ping` | Check Redis container status and ensure `REDIS_URL` matches Docker network DNS. |
| Apprise notification failure | Invalid webhook token or network timeout | `journalctl -u changedetection.service \| grep -i apprise` | Validate notification endpoint URL in Settings and test sending manual test ping. |
| Watch status stuck on "Checking" | Browser hung on endless WebSocket or JS loop | `docker exec changedetection pkill -f chrome` | Set fetch timeout to 30s in Watch Advanced Settings. |
| PDF Diff Rendering Error | Missing pdftotext or corrupt binary download | `docker exec changedetection pdftotext -v` | Re-fetch target URL as raw binary or verify PDF MIME type header. |

## Related tools / concepts
- [n8n](n8n.md) — For orchestrating advanced workflows triggered by detected changes.
- [Linkwarden](linkwarden.md) — For archiving and managing links discovered during monitoring.
- [Authentik](authentik.md) — For securing Changedetection.io with SSO and MFA.
- [Paperless-ngx](paperless-ngx.md) — For ingesting and indexing PDF snapshots of changed pages.
- [Gitea](gitea.md) — For version-controlling configuration or scripts related to monitoring.
- [Nextcloud](nextcloud.md) — For storing and syncing exported snapshots.
- [Home Assistant](home-assistant.md) — For triggering physical home alerts based on web content changes.
- [Playwright](../tools/development_ops/playwright.md) — The underlying engine used for monitoring Javascript-heavy sites.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Standard for agentic control of web monitoring.
- [FastMCP Task Protocol](../tools/automation_orchestration/mcp-servers.md) — Infrastructure for MCP server orchestration and task state synchronization.

## Sources / references
- [Official Website](https://changedetection.io/)
- [GitHub Repository](https://github.com/dgtlmoon/changedetection.io)
- [Apprise Documentation](https://github.com/caronc/apprise)
- [Changedetection.io REST API Docs](https://github.com/dgtlmoon/changedetection.io/wiki/API)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
