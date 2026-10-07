# qBittorrent

## What it is
qBittorrent is a premier, open-source BitTorrent client designed for cross-platform reliability, privacy, and high-performance file transfers. Written in C++ using the Qt framework and libtorrent-rasterbar engine, it provides a feature-rich, advertisement-free alternative to proprietary clients. As of early 2027, version **5.x** has solidified its position as the enterprise and homelab standard for content acquisition, featuring advanced asynchronous piece calculation, automated bandwidth throttling, frontier model (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Llama 4) automation, and native **Model Context Protocol (FastMCP 3.1)** tool integration.

```
+-----------------------------------------------------------------------------------+
|                            AUTOMATED CONTENT PIPELINE                             |
|  [ Sonarr / Radarr / Lidarr ] <---> [ FastMCP 3.1 Server ] <---> [ Agent Runtime ]|
+-----------------------------------------------------------------------------------+
                                         |
                            (WebUI API v2 / REST JSON)
                                         v
+-----------------------------------------------------------------------------------+
|                               GLUETUN VPN SIDECAR                                 |
|  +-----------------------------------------------------------------------------+  |
|  | WireGuard / OpenVPN Tunnel with Port Forwarding & Automated Killswitch      |  |
|  +-----------------------------------------------------------------------------+  |
|                                        |                                          |
|                                        v                                          |
|  +-----------------------------------------------------------------------------+  |
|  | qBittorrent Engine (libtorrent-rasterbar 2.0.x Async I/O Core)             |  |
|  | - WebUI Server (Port 8080)        - BitTorrent Protocol Core (Port 6881)    |  |
|  | - Category / Tag Rules Engine     - Sequential & First/Last Piece Download  |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                            STORAGE & MEDIA ACCESS                                 |
|        [ Local ZFS Pool / Unraid Share / NFS Mount / Jellyfin / Plex ]            |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Managing large-scale distributed file transfers via the BitTorrent protocol requires precise bandwidth control, secure network isolation, and seamless automation capabilities. qBittorrent solves these challenges by providing a lightweight, headless-capable daemon (`qbittorrent-nox`) alongside an administrative Web UI. It allows users and autonomous agents to manage multi-terabyte download queues, filter torrents via dynamic tagging and categories, execute post-completion triggers, and safely isolate P2P traffic through VPN sidecars.

Key problems resolved include:
- **Unsecured P2P Traffic**: Isolation of torrent traffic inside containerized VPN namespaces with strict killswitches.
- **Unstructured Media Intake**: Automatic categorization, path remapping, and post-processing script execution upon torrent download completion.
- **Agentic Ingestion Bottlenecks**: Exposing a full REST API and FastMCP 3.1 protocol interface so LLM agents can query download states, manage seed ratios, and fetch open-source dataset distributions without manual supervision.

## Where it fits in the stack
**Category**: Service / Content & Dataset Acquisition. It serves as the **primary data intake engine** for large-scale dataset acquisition, media server ingestion, and open-source software distribution mirroring.

```
+-----------------------------------------------------------------------------------+
|                               USER & AGENT LAYER                                  |
|   [ Web Browser ]         [ FastMCP Agent Tool ]         [ Media Automation ]     |
+-----------------------------------------------------------------------------------+
                                         |
                          (Authenticated API / Port 8080)
                                         v
