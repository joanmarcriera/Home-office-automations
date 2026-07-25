# Reference Implementation: Paperless-ngx Webhook Ingestion

## What it is
A guide and set of examples for programmatically uploading documents to Paperless-ngx via its REST API. This method allows for real-time document ingestion from external sources like mobile scanners, email bots, or automated webhooks, bypassing the latency of standard folder polling.

## What problem it solves
Standard Paperless-ngx ingestion often relies on "consumption folders" which are polled at intervals. This can introduce delays (up to several minutes) between scanning a document and its appearance in the system. Webhook ingestion enables "push" architecture, allowing for instantaneous processing and immediate feedback to the user or triggering agent.

## Where it fits in the stack
This implementation sits at the **Intake/Ingress layer**. It connects **External Sources** (n8n, mobile apps, email gateways) to the **Document Management System** (Paperless-ngx).

## Typical use cases
- **Mobile Scan-to-Cloud**: A shortcut on a phone that captures an image and POSTs it directly to the server.
- **Email Gateway**: A script that monitors an "invoices@" inbox and pushes attachments to Paperless.
- **Automated Web Downloads**: A script that downloads monthly utility bills and uploads them with pre-applied tags.
- **Real-time Agent Analysis**: Triggering a **Claude 5.1** or **GPT-5.5** agent to analyze a document the moment it is scanned.

## Strengths
- **Low Latency**: Near-instantaneous ingestion.
- **Direct Metadata Injection**: Allows applying tags, titles, and dates at the moment of upload.
- **Improved Reliability**: Provides immediate HTTP success/failure codes to the sending system.
- **Agent Integration**: Seamlessly connects to the **Model Context Protocol (MCP 3.1)** for automated processing.

## Limitations
- **Token Management**: Requires secure handling of API tokens.
- **Complexity**: Slightly more complex to set up than a simple shared folder.
- **Payload Limits**: Large files may require tuning of the web server (e.g., Nginx) `client_max_body_size`.

## When to use it
- When building automated intake pipelines in n8n or Node-RED.
- When real-time availability of the document is required (e.g., for an agent to process it immediately).
- For distributed setups where the scanner and Paperless server are on different networks.

## When not to use it
- For simple home setups where a 5-minute polling delay is acceptable.
- If the source system does not support multipart form-data POST requests.

## Getting started
1. Generate an API token in the Paperless-ngx Django admin panel.
2. Ensure your Paperless instance is accessible via HTTPS or a secure tunnel (Tailscale).
3. Test connectivity using the `curl` example provided in the CLI section.
4. Integrate the upload logic into your mobile app, script, or n8n workflow.

## CLI examples
Use `curl` to perform a manual upload for testing.

```bash
# Upload a PDF with metadata
curl -H "Authorization: Token your_token_here" \
     -F "document=@/path/to/your/document.pdf" \
     -F "title=Utility Bill" \
     -F "tags=1,2,3" \
     -X POST https://your-paperless-url/api/documents/post_document/
```

## API examples
The **Model Context Protocol (MCP 3.1)** provides a standardized way for agents to perform this upload.

### Python Integration
Below is a modern asynchronous implementation using Python to upload a document to Paperless-ngx, fully compatible with late August 2026 developer guidelines.

```python
import asyncio
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PaperlessIngestion")

class DocumentUploadRequest(BaseModel):
    filepath: str = Field(..., description="Local system path to the document file")
    title: Optional[str] = Field(None, description="Custom title for the uploaded document")
    tags: List[int] = Field(default_factory=list, description="List of integer Tag IDs in Paperless")

async def upload_document(endpoint_url: str, api_token: str, upload_req: DocumentUploadRequest) -> bool:
    """
    Asynchronously uploads a document to Paperless-ngx REST API.
    Aligned with MCP 3.1 tooling requirements.
    """
    headers = {
        "Authorization": f"Token {api_token}"
    }

    # We construct a multipart form payload
    data = aiohttp.FormData()
    if upload_req.title:
        data.add_field("title", upload_req.title)
    if upload_req.tags:
        # Paperless expects multiple tags as separate fields or comma-separated depending on implementation
        for tag in upload_req.tags:
            data.add_field("tags", str(tag))

    try:
        # Read file binary payload
        with open(upload_req.filepath, "rb") as f:
            data.add_field("document", f, filename=upload_req.filepath.split("/")[-1])

            async with aiohttp.ClientSession() as session:
                logger.info(f"Uploading {upload_req.filepath} to {endpoint_url}...")
                async with session.post(f"{endpoint_url}/api/documents/post_document/", headers=headers, data=data, timeout=30) as resp:
                    if resp.status in (200, 201):
                        resp_json = await resp.json()
                        logger.info(f"Ingestion successful! Response: {resp_json}")
                        return True
                    else:
                        resp_text = await resp.text()
                        logger.error(f"Paperless API error ({resp.status}): {resp_text}")
                        return False
    except FileNotFoundError:
        logger.error(f"File not found: {upload_req.filepath}")
        return False
    except Exception as e:
        logger.error(f"Failed to complete webhook ingestion: {e}")
        return False

if __name__ == "__main__":
    request_data = DocumentUploadRequest(
        filepath="sample_bill.pdf",
        title="Utility Bill August 2026",
        tags=[4, 12]
    )
    # asyncio.run(upload_document("https://paperless.local", "secure_token", request_data))
```

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md): The target document management system.
- [n8n](../../services/n8n.md): The ideal platform for orchestrating these webhooks.
- [Tag Taxonomy](../../reference-implementations/paperless/tag-taxonomy.md): Deciding which tags to apply during ingestion.
- [Scan-to-Task Playbook](../../playbooks/scan-to-task.md): A workflow that begins with webhook ingestion.
- [Cloudflare Mesh](../../services/cloudflare-mesh.md): Securing the webhook endpoint if exposed to the internet.
- [Home Admin Agent Architecture](../../knowledge_base/home-admin-agent-architecture.md): The system that monitors for new documents.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md): Triggering agent actions upon successful ingestion.
- [Claude Code](../../tools/development_ops/claude-code.md): The CLI tool used to manage these integrations.
- [MCP](../../tools/automation_orchestration/mcp.md) — Standardized protocol for model-tool interaction.

## Sources / references
- [Paperless-ngx REST API Documentation](https://docs.paperless-ngx.com/api/)
- [n8n HTTP Request Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [Tailscale API Access Control](https://tailscale.com/blog/api-security/)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
