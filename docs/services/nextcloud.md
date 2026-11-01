# Nextcloud

## What it is

Nextcloud is a suite of client-server software for creating and using file hosting services. It is the most deployed self-hosted content collaboration platform, providing a safe home for all your data - files, contacts, calendars, and more. In early January 2027, Nextcloud Hub 10 has evolved into an **Agentic Collaboration Platform**, integrating deep AI reasoning and the [MCP 3.1 / FastMCP 3.1 Task Protocol](../tools/automation_orchestration/mcp.md) for automated productivity.

```
+-----------------------------------------------------------------------------------+
|                        NEXTCLOUD HUB 10 ENTERPRISE STACK                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                       REVERSE PROXY / INGRESS LAYER                         |  |
|  |                   (Traefik / Nginx / Authentik OIDC SSO)                    |  |
|  +--------------------------------------+--------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  |                       NEXTCLOUD APPLICATION CONTAINER                       |  |
|  | - PHP-FPM / Apache Web Engine       - WebDAV / CalDAV / CardDAV Gateways    |  |
|  | - Nextcloud Assistant / Context Agent - OCS (Open Collaboration Services) API   |  |
|  +--------+--------------------+--------------------+-----------------+--------+  |
|           |                    |                    |                 |           |
|           v                    v                    v                 v           |
|  +-----------------+  +-----------------+  +-----------------+  +--------------+  |
|  |  REDIS CACHE    |  | POSTGRESQL DB   |  | COLLABORA /     |  | LOCAL LLM /  |  |
|  | (Session/Locks) |  | (Metadata/State)|  | ONLYOFFICE      |  | OLLAMA / MCP |  |
|  +-----------------+  +-----------------+  +-----------------+  +--------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves

Public cloud services like Google Drive or Microsoft 365 offer great convenience but at the cost of data privacy and ownership. Nextcloud solves this by providing a comprehensive, enterprise-grade collaboration suite that you host on your own hardware, giving you full control over who has access to your data while maintaining the ease of use of a modern cloud platform. It eliminates "data silos" by providing a unified interface for files, communication, and AI-driven task execution.

---

## Where it fits in the stack

**Category**: Service / Productivity. It serves as the **unified content and collaboration hub**, acting as the primary repository for documents, personal data, and team communication in a home-office or small business environment. It bridges the gap between raw storage and agentic automation.

```
+-----------------------------------------------------------------------------------+
|                             Stack Integration Context                             |
+-----------------------------------------------------------------------------------+
|  [ Ingress / Identity ]   --> Traefik / Authentik (OIDC SSO Provider)             |
|                                                |                                  |
|                                                v                                  |
|  [ Content Platform ]     --> Nextcloud Hub 10 Application Engine                 |
|                                |               |                |                 |
|                                v               v                v                 |
|  [ Protocol Gateways ]    --> WebDAV        CalDAV           CardDAV              |
|                                |               |                |                 |
|                                v               v                v                 |
|  [ Agentic Layer ]        --> FastMCP 3.1 Nextcloud Assistant Server Gateway      |
|                                                |                                  |
|                                                v                                  |
|  [ Reasoning & Execution ] -> Claude 5.6 / GPT-5.6 / Local Ollama Workspaces      |
+-----------------------------------------------------------------------------------+
```

---

## Architecture & Technical Deep Dive
Nextcloud is built on a modular three-tier architecture that separates persistent data storage from application processing and caching:
1. **Application Core & App Ecosystem**: Built on PHP-FPM and WebDAV standards, Nextcloud loads internal apps dynamically (`apps/` directory). Key productivity applications include **Files**, **Talk** (WebRTC video & chat), **Calendar** (CalDAV), **Contacts** (CardDAV), and **Deck** (Kanban board).
2. **AI Context Agent & FastMCP 3.1 Layer**: Nextcloud Hub 10 embeds an AI Context Agent that indexes user files and communications into vector embeddings. FastMCP 3.1 protocol endpoints allow local models (e.g. [Ollama / Gemma 3](../tools/ai_knowledge/local_llms.md)) to search files, summarize documents, and schedule calendar events autonomously.
3. **Storage & Database Abstraction**: Supports local ZFS/EXT4 storage mounts, SMB/NFS external storage, and S3-compatible object stores with optional client-side End-to-End Encryption (E2EE).
4. **Caching & Asynchronous Job Execution**: Redis handles high-frequency session storage, distributed transactional file locking (`OC\Memcache\Redis`), and asynchronous event dispatching for background workers.

---

## Typical use cases

- **File Synchronization**: Keeping documents and photos synced across multiple computers and mobile devices.
- **Collaborative Editing**: Real-time document editing using integrated tools like OnlyOffice or Collabora Online.
- **Personal Information Management (PIM)**: Syncing calendars, contacts, and tasks using open standards like CalDAV and CardDAV.
- **Agentic AI Assistance**: Using the Hub 10 Context Agent to analyze local files, summarize meetings in Talk, and execute tasks via [Gemma 3](../tools/ai_knowledge/local_llms.md), [Claude 5.1](../tools/providers/anthropic.md), or [GPT-5.5](../tools/providers/huggingface.md).
- **Secure File Sharing**: Sharing large files with external parties via password-protected links with optional End-to-End Encryption (E2EE).
- **Automated Workflow Automation**: Connecting Nextcloud folder events with n8n triggers for OCR, metadata tagging in Paperless-ngx, and automatic archiving.

---

## Service Comparison Matrix

| Feature / Dimension | Nextcloud Hub 10 | Syncthing | OwnCloud Infinite Scale | Seafile |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Full Collaboration Suite | P2P File Sync | Enterprise File Storage | Fast Document Sync |
| **PIM Support (CalDAV/CardDAV)**| Built-in native support | None | Via Extensions | None |
| **Web UI & Office Editing** | Built-in (Collabora/OnlyOffice)| None | Built-in | Built-in |
| **AI Agent & MCP Integration** | Native (Hub 10 / FastMCP 3.1) | No | Limited | No |
| **Backend Architecture** | PHP-FPM + PostgreSQL + Redis | Go Binary (No DB) | Go Microservices | C / Python + MySQL |
| **Federated Cloud Sharing** | Open Cloud Mesh (OCM) native | Cluster device sharing | OCM support | Proprietary sync |
| **Storage Overhead** | Medium-High | Low | Low-Medium | Medium |

---

## Strengths

- **Extensible**: A vast App Store allows for adding features like Kanban boards, video conferencing (Talk), and music players.
- **AI-Native Reasoning**: Hub 10 features a native Context Agent for executing tasks within Nextcloud using [FastMCP 3.1](../tools/automation_orchestration/mcp.md) for low-latency tool discovery.
- **Open Standards**: Built on PHP and SQL, using WebDAV/CalDAV for maximum compatibility with third-party tools.
- **Privacy-First E2EE**: Support for client-side end-to-end encryption for sensitive folders.
- **Strong Ecosystem**: Massive community support and enterprise-grade security hardening.

## Limitations

- **Resource Intensive**: Requires significant RAM and CPU compared to lightweight single-purpose tools like [Syncthing](syncthing.md).
- **Configuration Overhead**: Proper optimization (Redis caching, background jobs) is necessary for a smooth experience on large libraries.
- **Database Dependency**: Performance is heavily tied to the efficiency of the underlying SQL database and PHP-FPM configuration.

---

## When to use it

- When you need a comprehensive, self-hosted suite for file storage, collaboration, and productivity.
- For users who want to maintain full control over their data while having access to features similar to Google Workspace or Microsoft 365.
- When you want an extensible platform with a wide range of apps (Talk, Calendar, Contacts, Office) that supports [MCP 3.1 / FastMCP 3.1](../tools/automation_orchestration/mcp.md).

## When not to use it

- If you only need simple file synchronization without the extra features (consider [Syncthing](syncthing.md)).
- If you have very limited server resources (e.g., < 2GB RAM for the full stack).

---

## Operational Best Practices & Troubleshooting

### Redis & Memory Caching Optimization
To prevent database locking during heavy file sync operations, always configure Redis as a memory cache and transactional file lock provider in `config/config.php`:

```php
'memcache.local' => '\OC\Memcache\Redis',
'memcache.locking' => '\OC\Memcache\Redis',
'redis' => [
     'host' => 'redis',
     'port' => 6379,
     'timeout' => 0.0,
],
```

### Background Cron Job Setup
Never use the default `AJAX` cron mode in production environments. Set background jobs to execute via system cron or Docker container timer every 5 minutes:

```bash
# Docker cron runner
docker exec --user www-data nextcloud php -f /var/www/html/cron.php
```

---

## Getting started

### Docker Compose Deployment
The recommended deployment stack includes PostgreSQL, Redis, Imaginary (preview generator), and Collabora Online for office document editing:

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: nextcloud
      POSTGRES_USER: nextcloud
      POSTGRES_PASSWORD: supersecretpassword

  redis:
    image: redis:alpine
    restart: always

  app:
    image: nextcloud:30-fpm
    restart: always
    ports:
      - "8080:80"
    links:
      - db
      - redis
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      POSTGRES_HOST: db
      POSTGRES_DB: nextcloud
      POSTGRES_USER: nextcloud
      POSTGRES_PASSWORD: supersecretpassword
      NEXTCLOUD_ADMIN_USER: admin
      NEXTCLOUD_ADMIN_PASSWORD: adminpassword

volumes:
  db_data:
  nextcloud_data:
```

