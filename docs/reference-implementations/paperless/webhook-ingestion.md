# Reference Implementation: Paperless-ngx Webhook Ingestion

## What it is
A guide and reference implementation for programmatically uploading documents to Paperless-ngx via its REST API and Model Context Protocol (FastMCP 3.1) endpoints. This method enables real-time document ingestion from external sources like mobile scanners, email bots, home-automation webhooks, or multi-agent orchestrators, bypassing the latency of standard folder polling.

## System Architecture

```
                                +-------------------------------------------------------+
                                |               External Ingestion Sources              |
                                |     (iOS Shortcuts / Email Gateway / n8n / Scanners)  |
                                +---------------------------+---------------------------+
                                                            |
                                                            v  HTTP Multipart POST
                                +-------------------------------------------------------+
                                |               Cloudflare / Reverse Proxy              |
                                |      (TLS Termination / Authentication Header Check)  |
                                +---------------------------+---------------------------+
                                                            |
                                                            v
                                +-------------------------------------------------------+
                                |                 Paperless-ngx Webhook                 |
                                |       (/api/documents/post_document/ Ingest API)      |
                                +---------------------------+---------------------------+
                                                            |
                                        +-------------------+-------------------+
                                        |                                       |
                                        v                                       v
                     +-------------------------------------+   +-------------------------------------+
                     |     PostgreSQL + Redis Queue        |   |     FastMCP 3.1 Task Protocol       |
                     |  (Metadata Tracking / Celery OCR)   |   |  (Synchronous Agent Event Dispatch) |
                     +-------------------------------------+   +-------------------------------------+
```

## Ingestion Event Handling & Retry Lifecycle

```
[External Scanner / Webhook Source]
               |
               v
  [FastMCP 3.1 Ingestion Router]
               |
               +---> Validate Payload Schema (Pydantic v2)
               |           |
               |           +---> (Schema Error) -> Return HTTP 400 Bad Request
               |
               v
  [Paperless REST Endpoint] (/api/documents/post_document/)
               |
               +---> Transmit Multipart Body + Authorization Header
               |           |
               |           +---> (413 / 500 Error) -> Retry Exponential Backoff (3x)
               |
               v
  [Celery Redis Task Queue]
               |
               v
  [OCR Processing & FastMCP Dispatch Signal] ---> [Agent Trigger Engine]
```

## What problem it solves
Standard Paperless-ngx ingestion relies on consumption folder polling, which introduces delays (up to several minutes) between scanning a document and its availability in the index. Webhook ingestion enables a real-time "push" architecture, providing instantaneous document ingestion, immediate HTTP feedback, and synchronous metadata application (tags, correspondent, document type, created date).

## Where it fits in the stack
This implementation sits at the **Intake/Ingress layer**. It connects **External Sources** (n8n, mobile shortcuts, email gateways, edge sensors) to the **Document Management System** (Paperless-ngx) and downstream **AI Processing Engines** (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**).

## Key Feature Comparison Matrix

| Ingestion Method | Webhook Push Ingestion | Directory Polling | Email Import Gateway | FastMCP Tool Upload |
| :--- | :--- | :--- | :--- | :--- |
| **Ingestion Latency** | Immediate (<500ms) | Polling Interval (1–5 min) | Polling Interval (1–3 min) | Immediate (<300ms) |
| **Metadata Injection** | Synchronous during upload | Post-OCR auto-matching | Header / Subject regex | Synchronous Pydantic validated |
| **Network Direction** | Inbound Push (HTTP POST) | Local File IO Mount | Inbound IMAP Polling | Bidirectional JSON-RPC |
| **Error Handling** | Synchronous HTTP status | Log file inspection | Email bounce notification | Structured JSON response |
| **Authentication** | Bearer / Token Auth Header | Filesystem permissions | IMAP Credentials | FastMCP Auth Header |
| **Throughput Capacity** | 100+ req/min parallel | Bound by FS I/O scan rate | Dependent on IMAP Server | High-concurrency Async IO |
| **Payload Security** | TLS + Token Verification | Local ACL File Permissions | TLS IMAP Connection | Token / Mutual TLS |

