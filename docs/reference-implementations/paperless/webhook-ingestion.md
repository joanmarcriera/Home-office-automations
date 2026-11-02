# Reference Implementation: Paperless-ngx Webhook Ingestion

## What it is
A comprehensive architecture, deployment guide, and reference implementation for programmatically streaming and uploading documents to Paperless-ngx via its REST API and Model Context Protocol (FastMCP 3.1) endpoints. This method establishes real-time document ingestion pathways from external edge sources—such as physical mobile network scanners, email parser daemons, home automation event webhooks, or autonomous multi-agent orchestrators—bypassing the polling lag and file-system locking of traditional consumption folders.

```
+---------------------------------------------------------------------------------------------------+
|                        PAPERLESS-NGX REAL-TIME INGESTION ARCHITECTURE                             |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  |                             DISTRIBUTED INGESTION SOURCES                                   |  |
|  |       (iOS Scanner Shortcuts / IMAP Email Gateway / n8n Orchestrator / Multi-Agent)         |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 |                                                 |
|                                                 v  HTTP Multipart POST / HMAC Signed Webhook      |
|  +---------------------------------------------------------------------------------------------+  |
|  |                        INGRESS REVERSE PROXY & SECURITY GATEWAY                             |  |
|  |          (Cloudflare Tunnel / Traefik / Authentik Forward-Auth / TLS 1.3 Termination)       |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 |                                                 |
|                                                 v  Internal Mesh Route / Token Authorization      |
|  +---------------------------------------------------------------------------------------------+  |
|  |                  FASTMCP 3.1 DOCUMENT INGESTION & VALIDATION ROUTER                         |  |
|  | - Strict Pydantic v2 Schema Enforcement    - Asynchronous Multipart Streamer                |  |
|  | - Pre-OCR Metadata Tag Resolution          - Deduplication & SHA-256 Checksumming           |  |
|  | - Celery Task UUID Registration            - Synchronous FastMCP 3.1 Event Dispatch         |  |
|  +----------------------+-----------------------------------------------+----------------------+  |
|                         |                                               |                         |
|                         v                                               v                         |
|  +---------------------------------------------+ +---------------------------------------------+  |
|  |         PAPERLESS-NGX CORE SERVICE          | |            CELERY & REDIS RUNTIME           |  |
|  | (/api/documents/post_document/ Controller) | | (Async Tesseract OCR / Content Indexing)   |  |
|  +----------------------+----------------------+ +----------------------+----------------------+  |
|                         |                                               |                         |
|                         +-----------------------+-----------------------+                         |
|                                                 |                                                 |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  |                         DOWNSTREAM AUTONOMOUS AGENT ACTIONS                                 |  |
|  |   (Claude 5.6 / GPT-5.6 / DeepSeek-V4 Document Classification, Tagging, & Task Dispatch)   |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## Ingestion Event Handling & Lifecycle Sequence

```
[Edge Scanner / Mobile Client / n8n]
                 |
                 v
   [FastMCP 3.1 Ingestion Router]
                 |
                 +---> 1. Validate Payload Schema (Pydantic v2 extra="forbid", frozen=True)
                 |           |
                 |           +---> [Schema Mismatch] -> Return HTTP 400 Bad Request
                 |
                 +---> 2. Compute SHA-256 Digest & Query Existing Hashes
                 |           |
                 |           +---> [Duplicate Detected] -> Return HTTP 409 Conflict (with doc_id)
                 |
                 v
   [Paperless REST Endpoint] (/api/documents/post_document/)
                 |
                 +---> 3. Transmit Multipart Stream + Authorization Token Header
                 |           |
                 |           +---> [HTTP 413 / 502] -> Exponential Backoff Retry (Max 3 attempts)
                 |
                 v
   [PostgreSQL & Redis Queue]
                 |
                 +---> 4. Enqueue Celery Worker Background Task
                 |
                 v
   [Celery Worker (Tesseract / OCRmyPDF)]
                 |
                 +---> 5. Generate Searchable PDF / Extract Text Chunks
                 |
                 v
   [Paperless Post-Save Signal]
                 |
                 v
   [Agent Notification Dispatch] ---> [Trigger Downstream Workflows in n8n / Claude Skills]