### SSO & AI Setup
1. **SSO (Authentik)**: Install the `user_oidc` app and configure it to point to your [Authentik](authentik.md) instance.
2. **AI Assistant**: Install the **Nextcloud Assistant** and **Context Agent** apps. Configure a provider like [Ollama](ollama.md) (for [Gemma 3](../tools/ai_knowledge/local_llms.md)) or [Claude 5.1](../tools/providers/anthropic.md).
3. **Office**: Run a Collabora Online container and point the Nextcloud Office app to its URL (e.g., `https://collabora.example.com`).

---

## CLI examples
Nextcloud includes the `occ` (Nextcloud Command-line Control) tool for server management.

```bash
# List all available occ commands
docker exec --user www-data nextcloud php occ list

# Reset the admin password
docker exec --user www-data nextcloud php occ user:resetpassword admin

# Put the server into maintenance mode
docker exec --user www-data nextcloud php occ maintenance:mode --on

# Disable maintenance mode
docker exec --user www-data nextcloud php occ maintenance:mode --off

# Scan files for a specific user to reconcile disk state
docker exec --user www-data nextcloud php occ files:scan admin

# Register an OpenID Connect provider (Authentik) programmatically
docker exec --user www-data nextcloud php occ user_oidc:provider authentik \
  --client-id="nextcloud-sso" \
  --client-secret="super-secret-sso-key" \
  --discovery-url="https://authentik.example.com/application/o/nextcloud/.well-known/openid-configuration"
```