## Typical use cases
- **Mobile Scan-to-Cloud**: iOS Shortcuts or Android shares POSTing image/PDF payloads directly to Paperless via secure tunnel.
- **Email Ingestion Gateway**: Automated scripts monitoring inboxes (`invoices@domain.com`) and pushing attachments with pre-parsed headers.
- **Automated Web Downloads**: Scheduled utility/banking retrieval scripts pushing PDFs directly upon download.
- **Real-Time Agent Triggering**: Triggering **Claude 5.6** or **GPT-5.6** agentic routines the second a document is ingested via Model Context Protocol (FastMCP 3.1) hooks.

## Strengths
- **Low Latency**: Sub-second ingestion and instant indexing.
- **Synchronous Metadata Injection**: Tags, title, correspondent, and document type applied during upload rather than post-OCR.
- **Deterministic Feedback**: Immediate HTTP 200/400 status codes provided to sending systems or n8n nodes.
- **Agent Integration**: Seamlessly interfaces with **FastMCP 3.1** servers for tool-calling models.

## Limitations
- **Token Management**: Requires secure storage and rotation of Paperless API authorization tokens.
- **Network Ingress**: Server or reverse proxy (e.g., Cloudflare Tunnel / Tailscale) must accept incoming POST payloads securely.
- **Payload Limits**: Large PDF scans require tuning web server upload body limits (`client_max_body_size 100M;`).

## When to use it
- When building real-time ingestion pipelines in n8n, Node-RED, or custom Python microservices.
- When instant availability of documents is required for downstream agentic workflows.
- For multi-site or remote scanning devices pushing documents over HTTPS or mesh networks.

## When not to use it
- For basic home setups where a 5-minute folder polling delay is acceptable.
- When source devices cannot execute HTTP multipart form requests.

## Getting started
1. Generate an API token in the Paperless-ngx Django admin panel (`/admin/authtoken/token/`).
2. Verify instance connectivity via HTTPS or Tailscale.
3. Perform a test upload using `curl` or the provided FastMCP 3.1 Python integration.
4. Integrate the payload format into n8n or your agent framework.

## CLI examples

### 1. Basic Ingestion via Curl
```bash
curl -X POST https://paperless.home.arpa/api/documents/post_document/ \
     -H "Authorization: Token 9f8a3b1c2d3e4f5a6b7c8d9e0f1a2b3c" \
     -F "document=@/path/to/invoice.pdf;type=application/pdf" \
     -F "title=2027-01 Electric Utility Bill" \
     -F "tags=4" \
     -F "correspondent=12" \
     -F "document_type=3"
```

### 2. Ingestion with Custom Created Date and Auto-Matching
```bash
curl -X POST https://paperless.home.arpa/api/documents/post_document/ \
     -H "Authorization: Token 9f8a3b1c2d3e4f5a6b7c8d9e0f1a2b3c" \
     -F "document=@/path/to/receipt.pdf" \
     -F "created=2027-01-07T14:30:00Z" \
     -F "archive_serial_number=10042" \
     -F "tags=1,8,15"
```

## API examples

The following Python script uses **Pydantic v2** for schema validation and FastMCP 3.1 patterns to perform synchronous document uploads and metadata parsing.