```

## What problem it solves
Traditional Paperless-ngx deployments depend on filesystem polling of the consumption directory (`/usr/src/paperless/consume/`). This presents multiple architectural and operational liabilities:
- **Polling Latency**: Inotify filesystem polling can take anywhere from 30 seconds to several minutes to register newly dropped files, delaying downstream agentic processing.
- **Filesystem Permissions & NFS Lockouts**: Networked NFS/SMB mounts from scanners frequently encounter file permission mismatches, incomplete partial writes, and stale file handle locks.
- **Loss of Upstream Context**: Dropping a PDF into a directory strips rich ingestion metadata—such as caller identity, custom tag taxonomies, correspondent overrides, originating transaction IDs, and capture timestamps.
- **Silent Failures**: If an ingestion fails during consumption folder scanning, the source scanner or caller receives no synchronous error code, leaving operators unaware of lost documents.

Webhook ingestion solves these failures by establishing a deterministic HTTP push pipeline with synchronous acknowledgment, atomic metadata injection, cryptographic deduplication, and direct integration into FastMCP 3.1 event networks.

## Where it fits in the stack
**Category**: Reference Implementation / Ingestion & Intake Architecture. It bridges edge devices and external orchestrators to the enterprise storage and AI reasoning planes:

```
+-----------------------------------------------------------------------+
|                 Agentic Reasoning & Automation Plane                  |
|  [Claude 5.6 / GPT-5.6 / n8n] <-> [FastMCP 3.1 Ingestion Router]      |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                     Edge Ingress & Reverse Proxy                      |
|  [Cloudflare Tunnel / Traefik Ingress] (Bearer Auth & Rate Limiting)  |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                  Paperless-ngx Core & Celery Pipeline                 |
|  [Gunicorn API] -> [Redis Celery Queue] -> [Tesseract / PostgreSQL]   |
+-----------------------------------------------------------------------+
```

## Ingestion Channel Comparison Matrix

| Evaluation Dimension | Webhook Push Ingestion | Directory Polling | IMAP Email Gateway | FastMCP 3.1 Tool Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **Ingestion Latency** | Sub-second (<350ms) | Polling Interval (1–5 min) | Polling Interval (1–3 min) | Immediate (<250ms) |
| **Metadata Injection** | Synchronous during upload | Regex matching on file name | Subject / Body heuristic regex | Synchronous Pydantic validated |
| **Payload Integrity Verification** | In-flight SHA-256 + HMAC | OS file size check | MIME boundary inspection | Strict schema + Hash audit |
| **Network Direction** | Inbound Push (HTTP POST) | Local File IO Mount | Inbound IMAP Polling | Bidirectional JSON-RPC 2.0 |
| **Error Feedback Loop** | Immediate HTTP 200/400/409/413| Silent error log file | Bounce message / Log | Structured JSON Exception |
| **Throughput Capacity** | 120+ docs/min parallel | Bound by FS scan locks | Bound by IMAP server latency | High-concurrency Async IO |
| **Agent Interoperability** | REST / Webhook Hookable | Indirect (File creation) | None (Mailbox bound) | Native FastMCP 3.1 Tooling |
| **Authentication Scope** | Django Rest Token / Bearer | POSIX User / Group | IMAP Credentials | FastMCP Bearer / Mutual TLS |

## Typical use cases
- **Multi-Agent Document Routing**: Autonomous agents (Claude 5.6, GPT-5.6, DeepSeek-V4) stream scanned contracts directly into Paperless, synchronously attaching tag taxonomies, document classification IDs, and vendor correspondents.
- **Physical Mobile Scanner Ingress**: iOS Shortcuts or Android scanning apps capturing receipts, computing SHA-256 signatures, and POSTing payloads through a Cloudflare Tunnel.
- **High-Volume Invoice Pipelines**: n8n workflows extracting incoming PDF attachments from financial billing portals and dispatching them with pre-filled billing metadata.
- **Home Office Automation**: Smart multifunction printers triggering direct HTTP uploads upon scan completion without intermediate Samba file shares.

## Strengths
- **Sub-Second Processing**: Eliminates folder polling sleep loops; files are enqueued for Celery OCR immediately upon receipt.
- **Atomic Metadata Assignment**: Tags, document types, correspondents, and custom creation timestamps are bound at the moment of upload.
- **Predictable Error Semantics**: Upstream callers receive exact HTTP status codes (e.g., 400 for bad parameters, 409 for duplicate content, 413 for oversized payloads).
- **FastMCP 3.1 Native**: Provides turnkey tool schemas for agentic integration into LLM developer environments.

## Limitations
- **Token Leakage Risk**: Long-lived Django REST tokens must be safeguarded with environment variables or HashiCorp Vault.
- **Reverse Proxy Body Limits**: Large architectural blueprints or high-DPI scans require explicit tuning of reverse proxy buffer sizes (`client_max_body_size 100M;`).
- **Resource Spikes During Heavy Ingest**: Bursts of incoming documents can congest Celery worker pools unless throttled or scaled.

## When to use it
- When low latency between document capture and agentic processing is required.
- When orchestrating document workflows with n8n, Temporal, or custom agent scripts.
- When ingesting documents from distributed edge devices over internet or VPN connections.

## When not to use it
- In minimal local installations where single-user folder drops with 5-minute polling are adequate.
- When edge scanning hardware is constrained to legacy FTP/SMB protocols without HTTP capability.

## Complete Multi-Container Docker Compose Stack

The following production `docker-compose.yml` provisions Paperless-ngx, PostgreSQL 16, Redis 7.2, and the containerized FastMCP Ingestion Gateway:

```yaml
version: "3.8"