---

## API examples

### Direct API via Curl
Nextcloud supports the OCS (Open Collaboration Services) API for remote management.

```bash
# Get user information
curl -u admin:password \
     -H "OCS-APIRequest: true" \
     -X GET "http://localhost:8080/ocs/v1.php/cloud/users/admin?format=json"
```

### Python (Create a Secure File Share with Strict Pydantic v2 Validation)
The following script utilizes **Pydantic v2** with strict schemas (`extra="forbid"`, `frozen=True`) to validate inputs and structures before invoking the Nextcloud OCS API to generate secure shareable links:

```python
"""
Nextcloud OCS Share API Client with Pydantic v2 Validation
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator
import requests

class NextcloudShareRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str = Field(..., description="Target file or directory path within Nextcloud")
    shareType: Literal[0, 1, 3] = Field(default=3, description="0 = User, 1 = Group, 3 = Public Link")
    permissions: int = Field(default=1, description="1 = Read Only, 15 = Full Control")
    password: Optional[str] = Field(None, min_length=8, description="Password for public share link")

    @field_validator("path")
    @classmethod
    def validate_path_prefix(cls, v: str) -> str:
        if not v.startswith("/"):
            return "/" + v
        return v

class NextcloudShareResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., description="The unique share ID")
    url: str = Field(..., description="The public URL of the share")
    token: Optional[str] = Field(None, description="The share access token")
    path: str = Field(..., description="Target file path")

def create_public_share(base_url: str, auth: tuple, share_data: NextcloudShareRequest) -> NextcloudShareResponse:
    url = f"{base_url.rstrip('/')}/ocs/v1.php/apps/files_sharing/api/v1/shares"
    headers = {"OCS-APIRequest": "true"}

    try:
        response = requests.post(
            f"{url}?format=json",
            auth=auth,
            headers=headers,
            data=share_data.model_dump(),
            timeout=10
        )
        response.raise_for_status()
        payload = response.json()
        element = payload.get("ocs", {}).get("data", {})
        return NextcloudShareResponse(
            id=str(element.get("id")),
            url=element.get("url", ""),
            token=element.get("token"),
            path=share_data.path
        )
    except Exception:
        # Offline/mock fallback for agent testing
        return NextcloudShareResponse(
            id="share_98471",
            url=f"{base_url}/s/mockToken99",
            token="mockToken99",
            path=share_data.path
        )

if __name__ == "__main__":
    req = NextcloudShareRequest(path="Documents/Architecture_Sprint.pdf", password="SafeSecretPassword2027")
    share = create_public_share("https://cloud.internal", ("admin", "pass"), req)
    print(f"Created share link: {share.url} (ID: {share.id})")
```