```python
import asyncio
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import httpx
from pydantic import BaseModel, Field, ConfigDict, field_validator
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("paperless-webhook-gateway", version="3.1.0")


class PaperlessIngestRequest(BaseModel):
    """Schema for validating document ingestion parameters."""
    model_config = ConfigDict(arbitrary_types_allowed=True, str_strip_whitespace=True)

    file_path: Path = Field(..., description="Absolute path to the local document file.")
    title: Optional[str] = Field(default=None, max_length=128, description="Custom document title.")
    tags: List[int] = Field(default_factory=list, description="List of tag IDs to assign.")
    correspondent: Optional[int] = Field(default=None, description="Correspondent ID.")
    document_type: Optional[int] = Field(default=None, description="Document type ID.")
    created_date: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$", description="ISO date YYYY-MM-DD.")

    @field_validator("file_path")
    @classmethod
    def validate_path(cls, v: Path) -> Path:
        if not v.exists():
            raise ValueError(f"File path does not exist: {v}")
        return v


class PaperlessIngestResponse(BaseModel):
    """Schema for validating API response from Paperless-ngx."""
    model_config = ConfigDict(str_strip_whitespace=True)

    task_id: str = Field(..., description="UUID task token for tracking document consumption.")
    status: str = Field(default="queued", description="Ingestion queue status.")


class PaperlessWebhookClient:
    """Client for performing synchronous multipart uploads to Paperless-ngx."""

    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Token {api_token}"}

    async def upload_document(self, request: PaperlessIngestRequest) -> PaperlessIngestResponse:
        """Uploads a document with validated metadata via multipart/form-data."""
        endpoint = f"{self.base_url}/api/documents/post_document/"

        data = {}
        if request.title:
            data["title"] = request.title
        if request.correspondent:
            data["correspondent"] = str(request.correspondent)
        if request.document_type:
            data["document_type"] = str(request.document_type)
        if request.created_date:
            data["created"] = request.created_date

        form_data = []
        for tag in request.tags:
            form_data.append(("tags", str(tag)))
        for k, v in data.items():
            form_data.append((k, v))

        async with httpx.AsyncClient(timeout=30.0) as client:
            with open(request.file_path, "rb") as f:
                files = {"document": (request.file_path.name, f, "application/pdf")}
                response = await client.post(endpoint, headers=self.headers, data=form_data, files=files)
                response.raise_for_status()

                task_id = response.text.strip('" \n\r')
                return PaperlessIngestResponse(task_id=task_id, status="queued")


@mcp.tool()
async def ingest_paperless_document(request_json: str) -> str:
    """FastMCP tool endpoint to validate and upload a document to Paperless-ngx."""
    try:
        data = json.loads(request_json)
        req = PaperlessIngestRequest.model_validate(data)

        # In production, replace with vault environment lookup
        client = PaperlessWebhookClient(
            base_url="https://paperless.home.arpa",
            api_token="9f8a3b1c2d3e4f5a6b7c8d9e0f1a2b3c"
        )
        res = await client.upload_document(req)
        return res.model_dump_json(indent=2)
    except Exception as e:
        return json.dumps({"status": "ERROR", "error": str(e)})


if __name__ == "__main__":
    mcp.run()
```

## Systemd Ingestion Gateway Service

For production environment execution, run the Paperless FastMCP Ingestion Gateway as a systemd service:

```ini
[Unit]
Description=Paperless-ngx Webhook Ingestion FastMCP Gateway
After=network.target paperless-webserver.service
Wants=paperless-webserver.service

[Service]
Type=simple
User=paperless-gateway
Group=paperless-gateway
WorkingDirectory=/opt/paperless-gateway
ExecStart=/opt/paperless-gateway/venv/bin/python -m gateway.server
Restart=always
RestartSec=5s

# Environment secrets
Environment=PAPERLESS_URL=https://paperless.home.arpa
EnvironmentFile=/etc/default/paperless-gateway

# Security Hardening
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/paperless-gateway/tmp /var/log/paperless-gateway
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Operational Best Practices & Troubleshooting

### Operational Guidance
1. **Reverse Proxy Configuration**: Ensure reverse proxies (Nginx/Traefik) have `client_max_body_size` set to at least `100M` to accommodate multi-page high-resolution PDF uploads.
2. **Token Security**: Store API authorization tokens in environment variables or secret vaults rather than hardcoding in client scripts.
3. **Queue Health**: Monitor Redis queue depth on Paperless-ngx instances when receiving heavy concurrent webhook spikes.

### Common Troubleshooting Scenarios

| Symptom / Issue | Root Cause | Resolution Strategy |
| :--- | :--- | :--- |
| `HTTP 413 Payload Too Large` | Reverse proxy body size limit exceeded | Increase `client_max_body_size 100M;` in Nginx / Traefik config. |
| `HTTP 401 Unauthorized` | Invalid or missing token header | Verify token header format (`Authorization: Token <token_hash>`). |
| Celery task execution backlog | High concurrent document ingest rate | Scale Celery worker threads (`PAPERLESS_WEBSERVER_WORKERS=4`). |
| Ingestion metadata tags ignored | Form parameter name mismatch | Pass `tags` as repeated form fields or array indices (`tags=1&tags=2`). |
| Webhook connection timeout | Unreachable Paperless hostname | Verify Tailscale / Cloudflare tunnel routing to local container port. |

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