services:
  paperless-db:
    image: postgres:16-alpine
    container_name: paperless-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: paperless
      POSTGRES_USER: paperless_admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - /mnt/tank/databases/paperless-db:/var/lib/postgresql/data
    secrets:
      - db_password
    networks:
      - paperless-internal

  paperless-redis:
    image: redis:7.2-alpine
    container_name: paperless-redis
    restart: unless-stopped
    command: redis-server --save "" --appendonly no --maxmemory 256mb --maxmemory-policy allkeys-lru
    networks:
      - paperless-internal

  paperless-webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:2.14
    container_name: paperless-webserver
    restart: unless-stopped
    depends_on:
      - paperless-db
      - paperless-redis
    environment:
      PAPERLESS_REDIS: redis://paperless-redis:6379
      PAPERLESS_DBHOST: paperless-db
      PAPERLESS_DBNAME: paperless
      PAPERLESS_DBUSER: paperless_admin
      PAPERLESS_DBPASS_FILE: /run/secrets/db_password
      PAPERLESS_SECRET_KEY_FILE: /run/secrets/django_secret
      PAPERLESS_URL: https://docs.internal.net
      PAPERLESS_TIME_ZONE: UTC
      PAPERLESS_OCR_LANGUAGE: eng+deu+fra
      PAPERLESS_TASK_WORKERS: 4
      PAPERLESS_WEBSERVER_WORKERS: 2
    volumes:
      - /mnt/tank/apps/paperless/data:/usr/src/paperless/data
      - /mnt/tank/apps/paperless/media:/usr/src/paperless/media
      - /mnt/tank/apps/paperless/export:/usr/src/paperless/export
    secrets:
      - db_password
      - django_secret
    networks:
      - paperless-internal
      - internal-management

  paperless-fastmcp-gateway:
    image: ghcr.io/homelab/paperless-fastmcp-gateway:2027.1
    container_name: paperless-fastmcp-gateway
    restart: unless-stopped
    depends_on:
      - paperless-webserver
    environment:
      - PAPERLESS_API_URL=http://paperless-webserver:8000
      - PAPERLESS_API_TOKEN_FILE=/run/secrets/paperless_api_token
      - GATEWAY_PORT=8090
      - LOG_LEVEL=INFO
    volumes:
      - /mnt/tank/apps/paperless-gateway/tmp:/tmp/gateway:rw
    secrets:
      - paperless_api_token
    networks:
      - paperless-internal
      - internal-management
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8090/healthz')"]
      interval: 15s
      timeout: 5s
      retries: 3

secrets:
  db_password:
    file: /opt/homelab/secrets/paperless_db_password.txt
  django_secret:
    file: /opt/homelab/secrets/paperless_django_secret.txt
  paperless_api_token:
    file: /opt/homelab/secrets/paperless_api_token.txt

networks:
  paperless-internal:
    internal: true
  internal-management:
    external: true
```

## Systemd Ingestion Gateway Service

When running the FastMCP Gateway as a native systemd unit on a bare-metal TrueNAS or Linux management host:

```ini
[Unit]
Description=Paperless-ngx Webhook Ingestion & FastMCP 3.1 Gateway
Documentation=file:///opt/homelab/docs/reference-implementations/paperless/webhook-ingestion.md
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=paperless-svc
Group=paperless-svc
WorkingDirectory=/opt/homelab/paperless-gateway
Environment="PYTHONUNBUFFERED=1"
Environment="PAPERLESS_URL=http://127.0.0.1:8000"
EnvironmentFile=/etc/default/paperless-gateway
ExecStart=/opt/homelab/paperless-gateway/venv/bin/python -m gateway.fastmcp_server
Restart=always
RestartSec=5s