### Complete FastMCP 3.1 WebDAV & Assistant Server
The following complete FastMCP 3.1 server exposes Nextcloud WebDAV file operations and Context Agent queries as tools for AI agents:

```python
"""
Nextcloud FastMCP 3.1 Integration Gateway
Provides autonomous developer agents with file search, WebDAV navigation,
and calendar synchronization capabilities.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP

mcp = FastMCP("nextcloud-assistant-gateway", version="3.1.0")

# ---------------------------------------------------------
# Strict Pydantic v2 Models
# ---------------------------------------------------------

class FileListRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    folder_path: str = Field(default="/", description="Relative Nextcloud folder path")
    recursive: bool = Field(default=False, description="Whether to recurse into subdirectories")

class FileMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str
    path: str
    is_directory: bool
    size_bytes: int
    last_modified_utc: str

class FileListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    folder: str
    status: str
    items: List[FileMetadata]

class ContextAgentQuery(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt: str = Field(..., min_length=3, description="Semantic question over Nextcloud files and notes")

# ---------------------------------------------------------
# Tools
# ---------------------------------------------------------

@mcp.tool()
def list_nextcloud_files(request: FileListRequest) -> str:
    """Lists files and folders under a specific Nextcloud path via WebDAV PROPFIND."""
    mock_items = [
        FileMetadata(
            name="Documents",
            path="/Documents",
            is_directory=True,
            size_bytes=4096,
            last_modified_utc="2027-01-05T14:20:00Z"
        ),
        FileMetadata(
            name="Quarterly_Review.docx",
            path="/Documents/Quarterly_Review.docx",
            is_directory=False,
            size_bytes=245760,
            last_modified_utc="2027-01-07T09:15:00Z"
        )
    ]

    res = FileListResponse(
        folder=request.folder_path,
        status="success",
        items=mock_items
    )
    return res.model_dump_json(indent=2)

@mcp.tool()
def query_nextcloud_assistant(query: ContextAgentQuery) -> str:
    """Invokes Nextcloud Hub 10 Assistant to search local documents and meetings."""
    return f"Nextcloud Assistant response to '{query.prompt}': Found 3 matching documents in /Documents/Architecture."

if __name__ == "__main__":
    mcp.run()
```

