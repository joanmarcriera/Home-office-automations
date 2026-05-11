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

## Strengths
- **Low Latency**: Near-instantaneous ingestion.
- **Direct Metadata Injection**: Allows applying tags, titles, and dates at the moment of upload.
- **Improved Reliability**: Provides immediate HTTP success/failure codes to the sending system.

## Limitations
- **Token Management**: Requires secure handling of API tokens.
- **Complexity**: Slightly more complex to set up than a simple shared folder.

## When to use it
- When building automated intake pipelines in n8n or Node-RED.
- When real-time availability of the document is required (e.g., for an agent to process it immediately).
- For distributed setups where the scanner and Paperless server are on different networks.

## When not to use it
- For simple home setups where a 5-minute polling delay is acceptable.
- If the source system does not support multipart form-data POST requests.

## Configuration

### API Endpoint
`POST /api/documents/post_document/`

### Authentication
Requires an `Authorization: Token <YOUR_API_TOKEN>` header.

### Multipart Form Data Fields
- `document`: The file to upload.
- `title` (optional): Override the filename.
- `created` (optional): ISO8601 date.
- `tags` (optional): List of tag IDs.

## cURL Example
```bash
curl -H "Authorization: Token your_token_here" \
     -F "document=@/path/to/your/document.pdf" \
     -F "title=Utility Bill" \
     -X POST http://your-paperless-ip:8000/api/documents/post_document/
```

## n8n Implementation
Use the **HTTP Request** node:
- **Method**: POST
- **URL**: `http://paperless:8000/api/documents/post_document/`
- **Authentication**: Header Auth (`Authorization`)
- **Send Binary Data**: Yes
- **Body Content Type**: Multipart Form-Data

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md): The target document management system.
- [n8n](../../services/n8n.md): The ideal platform for orchestrating these webhooks.
- [Tag Taxonomy](../../reference-implementations/paperless/tag-taxonomy.md): Deciding which tags to apply during ingestion.
- [Scan-to-Task Playbook](../../playbooks/scan-to-task.md): A workflow that begins with webhook ingestion.
- [Cloudflare Mesh](../../services/cloudflare-mesh.md): Securing the webhook endpoint if exposed to the internet.
- [Home Admin Agent Architecture](../../knowledge_base/home-admin-agent-architecture.md): The system that monitors for new documents.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md): Triggering agent actions upon successful ingestion.

## Sources / References
- [Paperless-ngx API Docs](https://docs.paperless-ngx.com/api/)
- [n8n HTTP Request Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