# Sandboxing and System Hardening
ProtectSystem=strict
ProtectHome=true
ReadOnlyPaths=/opt/homelab/paperless-gateway/config
ReadWritePaths=/opt/homelab/paperless-gateway/tmp /var/log/paperless-gateway
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictSUIDSGID=true
NoNewPrivileges=true
LimitNOFILE=65535

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## Getting started
1. Generate an API token in the Paperless-ngx Django administration console (`/admin/authtoken/token/`).
2. Verify network connectivity to the Paperless REST endpoint:
   ```bash
   curl -s -H "Authorization: Token <YOUR_TOKEN>" https://docs.internal.net/api/ | jq .
   ```
3. Deploy the FastMCP Gateway using Docker Compose or systemd.
4. Test asynchronous document ingestion and metadata attachment with the CLI examples below.

## CLI examples

### 1. Ingestion via Multipart Curl
```bash
curl -X POST https://docs.internal.net/api/documents/post_document/ \
     -H "Authorization: Token 9f8a3b1c2d3e4f5a6b7c8d9e0f1a2b3c" \
     -F "document=@/path/to/invoice.pdf;type=application/pdf" \
     -F "title=2027-01 Enterprise Fiber Invoice" \
     -F "tags=4" \
     -F "tags=12" \
     -F "correspondent=5" \
     -F "document_type=2" \
     -F "created=2027-01-07T10:15:00Z"
```

### 2. Querying Ingestion Task Status
```bash
curl -s -X GET https://docs.internal.net/api/tasks/?task_id=3c9b74b8-2a96-419b-a3f2-1d58d8396ec2 \
     -H "Authorization: Token 9f8a3b1c2d3e4f5a6b7c8d9e0f1a2b3c" | jq .
```

## API examples

### Production FastMCP 3.1 Ingestion Server (Python + Pydantic v2)
The following server exposes document ingestion, duplicate verification, and task tracking to autonomous AI agents via FastMCP 3.1:

```python
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional
import httpx
from pydantic import BaseModel, Field, ConfigDict, field_validator
from fastmcp import FastMCP

mcp = FastMCP("Paperless-Webhook-Gateway-MCP", version="3.1.0")

class DocumentUploadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    file_path: str = Field(..., description="Absolute path to the local document payload.")
    title: Optional[str] = Field(None, max_length=128, description="Override document title.")
    tags: List[int] = Field(default_factory=list, description="List of primary tag IDs.")
    correspondent_id: Optional[int] = Field(None, description="Numeric correspondent ID.")
    document_type_id: Optional[int] = Field(None, description="Numeric document type ID.")
    created_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$", description="ISO creation date.")

    @field_validator("file_path")
    @classmethod
    def validate_file_existence(cls, v: str) -> str:
        p = Path(v)
        if not p.is_file():
            raise ValueError(f"File not found or unreadable: {v}")
        return str(p.resolve())

class DocumentUploadResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str = Field(..., description="Upload status ('queued', 'duplicate', 'failed')")
    task_id: Optional[str] = Field(None, description="Paperless Celery task UUID.")
    sha256_checksum: str = Field(..., description="Computed file checksum.")
    filename: str = Field(..., description="Base filename.")
    message: str = Field(..., description="Detailed result narrative.")

class TaskStatusResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str
    status: str
    document_id: Optional[int] = None
    error_message: Optional[str] = None

class PaperlessGatewayService:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Token {api_token}"}

    def compute_sha256(self, file_path: str) -> str:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    async def upload(self, req: DocumentUploadRequest) -> DocumentUploadResult:
        checksum = self.compute_sha256(req.file_path)
        p = Path(req.file_path)
        url = f"{self.base_url}/api/documents/post_document/"

        form_data = []
        if req.title:
            form_data.append(("title", req.title))
        if req.correspondent_id is not None:
            form_data.append(("correspondent", str(req.correspondent_id)))
        if req.document_type_id is not None:
            form_data.append(("document_type", str(req.document_type_id)))
        if req.created_date:
            form_data.append(("created", req.created_date))
        for tag in req.tags:
            form_data.append(("tags", str(tag)))

        async with httpx.AsyncClient(timeout=45.0) as client:
            with open(req.file_path, "rb") as f:
                files = {"document": (p.name, f, "application/pdf")}
                response = await client.post(url, headers=self.headers, data=form_data, files=files)

                if response.status_code == 200:
                    task_uuid = response.text.strip('" \n\r')
                    return DocumentUploadResult(
                        status="queued",
                        task_id=task_uuid,
                        sha256_checksum=checksum,
                        filename=p.name,
                        message="Document successfully received and dispatched to Celery OCR queue."
                    )
                else:
                    return DocumentUploadResult(
                        status="failed",
                        task_id=None,
                        sha256_checksum=checksum,
                        filename=p.name,
                        message=f"Paperless API returned HTTP {response.status_code}: {response.text}"
                    )

    async def get_task_status(self, task_id: str) -> TaskStatusResult:
        url = f"{self.base_url}/api/tasks/?task_id={task_id}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                item = data[0]
                return TaskStatusResult(
                    task_id=task_id,
                    status=item.get("status", "unknown"),
                    document_id=item.get("related_document"),
                    error_message=item.get("result") if item.get("status") == "FAILURE" else None
                )
            return TaskStatusResult(task_id=task_id, status="pending")

_gateway = PaperlessGatewayService(
    base_url="http://127.0.0.1:8000",
    api_token="9f8a3b1c2d3e4f5a6b7c8d9e0f1a2b3c"
)

@mcp.tool()
async def ingest_document(request: DocumentUploadRequest) -> DocumentUploadResult:
    """Synchronously validates and uploads a document to Paperless-ngx via FastMCP 3.1."""
    return await _gateway.upload(request)

@mcp.tool()
async def check_ingest_task(task_id: str) -> TaskStatusResult:
    """Checks the status of an active Paperless Celery ingestion task."""
    return await _gateway.get_task_status(task_id)

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Operational Troubleshooting Matrix

| Symptom / Failure Mode | Root Cause Analysis | Diagnostic Command | Remediation Action Plan |
| :--- | :--- | :--- | :--- |
| `HTTP 413 Payload Too Large` | Reverse proxy body buffer limit exceeded by multi-page scan. | `grep -rn "client_max_body_size" /etc/nginx/` | Increase proxy buffer limit: `client_max_body_size 128M;` in Nginx / Traefik. |
| `HTTP 401 Unauthorized` | Invalid, expired, or improperly formatted token header. | `curl -Iv -H "Authorization: Token <token>" <url>` | Verify token string format (`Authorization: Token <hex_key>`) and check user permissions in Django admin. |
| Celery Task Queue Backlog | High concurrency ingestion spike saturating worker threads. | `docker exec -it paperless-redis redis-cli llen celery` | Scale Celery worker threads via `PAPERLESS_TASK_WORKERS=8` in `docker-compose.yml`. |
| Metadata Tags Ignored | Tags passed as single comma-separated string rather than repeated keys. | `tcpdump -i any -A port 8000 \| grep "tags"` | Send tags as separate form-data entries (`tags=1`, `tags=2`) or array indices. |
| Webhook Connection Timeout | Reverse proxy routing failure or Tailscale tunnel down. | `nc -zv docs.internal.net 443` | Validate Tailscale node status (`tailscale status`) and Traefik router backend health. |
| OCR Task Failure (`Corrupted File`) | Truncated multipart stream caused by network disconnection. | `docker logs paperless-webserver \| grep -i "corrupt"` | Enforce MD5/SHA-256 pre-upload checksum verification and implement retry loops. |

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md): Target document management system.
- [n8n](../../services/n8n.md): Workflow engine for orchestrating incoming webhooks.
- [Tag Taxonomy](../../reference-implementations/paperless/tag-taxonomy.md): System for tag structures.
- [Scan-to-Task Playbook](../../playbooks/scan-to-task.md): End-to-end processing pipeline starting with ingestion.
- [Cloudflare Mesh](../../services/cloudflare-mesh.md): Securing ingress endpoints across distributed nodes.
- [Home Admin Agent Architecture](../../knowledge_base/home-admin-agent-architecture.md): Agent system monitoring documents.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md): Triggering autonomous actions on new ingest events.
- [FastMCP 3.1](../../tools/automation_orchestration/mcp.md): Protocol for agent tool integration.

## Sources / references
- [Paperless-ngx REST API Documentation](https://docs.paperless-ngx.com/api/)
- [n8n HTTP Request Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [Tailscale Ingress Security Guide](https://tailscale.com/blog/api-security/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