+-----------------------------------------------------------------------------------+
|                              QBITTORRENT SERVICES                                 |
|  +------------------------+  +------------------------+  +---------------------+  |
|  | Category Manager       |  | RSS Auto-Downloader    |  | Ratio / Seeding     |  |
|  | - /downloads/tv        |  | - Automated Regex Match|  | - Seed Time Rules   |  |
|  | - /downloads/datasets  |  | - Smart Episode Filters|  | - Ratio Throttling  |  |
|  +------------------------+  +------------------------+  +---------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                          NETWORK & STORAGE ISOLATION                              |
|           [ WireGuard Tunnel Namespace ] <---> [ Mounted Shared Storage ]          |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Headless Server Operations**: Running `qbittorrent-nox` as a Docker container on NAS or cloud instances for 24/7 seeding and downloading.
- **Automated Dataset Acquisition**: Ingesting multi-gigabyte open-source AI datasets (e.g., HuggingFace mirrors, Common Crawl splits) via RSS and automated magnet link queues.
- **Agentic File Transfers**: Allowing AI agents (e.g., Claude 5.6, GPT-5.6) to inspect file structures, adjust download priority, and clean completed downloads using FastMCP 3.1 Task Protocol.
- **Media Automation Ecosystem**: Serving as the download backend for "Arr" stack suites (Sonarr, Radarr, Readarr) with dynamic directory mapping.
- **Ratio-Compliant High-Performance Seeding**: Managing private tracker seed ratios with granular upload speed limits and automated removal rules based on seeding time.

## Strengths
- **No Bloatware**: Completely free and open-source (GPL-2.0) with zero advertising, telemetry, or bundled third-party installers.
- **Feature-Rich Web UI**: Fully responsive browser interface replicating the native Qt desktop GUI, supporting bulk actions and search plugins.
- **Extensible Search Engine**: Python-based plugin system allowing direct search across dozens of public and private indexers.
- **Post-Processing Execution**: Native hook support to execute shell scripts or webhook calls upon torrent state change or completion.
- **Native FastMCP 3.1 Integration**: Seamless direct tool-calling interface enabling LLM agents to monitor, add, pause, or prune torrent transfers safely.
- **Granular Network Binding**: Capability to bind listening sockets strictly to a specific network interface (e.g., `tun0` or `wg0`), preventing IP leaks if the VPN drops.

## Limitations
- **Memory Footprint at Scale**: Managing libraries with over 20,000 active torrents requires substantial RAM allocation and libtorrent cache tuning.
- **Single-Threaded UI Overhead**: Extremely high network IOPS can occasionally stall Web UI responses if disk I/O bottlenecks occur.
- **Native WebUI Authentication**: Built-in HTTP authentication lacks multi-factor auth (MFA), requiring reverse proxies like [Authentik](authentik.md) or Traefik for public-facing deployments.

## When to use it
- When you need a hardened, headless BitTorrent engine for automated server or NAS environments.
- When isolating download traffic behind a VPN sidecar container (e.g., Gluetun) with interface binding.
- When constructing autonomous agent pipelines that require programmatic dataset or ISO downloads via Web API.
- When managing high-bandwidth seeding workloads with ratio and time-based limits.

## When not to use it
- For protocols other than BitTorrent (e.g., USENET/NZBs, direct HTTP, or IPFS transfers).
- In lightweight embedded hardware where a ultra-minimal client like Transmission is required.

## Getting started

### Docker Compose (Hardened Stack with Gluetun VPN Sidecar)
Deploying qBittorrent routed strictly through a WireGuard VPN container ensures total privacy and prevents real IP leakage via killswitch mechanisms.

```yaml
version: "3.8"

services:
  gluetun:
    image: qmcgaw/gluetun:v3
    container_name: gluetun
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    environment:
      - VPN_SERVICE_PROVIDER=custom
      - VPN_TYPE=wireguard
      - WIREGUARD_PRIVATE_KEY=yOurWireGuardPrivateKeyGoesHere=
      - WIREGUARD_ADDRESSES=10.2.0.2/32
      - FIREWALL_OUTBOUND_SUBNETS=192.168.1.0/24
    ports:
      - 8080:8080 # qBittorrent Web UI
      - 6881:6881 # BitTorrent TCP
      - 6881:6881/udp # BitTorrent UDP
    restart: always

  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    network_mode: "container:gluetun"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - WEBUI_PORT=8080
      - TORRENTING_PORT=6881
    volumes:
      - ./config:/config
      - /mnt/storage/downloads:/downloads
    depends_on:
      - gluetun
    restart: unless-stopped
```