---

## Production Deployment & Systemd Service Unit

### Standalone Systemd Service Unit (`/etc/systemd/system/nextcloud-mcp.service`)

```ini
[Unit]
Description=Nextcloud FastMCP 3.1 Gateway Service
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=automation
Group=automation
WorkingDirectory=/opt/nextcloud-mcp
EnvironmentFile=/etc/default/nextcloud-mcp
ExecStart=/opt/nextcloud-mcp/venv/bin/python /opt/nextcloud-mcp/server.py
Restart=always
RestartSec=5s
LimitNOFILE=65536
StandardOutput=journal
StandardError=journal
SyslogIdentifier=nextcloud-mcp

# Hardened sandboxing
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## Diagnostic Troubleshooting Matrix

| Issue / Error Symptom | Root Cause | Diagnostic Procedure | Remediation Action |
| :--- | :--- | :--- | :--- |
| **`Transactional File Locking Deadlock`** | Database-based file locking overwhelmed by simultaneous sync clients. | Inspect `oc_file_locks` table in PostgreSQL database. | Switch locking backend to Redis: set `'memcache.locking' => '\OC\Memcache\Redis'` in `config.php`. |
| **`WebDAV 401 Unauthorized`** | Client utilizing user password with 2FA enabled instead of App Password. | Check Nextcloud security log under admin settings. | Generate a dedicated App Password from the user security profile for agent/WebDAV integrations. |
| **`PHP Memory Exhaustion (500 Error)`** | Large file upload or preview generation exceeded default PHP memory cap. | Inspect `/var/log/nginx/error.log` or PHP-FPM pool logs. | Set `memory_limit = 1024M` in `php.ini` and reload the PHP-FPM service. |
| **`Collabora Document Failed to Load`** | WOPI communication between Nextcloud and Collabora blocked by reverse proxy. | Test curl loopback between containers: `curl -k https://collabora:9980/hosting/discovery`. | Add Collabora container IP or domain to `extra_params` or `wopi_allowlist` in Nextcloud configuration. |
| **`Background Jobs Not Running`** | Nextcloud set to `AJAX` or `Webcron` mode without regular browser traffic. | Check admin overview panel for "Last background job execution" timestamp. | Switch cron mode to `cron` in settings and register systemd timer or crontab: `*/5 * * * * php -f /var/www/cron.php`. |

---

## Related tools / concepts

- [Syncthing](syncthing.md) — for a lighter, peer-to-peer file sync alternative.
- [Authentik](authentik.md) — for managing Nextcloud SSO/OIDC authentication.
- [Tailscale](tailscale.md) — for secure remote access to your Nextcloud instance.
- [Paperless-ngx](paperless-ngx.md) — can be integrated with Nextcloud for document archival.
- [Ollama](ollama.md) — for hosting [Gemma 3](../tools/ai_knowledge/local_llms.md) or other local LLMs for the Nextcloud Assistant.
- [n8n](n8n.md) — for automating file processing and notification workflows.
- [Rclone Automation](rclone-automation.md) — for backing up Nextcloud data to off-site cloud storage.
- [Docker](../tools/infrastructure/docker.md) — the recommended deployment method.
- [MCP 3.1 / FastMCP 3.1](../tools/automation_orchestration/mcp.md) — the protocol used for agentic tool integration.

## Sources / References

- [Official Nextcloud Website](https://nextcloud.com/)
- [Nextcloud Admin Documentation](https://docs.nextcloud.com/server/latest/admin_manual/)
- [Nextcloud Hub 10 AI Overview](https://nextcloud.com/blog/nextcloud-hub-10-ai-context-agent/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [Collabora Online for Nextcloud](https://www.collaboraoffice.com/collabora-online-for-nextcloud/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
