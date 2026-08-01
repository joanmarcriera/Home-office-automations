# qBittorrent Automation

## What it is
qBittorrent Automation encompasses the workflows, scripts, and integrations used to manage the lifecycle of torrent downloads autonomously. In late October / November 2026, it leverages the **v5.4** Web API, Model Context Protocol (MCP 3.1) via FastMCP, and frontier model reasoning (Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, Qwen 3.6) to allow AI agents to orchestrate content acquisition, categorization, and library maintenance with unprecedented precision.

## What problem it solves
Manual torrent management is time-consuming and prone to organizational chaos. qBittorrent Automation solves the "acquisition overhead" by automatically ingesting content from RSS feeds, categorizing downloads based on content type, renaming files for media servers, and enforcing seeding rules to maintain private tracker ratios without human intervention.

## Where it fits in the stack
**Category**: Service / Media / Automation. It sits at the **intake orchestration layer**, bridging content discovery (via [SearXNG](searXNG.md) or RSS) with media consumption ([Plex](plex.md), [Jellyfin](jellyfin.md)).

## Typical use cases
- **Agentic Content Retrieval**: Asking an AI agent (Claude 5.1) to "Find and download the latest Debian ISO," which it executes via the qBittorrent API and MCP 3.1 Task Protocol.
- **Automated Library Maintenance**: Using [n8n](n8n.md) to move completed downloads to specific folders and trigger a media library scan.
- **Ratio Management**: Automatically pausing or deleting torrents once they reach a predefined seeding ratio or time limit.
- **Real-Time Notifications**: Sending alerts to [Element](element.md) or [Synapse](synapse.md) when a high-priority download completes.
- **Dynamic Bandwidth Scaling**: Automatically adjusting download speeds based on home network occupancy or [Speedtest](speedtest.md) results.

## Strengths
- **Native MCP 3.1 Support**: Allows autonomous agents using Claude 5.1 or GPT-5.5 to securely query and manipulate the download queue using standardized task and tool definitions.
- **Frontier Model Integration**: Enables intelligent categorization and "self-healing" of stalled downloads through advanced causal reasoning from Qwen 3.6 or Gemma 3.
- **Comprehensive Web API**: Version v5.4 provides highly granular control over every aspect of the client, from peer management to transfer settings.
- **Event-Driven Triggers**: Native support for running external programs on torrent completion.
- **Category-Level Logic**: v5.4+ allows for different automation rules (seeding, pathing) based on assigned categories.
- **Extensive Tooling**: Large ecosystem of Python wrappers (`qbittorrent-api`) and automation nodes (n8n, Node-RED).
- **Cost-Effective**: Open source (GPL-2.0) and completely free to self-host.

## Limitations
- **Security Complexity**: Exposing the Web API for automation requires robust authentication (e.g., via [Authentik](authentik.md)).
- **Configuration Overhead**: Setting up complex "If-This-Then-That" workflows can require significant initial effort.
- **Path Mapping**: Ensuring Docker container paths align across multiple services (qBittorrent, n8n, Plex) is a common point of friction.

## When to use it
- When you want a "set-and-forget" media and data acquisition pipeline.
- To manage complex seeding requirements for multiple private trackers simultaneously.
- When integrating content acquisition into a larger AI-driven homelab orchestration.
- To maintain a highly organized media library without manual file moving.

## When not to use it
- If you only download occasional files manually and don't mind manual organization.
- In environments where the security of the Web API cannot be guaranteed.

## Getting started

### Prerequisites
1. A running [qBittorrent](qbittorrent.md) instance with Web UI enabled.
2. An automation engine like [n8n](n8n.md) or a Python environment.

### Hello World (n8n Webhook)
1. In qBittorrent, go to **Options > Downloads > Run external program on torrent completion**.
2. Set the command to trigger an n8n webhook:
   `curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"%N\", \"hash\": \"%I\"}" http://n8n:5678/webhook/torrent-done`
3. In n8n, create a workflow that sends a notification when this webhook is called.

## CLI examples
Automate qBittorrent via `curl` and the Web API.

```bash
# Login and save session SID
curl -i -d "username=admin&password=your_password" http://localhost:8080/api/v2/auth/login

# Add a torrent with a specific category
curl -b "SID=YOUR_SID" -F "urls=magnet:?xt=urn:btih:..." -F "category=ISO" http://localhost:8080/api/v2/torrents/add

# Pause all torrents in the 'Movies' category
curl -b "SID=YOUR_SID" -X POST "http://localhost:8080/api/v2/torrents/pause?category=Movies"
```

## API examples
Use the `qbittorrent-api` Python library for advanced automation, combined with a Pydantic v2 schema for validating clean execution parameters.

```python
import qbittorrentapi
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# Define the automated cleanup configuration schema using Pydantic v2
class CleanupRule(BaseModel):
    max_ratio: float = Field(..., gt=0.0, description="The maximum seed ratio allowed before deletion")
    categories_to_clean: List[str] = Field(default_factory=list, description="List of categories this rule applies to")
    delete_files: bool = Field(default=False, description="Whether to also delete downloaded files on disk")

    @field_validator('max_ratio')
    @classmethod
    def validate_ratio(cls, val: float) -> float:
        if val > 10.0:
            raise ValueError("Seed ratio limit cannot exceed 10.0")
        return val

def run_automated_cleanup(client_host: str, rule: CleanupRule) -> None:
    # Initialize the qBittorrent client
    qbt_client = qbittorrentapi.Client(
        host=client_host,
        port=8080,
        username='admin',
        password='password'
    )

    try:
        qbt_client.auth_log_in()

        # Delete torrents that have finished seeding according to Pydantic rules
        for torrent in qbt_client.torrents_info(status_filter='completed'):
            if torrent.category in rule.categories_to_clean and torrent.ratio >= rule.max_ratio:
                print(f"Cleaning up torrent matching rule: {torrent.name}")
                torrent.delete(delete_files=rule.delete_files)
    finally:
        qbt_client.auth_log_out()

# Example invocation with Pydantic validated configuration
if __name__ == "__main__":
    config = CleanupRule(max_ratio=2.0, categories_to_clean=["ISO", "Temp"], delete_files=False)
    run_automated_cleanup(client_host='localhost', rule=config)
```

## Related tools / concepts
- [qBittorrent](qbittorrent.md) — The core download engine.
- [n8n](n8n.md) — The primary workflow engine for qBittorrent automation.
- [SearXNG](searXNG.md) — For programmatically finding content.
- [Plex](plex.md) — Media consumption platform.
- [Jellyfin](jellyfin.md) — Open-source media server.
- [Authentik](authentik.md) — Securing the Web API.
- [Tailscale](tailscale.md) — Secure remote access to the API.
- [Speedtest](speedtest.md) — Providing metrics for bandwidth automation.
- [Element](element.md) — Notification endpoint.
- [Synapse](synapse.md) — Matrix-based notification backbone.
- [Paperless-ngx](paperless-ngx.md) — Automated ingestion of downloaded documents.
- [Local LLMs Guide](../tools/ai_knowledge/local_llms.md) — Reference for Gemma 3 and other models.

## Sources / references
- [qBittorrent WebUI API Specification](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1))
- [qbittorrent-api Python Library Github](https://github.com/rmartin16/qbittorrent-api)
- [Arrr Suite (Sonarr/Radarr) Wiki](https://wiki.servarr.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/protocol/tasks)

## Contribution Metadata
- Last reviewed: 2026-11-08
- Confidence: high