### Initial Configuration Checklist
1. Access the Web UI at `http://localhost:8080`.
2. Retrieve the temporary admin password from container startup logs:
   ```bash
   docker logs qbittorrent 2>&1 | grep "A temporary password is set"
   ```
3. Navigate to **Tools > Options > Web UI** and update username and password.
4. Go to **Tools > Options > Advanced > Network Interface** and bind strictly to `tun0` (or `wg0`).

## CLI examples

### Container Operations and Status Checks
```bash
# Query qbittorrent-nox version
docker exec qbittorrent qbittorrent-nox --version

# Pause all active torrents via CLI
docker exec qbittorrent qbittorrent-nox --pause-all

# Resume all active torrents
docker exec qbittorrent qbittorrent-nox --resume-all
```

### Web API Direct Invocation via cURL
```bash
# 1. Login and save cookie
curl -i --header "Referer: http://localhost:8080" \
     --data "username=admin&password=YourHardenedPassword" \
     --cookie-jar /tmp/qb_cookie.txt \
     http://localhost:8080/api/v2/auth/login

# 2. Add magnet link with category
curl -X POST \
     --cookie /tmp/qb_cookie.txt \
     --data-urlencode "urls=magnet:?xt=urn:btih:ubuntu_hash_here" \
     --data "category=datasets&paused=false" \
     http://localhost:8080/api/v2/torrents/add

# 3. Fetch server state summary
curl -s --cookie /tmp/qb_cookie.txt \
     http://localhost:8080/api/v2/transfer/info | jq .
```

## API examples

Below is a complete FastMCP 3.1 server implementation that integrates with qBittorrent's Web API v2. It validates torrent states, bandwidth usage, and magnet link additions using Pydantic v2 schemas.

