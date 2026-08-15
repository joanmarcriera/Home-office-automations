# Reference Implementation: Paperless-ngx Webhook Ingestion

## What it is
A reference implementation and architecture guide for real-time document ingestion into Paperless-ngx (v2.14+) via its REST API and automated webhooks. This pattern bypasses filesystem polling latency, enabling instant document intake from scanners, email automation bots, mobile shortcuts, and agentic workflows using **FastMCP 3.1**.

## What problem it solves
Standard Paperless-ngx intake relies on asynchronous "consumption folder" polling, which can introduce multi-minute delays. Webhook and API-driven ingestion provides a low-latency "push" architecture. It ensures instant ingestion feedback, enables transactional metadata assignment (titles, correspondents, document types, tags), and immediately triggers downstream multi-agent analysis powered by **Claude 5.1**, **GPT-5.5**, or **Gemini 4.0 Pro**.

## Where it fits in the stack
**Intake / Ingress Layer**. It sits at the entry point of the document processing pipeline, connecting external intake drivers (n8n, mobile apps, email gateways, cloud storage hooks) to **Paperless-ngx** and downstream [KnowledgeOps](../../knowledge_base/multi_agent_knowledgeops.md) databases.

## Typical use cases
- **Mobile Scan-to-Cloud**: Direct capture from mobile devices POSTing multi-page scans directly to the Paperless API endpoint.
- **Email Ingestion Gateway**: Serverless script or n8n workflow monitoring incoming emails and uploading attachments with auto-parsed metadata.
- **Real-time Agentic Processing**: Triggering **Claude 5.1** or **GPT-5.5** via FastMCP 3.1 to summarize, classify, and create tasks (e.g., in Vikunja or Home Assistant) immediately upon document arrival.
- **Financial Document Pipelines**: Ingesting bank statements or receipts with pre-assigned tags (`tax-2027`, `needs-review`).

## Strengths
- **Instant Processing**: Eliminates folder consumption polling delays.
- **Atomic Metadata Tagging**: Assigns correspondents, tags, custom fields, and creation dates in the single upload payload.
- **Transactional Status Feedback**: Returns HTTP status codes and task IDs (`/api/tasks/`) for reliable exception handling in orchestrators like n8n or Temporal.
- **FastMCP 3.1 Compliance**: Seamlessly exposes document upload tools to LLM agents for autonomous file management.

## Limitations
- **Token Security**: Requires secure storage and lifecycle management for Paperless-ngx API tokens (e.g., in HashiCorp Vault).
- **Payload Constraints**: High-resolution image uploads require configuring web proxy body size limits (e.g., Nginx/Traefik `client_max_body_size 50M`).

## When to use it
- When real-time availability of ingested documents is required for automated downstream processing.
- When orchestrating complex intake workflows via n8n, Node-RED, or custom Python scripts.
- For multi-site setups where edge scanners upload to a central server across Tailscale or HTTPS boundaries.

## When not to use it
- For basic home setups where a 5-minute directory polling loop is acceptable.
- When the document source cannot send HTTP POST multipart requests.

## Getting started
1. Generate an API Auth Token in Paperless-ngx (`Settings -> Auth Tokens`).
2. Verify network connectivity to the Paperless REST API endpoint (`https://paperless.home.arpa/api/documents/post_document/`).
3. Execute the `curl` test script below to verify token permissions and response handling.
4. Integrate the Python Pydantic v2 ingestion schema into your intake agent or webhook listener.

## CLI examples

Upload a PDF with metadata via `curl`:

```bash
curl -X POST https://paperless.home.arpa/api/documents/post_document/ \
     -H "Authorization: Token YOUR_PAPERLESS_API_TOKEN" \
     -F "document=@/path/to/invoice.pdf" \
     -F "title=Utility Invoice Jan 2027" \
     -F "correspondent=4" \
     -F "document_type=2" \
     -F "tags=12,15"
```

## API examples

### Strict Pydantic v2 Webhook Payload Schema & FastAPI Ingestion Endpoint

```python
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
import httpx

app = FastAPI(title="Paperless Webhook Ingestion Portal", version="2027.1")

class PaperlessIngestMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str = Field(description="Document title")
    correspondent_id: Optional[int] = Field(default=None, description="Paperless correspondent ID")
    document_type_id: Optional[int] = Field(default=None, description="Paperless document type ID")
    tag_ids: List[int] = Field(default_factory=list, description="List of tag IDs to apply")
    archive_serial_number: Optional[int] = Field(default=None)

class IngestResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: str
    task_id: str = Field(description="Paperless async task tracking UUID")
    message: str

PAPERLESS_URL = "https://paperless.home.arpa/api/documents/post_document/"
PAPERLESS_TOKEN = "env_paperless_token_secret"

@app.post("/api/v1/ingest", response_model=IngestResponse)
async def ingest_document(
    title: str,
    tag_ids: str = "12",
    file: UploadFile = File(...)
):
    """Webhook listener that validates and forwards incoming documents to Paperless-ngx."""
    tags = [int(t.strip()) for t in tag_ids.split(",") if t.strip().isdigit()]
    metadata = PaperlessIngestMetadata(title=title, tag_ids=tags)

    file_content = await file.read()

    files = {"document": (file.filename, file_content, file.content_type)}
    data = {
        "title": metadata.title,
        "tags": [str(tid) for tid in metadata.tag_ids]
    }
    headers = {"Authorization": f"Token {PAPERLESS_TOKEN}"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(PAPERLESS_URL, data=data, files=files, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        task_id = response.json() if isinstance(response.json(), str) else response.json().get("task_id", "completed")
        return IngestResponse(
            status="success",
            task_id=str(task_id),
            message="Document successfully queued for consumption."
        )

# Example output schema format verification
if __name__ == "__main__":
    test_meta = PaperlessIngestMetadata(title="Sample Invoice", tag_ids=[1, 2])
    print("Schema Test:", test_meta.model_dump_json(indent=2))
```

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md) — The target document management system.
- [n8n](../../services/n8n.md) — Orchestrator for incoming webhook events.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Agentic protocol for AI tools.
- [Scan-to-Task Playbook](../../playbooks/scan-to-task.md) — Automated task creation from scanned documents.
- [Tailscale](../../playbooks/tailscale-to-headscale-migration.md) — Secure networking mesh for private API endpoints.

## Sources / references
- [Paperless-ngx API Documentation](https://docs.paperless-ngx.com/api/)
- [FastAPI Upload File Documentation](https://fastapi.tiangolo.com/tutorial/request-files/)
- [Pydantic v2 Model Configuration](https://docs.pydantic.dev/latest/concepts/config/)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