```python
import requests
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

# 1. Initialize FastMCP 3.1 Server
mcp = FastMCP("qBittorrentManager", version="3.1.0")

# 2. Define Pydantic v2 Models for API Validation
class QBittorrentConfig(BaseModel):
    base_url: str = Field("http://localhost:8080", description="qBittorrent Web UI base URL")
    username: str = Field("admin", description="Web UI login username")
    password: str = Field(..., description="Web UI login password")

class TorrentItem(BaseModel):
    hash: str = Field(..., description="Torrent info hash")
    name: str = Field(..., description="Display name of the torrent")
    progress: float = Field(..., description="Download progress (0.0 to 1.0)")
    dlspeed: int = Field(..., description="Download speed in bytes/sec")
    upspeed: int = Field(..., description="Upload speed in bytes/sec")
    state: str = Field(..., description="Current status state string")
    category: Optional[str] = Field("", description="Assigned category")
    eta: int = Field(..., description="Estimated time to completion in seconds")

    @field_validator('progress')
    @classmethod
    def validate_progress_range(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("Progress fraction must be between 0.0 and 1.0")
        return v

class SystemTransferInfo(BaseModel):
    dl_info_speed: int = Field(..., description="Global download speed (bytes/sec)")
    up_info_speed: int = Field(..., description="Global upload speed (bytes/sec)")
    dl_rate_limit: int = Field(..., description="Global download speed limit")
    up_rate_limit: int = Field(..., description="Global upload speed limit")
    connection_status: str = Field(..., description="Network connection state")

# 3. Session Authenticator
class QBittorrentClient:
    def __init__(self, config: QBittorrentConfig):
        self.config = config
        self.session = requests.Session()
        self._login()

    def _login(self):
        login_url = f"{self.config.base_url}/api/v2/auth/login"
        headers = {"Referer": self.config.base_url}
        data = {"username": self.config.username, "password": self.config.password}
        resp = self.session.post(login_url, data=data, headers=headers)
        if resp.text != "Ok.":
            raise PermissionError("qBittorrent API authentication failed")

    def get_torrents(self, category: Optional[str] = None) -> List[TorrentItem]:
        url = f"{self.config.base_url}/api/v2/torrents/info"
        params = {}
        if category:
            params["category"] = category
        resp = self.session.get(url, params=params)
        resp.raise_for_status()

        results = []
        for raw in resp.json():
            results.append(TorrentItem.model_validate(raw))
        return results

    def add_magnet(self, magnet_url: str, category: str = "", save_path: str = "") -> bool:
        url = f"{self.config.base_url}/api/v2/torrents/add"
        data = {
            "urls": magnet_url,
            "category": category,
            "savepath": save_path,
            "paused": "false"
        }
        resp = self.session.post(url, data=data)
        return resp.status_code == 200

    def get_transfer_info(self) -> SystemTransferInfo:
        url = f"{self.config.base_url}/api/v2/transfer/info"
        resp = self.session.get(url)
        resp.raise_for_status()
        return SystemTransferInfo.model_validate(resp.json())

# 4. FastMCP 3.1 Tools Exposed to LLM Agents
@mcp.tool()
def list_active_torrents(
    base_url: str,
    username: str,
    password: str,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """Fetch and validate active torrent list from qBittorrent."""
    try:
        cfg = QBittorrentConfig(base_url=base_url, username=username, password=password)
        client = QBittorrentClient(cfg)
        torrents = client.get_torrents(category=category)
        return {
            "status": "success",
            "count": len(torrents),
            "torrents": [t.model_dump() for t in torrents]
        }
    except Exception as e:
        return {"status": "error", "details": str(e)}

@mcp.tool()
def add_download_task(
    base_url: str,
    username: str,
    password: str,
    magnet_link: str,
    category: str = "agent_intake"
) -> Dict[str, Any]:
    """Add a new magnet link to qBittorrent queue with category tagging."""
    try:
        cfg = QBittorrentConfig(base_url=base_url, username=username, password=password)
        client = QBittorrentClient(cfg)
        success = client.add_magnet(magnet_link, category=category)
        return {"status": "success" if success else "failed"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@mcp.tool()
def get_global_bandwidth(
    base_url: str,
    username: str,
    password: str
) -> Dict[str, Any]:
    """Query global download/upload speed and network connection status."""
    try:
        cfg = QBittorrentConfig(base_url=base_url, username=username, password=password)
        client = QBittorrentClient(cfg)
        info = client.get_transfer_info()
        return {
            "status": "success",
            "download_speed_mbps": round(info.dl_info_speed / (1024 * 1024), 2),
            "upload_speed_mbps": round(info.up_info_speed / (1024 * 1024), 2),
            "connection_status": info.connection_status
        }
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [qBittorrent Automation](qbittorrent-automation.md) — For advanced API workflows and n8n integrations.
- [n8n](n8n.md) — For orchestrating downloads with other services.
- [Plex](plex.md) — For consuming media downloaded via qBittorrent.
- [Jellyfin](jellyfin.md) — Open-source media server alternative.
- [Authentik](authentik.md) — For securing remote access to the Web UI.
- [Tailscale](tailscale.md) — For secure remote access to the dashboard.
- [SearXNG](searXNG.md) — A privacy-focused search engine for finding torrents.
- [Paperless-ngx](paperless-ngx.md) — For managing documents acquired via Bittorrent.
- [Local LLMs Guide](../tools/ai_knowledge/local_llms.md) — Reference for Gemma 3 and other models.
- [Gluetun](https://github.com/qdm12/gluetun) — VPN sidecar for secure torrenting.

## Sources / references
- [qBittorrent Official Project Site](https://www.qbittorrent.org/)
- [qBittorrent Source Code Repository](https://github.com/qbittorrent/qBittorrent)
- [Web API Development Reference](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1))
- [Model Context Protocol Specification](https://modelcontextprotocol.io/protocol/tasks)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
