# Reference Implementation: Paperless Tag Taxonomy

## What it is
A hierarchical tagging system designed for Paperless-ngx that organizes personal and household documents into actionable categories. It balances organizational needs (folders/categories) with workflow states (status/actions). As of January 2027, it is optimized for high-reasoning models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4** to perform autonomous classification and lifecycle management via **FastMCP 3.1** interfaces.

```
+---------------------------------------------------------------------------------------------------+
|                                PAPERLESS TAXONOMY LIFECYCLE TOPOLOGY                              |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +---------------------------+       +---------------------------------------------------------+  |
|  | Document Ingestion Stream | ----> | Inbox State Processing Engine                           |  |
|  | (Scanner, Email, Webhook) |       | (Tag: `inbox` / Unprocessed Storage Path)              |  |
|  +---------------------------+       +---------------------------------------------------------+  |
|                                                                  |                                |
|                                                                  v                                |
|                                      +---------------------------------------------------------+  |
|                                      | FastMCP 3.1 Agent Classification Engine                  |  |
|                                      | (Claude 5.6 / GPT-5.6 / DeepSeek-V4 Metadata Extraction)|  |
|                                      +---------------------------------------------------------+  |
|                                         /                      |                      \           |
|                                        v                       v                       v          |
|                       +------------------+    +------------------+    +------------------+        |
|                       | Status: Action   |    | Category Tagging |    | Retention Tagging|        |
|                       | `needs-action`   |    | `Finance/Bill`   |    | `Keep-7-years`   |        |
|                       +------------------+    +------------------+    +------------------+        |
|                                        \                       |                      /           |
|                                         +----------------------+---------------------+            |
|                                                                |                                  |
|                                                                v                                  |
|  +---------------------------+       +---------------------------------------------------------+  |
|  | Downstream Integration    | <---- | State Transition & Archival Emitter                     |  |
|  | Vikunja Task / n8n Flow   |       | (Tag: `processed` / Long-Term Paperless Storage Template)|  |
|  +---------------------------+       +---------------------------------------------------------+  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## What problem it solves
Flat document storage quickly becomes unmanageable as volume grows. Without a standardized taxonomy, users struggle to find files, and automated agents cannot reliably trigger specific workflows (like paying a bill or extracting a warranty). This taxonomy provides the "semantic hooks" necessary for both humans and machines to navigate the archive, ensuring that "Invisible Kubernetes" and "Agentic Workflows" have structured data to act upon.

Furthermore, ambiguous tag naming causes LLM categorization agents to hallucinate duplicate tags (e.g., creating `bills`, `Invoice`, and `Financial/Receipt`). This reference implementation enforces a strict, machine-enforceable taxonomy contract that restricts tag mutation and guarantees predictable document routing.

## Where it fits in the stack
The taxonomy sits at the **Organization/Metadata layer** of the document management system. It acts as the primary index used by **Search**, **Automated Workflows** (n8n, Python scripts), and **AI Agents** (leveraging **FastMCP 3.1**) to filter and process documents.

```
+---------------------------------------------------------------------------------------------------+
|                                 DOCUMENT ARCHITECTURE LAYERING                                    |
+---------------------------------------------------------------------------------------------------+
|  Agent Orchestration  |  FastMCP 3.1 Tools / Home Admin Agent / Vikunja Task Dispatcher          |
+-----------------------+---------------------------------------------------------------------------+
|  METADATA TAXONOMY    |  PAPERLESS TAG TAXONOMY (State Tags / Category Hierarchy / Retention)     |
+-----------------------+---------------------------------------------------------------------------+
|  Storage & Indexing   |  Paperless-ngx Core / PostgreSQL DB / xapian Search Engine / Redis        |
+-----------------------+---------------------------------------------------------------------------+
|  Ingestion Drivers    |  OCRmyPDF / Tesseract v5.5 / Paperless-AI / Email Poller                  |
+---------------------------------------------------------------------------------------------------+
```

### Taxonomy Structure & Matching Matrix
The table below specifies the standardized taxonomy tiers, color conventions, and matching behaviors:

| Tag Name | Taxonomy Layer | Purpose & Meaning | Default UI Color | Matching Algorithm |
| :--- | :--- | :--- | :--- | :--- |
| `inbox` | State | Newly ingested, unverified document awaiting agent classification. | `#e67e22` (Orange) | Auto |
| `needs-action` | State | Document requires pending human or automated task resolution (e.g. pay bill). | `#e74c3c` (Red) | Exact |
| `processed` | State | Fully processed, indexed, and archived document. | `#2ecc71` (Green) | Exact |
| `Finance/Bill` | Category | Invoices, utility bills, and payment requests. | `#3498db` (Blue) | Any ("Invoice", "Bill", "Due") |
| `Admin/Warranty` | Category | Product purchase receipts, guarantee certificates, and manuals. | `#9b59b6` (Purple) | Any ("Warranty", "Guarantee") |
| `Keep-7-years` | Retention | Compliance flag for tax-deductible or audit records. | `#34495e` (Dark Gray) | Exact |

## Typical use cases
- **Workflow Automation**: Moving a document from `inbox` to `needs-action` to trigger a reminder in [Vikunja](../../services/vikunja.md).
- **Tax Preparation**: Quickly retrieving all documents tagged with `Keep-7-years` or `Finance/Bill` for annual audits.
- **Legacy Preservation**: Categorizing scanned physical photos and historical records for long-term archiving using [Immich](../../services/immich.md) integration patterns.
- **Agentic Routing**: Using **Qwen 3.6 VL** or **DeepSeek-V4** to analyze document sentiment and apply urgent status tags for immediate human attention.
- **Warranty Expiration Tracking**: Extracting purchase dates from receipts tagged `Admin/Warranty` and adding expiration alerts to Google Calendar or Vikunja.

## Strengths
- **Action-Oriented**: Clearly separates "State" (what needs to be done) from "Category" (what the document is).
- **Extensible**: The `Category/Subcategory` pattern allows for infinite growth without breaking existing logic or n8n workflows.
- **Machine-Readable**: Simple, consistent naming conventions are easy for LLMs and scripts to parse via the Paperless REST API.
- **FastMCP 3.1 Compatibility**: Designed to be exposed via FastMCP servers to agentic IDEs and autonomous household assistants.
- **Deterministic Archival**: Eliminates orphaned files and forgotten bills through systematic state transition loops.

## Limitations
- **Maintenance**: Requires discipline to ensure every document is tagged correctly, though auto-tagging with **Claude 5.6** and **GPT-5.6** has mitigated this significantly.
- **Tool Support**: While ideal for Paperless-ngx, other DMS tools may have different tagging limitations or lack hierarchical support.
- **Over-Categorization**: Risk of creating too many niche tags that humans won't remember to use, necessitating agentic "Tag Cleanup" routines.

## Troubleshooting & Diagnostics Matrix

| Issue / Error Symptom | Probable Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| `Duplicate Tag Sprawl (Finance/Bills vs Finance/Bill)` | LLM Agent prompt lacks exact tag enum constraints | Enforce strict tag validation via Pydantic schema in the FastMCP 3.1 middleware tool. |
| `Document Stuck in inbox State` | Paperless auto-matching rule failed to match document OCR text | Run manual tag assignment or execute `document_index reindex` to re-extract OCR content. |
| `403 Forbidden on Tag PATCH API` | Paperless API token lacks edit permissions for state tags | Ensure API user token possesses `document_change` and `tag_change` global permissions. |
| `Vikunja Task Creation Failure` | Missing `needs-action` tag webhook handler in n8n pipeline | Verify n8n webhook node listener URL matches Paperless post-consumption trigger payload. |

## Operational Best Practices & Guardrails
- **Restrict Inbox Tag Auto-Removal**: Configure Paperless-ngx matching algorithms so the `inbox` tag is only stripped when an explicit classification payload is received from the agent.
- **Color-Code Taxonomy Layers**: Assign distinct color families in Paperless (e.g., Warm colors for State tags, Cool colors for Categories, Grayscale for Retention).
- **Run Monthly Orphan Audits**: Execute `document_index --tags=none` periodically to catch documents that bypassed auto-matching rules.
- **Tag Mutation Mutex Locking**: Ensure concurrent agent classification workers apply tag mutations sequentially to prevent race conditions during bulk ingestion.

## When to use it
- When setting up a new Paperless-ngx instance for household or small office use.
- When designing automated "Scan-to-Action" pipelines that require high-precision routing.
- For managing multi-generational family archives with high-volume ingest from scanners and email.

## When not to use it
- For extremely small document sets (under 100 files) where a simple full-text search is sufficient.
- If using a DMS that relies entirely on vector-based search without robust tagging support.

## Getting started
1. **Initial Tag Creation**: Create core status tags (`inbox`, `needs-action`, `processed`) in the Paperless-ngx UI or via API.
2. **Category Hierarchy**: Establish top-level categories using the `Category/Subcategory` naming convention (e.g., `Finance/Bill`).
3. **Matching Rules**: Configure Paperless-ngx "Matching Algorithms" to automatically apply tags based on document content (e.g., "Any" match for "Invoice" applies `Finance/Bill`).
4. **Agentic Onboarding**: Point your Home Admin Agent to the taxonomy documentation so it understands the routing logic.

## CLI examples
These commands are executed within the Paperless-ngx environment to maintain taxonomy integrity.

```bash
# Rename files on disk based on the new taxonomy and storage templates
docker exec -it paperless-webserver python3 manage.py document_renamer

# Reindex the search engine after a bulk tag migration or update
docker exec -it paperless-webserver python3 manage.py document_index reindex

# Sanity check for documents without any tags (taxonomy gaps)
docker exec -it paperless-webserver python3 manage.py document_index --tags=none
```

### Exporting Current Taxonomy Tags
```bash
docker exec -it paperless-webserver python3 manage.py document_exporter --export-tags-only /tmp/tags.json
```

## API examples
The Paperless-ngx REST API is the primary interface for agents to interact with the taxonomy.

### List all tags
```bash
curl -X GET http://localhost:8000/api/tags/ \
  -H "Authorization: Token your_api_token"
```

### Filter documents by status and category
```bash
# Find all bills that still need action
curl -X GET "http://localhost:8000/api/documents/?tags__name__all=needs-action,Finance/Bill" \
  -H "Authorization: Token your_api_token"
```

### Update document tags programmatically
```bash
curl -X PATCH http://localhost:8000/api/documents/123/ \
  -H "Authorization: Token your_api_token" \
  -H "Content-Type: application/json" \
  -d '{"tags": [1, 5, 10]}'
```

### Python Programmatic Tag Syncer & Validator (FastMCP 3.1 / Pydantic v2)
Use this programmatic script with strict **Pydantic v2** schemas to synchronize tax tags from your master list to Paperless-ngx while validating matching rules and payload structures within a FastMCP 3.1 tool endpoint.

```python
import sys
import requests
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PaperlessTaxonomyServer", version="3.1.0")

class PaperlessTagCreate(BaseModel):
    """Pydantic v2 model for validating Paperless tag creation payloads."""
    name: str = Field(..., description="Tag name (e.g., 'Finance/Bill' or 'needs-action')")
    color: str = Field(default="#008080", description="Hex color code for tag UI badge")
    matching_algorithm: int = Field(default=1, ge=0, le=6, description="Matching algorithm (1 = Auto, 6 = Exact)")
    is_inbox_tag: bool = Field(default=False, description="Flag indicating if tag acts as inbox state")

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, v: str) -> str:
        if not v.startswith("#") or len(v) not in (4, 7):
            raise ValueError(f"Invalid hex color string: {v}")
        return v

class TagSyncConfig(BaseModel):
    """Pydantic v2 config model for taxonomy synchronization."""
    api_url: str = Field(..., description="Paperless REST API endpoint base URL")
    token: str = Field(..., description="Paperless REST API authorization token")
    tag_mapping: Dict[str, str] = Field(..., description="Mapping of tag names to hex colors")

@mcp.tool()
def sync_taxonomy_tags(config_dict: dict) -> dict:
    """FastMCP tool step executing Paperless taxonomy synchronization with Pydantic v2 validation."""
    try:
        config = TagSyncConfig.model_validate(config_dict)
    except ValidationError as e:
        return {"status": "validation_error", "errors": e.errors(include_url=False)}

    headers = {
        "Authorization": f"Token {config.token}",
        "Content-Type": "application/json",
        "X-MCP-Version": "3.1"
    }
    try:
        resp = requests.get(f"{config.api_url.rstrip('/')}/tags/", headers=headers, timeout=5)
        existing_tags = {t['name']: t['id'] for t in resp.json().get('results', [])}
        created = []

        for name, color in config.tag_mapping.items():
            if name not in existing_tags:
                tag_obj = PaperlessTagCreate(name=name, color=color)
                requests.post(
                    f"{config.api_url.rstrip('/')}/tags/",
                    json=tag_obj.model_dump(),
                    headers=headers,
                    timeout=5
                )
                created.append(name)
        return {"status": "success", "created_tags": created, "total_synced": len(config.tag_mapping)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class TaxonomyValidationRule(BaseModel):
    required_namespaces: List[str] = Field(default_factory=lambda: ["Finance", "Medical", "Housing", "Vehicle", "Legal", "Personal"])
    disallowed_unqualified_tags: List[str] = Field(default_factory=lambda: ["tax", "invoice", "receipt", "doc"])

@mcp.tool()
def validate_taxonomy_hierarchy(tags_list: List[str]) -> dict:
    """
    FastMCP 3.1 tool for auditing document tag collections against taxonomy rules.
    """
    rule = TaxonomyValidationRule()
    invalid_unqualified = [t for t in tags_list if t.lower() in rule.disallowed_unqualified_tags]
    valid_namespaced = [t for t in tags_list if "/" in t and t.split("/")[0] in rule.required_namespaces]

    return {
        "is_valid": len(invalid_unqualified) == 0,
        "unqualified_violations": invalid_unqualified,
        "namespaced_tag_count": len(valid_namespaced)
    }

if __name__ == "__main__":
    sample_config = {
        "api_url": "http://localhost:8000/api",
        "token": "mock_token_key",
        "tag_mapping": {
            "inbox": "#e67e22",
            "needs-action": "#e74c3c",
            "Finance/Bill": "#3498db"
        }
    }
    print("FastMCP Paperless Taxonomy Server initialized successfully.")
```

## Production Deployment & Systemd Worker Architecture

To execute taxonomy maintenance scripts and FastMCP 3.1 background sync daemons on Linux hosts managing Paperless-ngx instances, use the systemd unit template below:

```ini
[Unit]
Description=Paperless Taxonomy FastMCP 3.1 Daemon
After=network.target paperless-webserver.service

[Service]
Type=simple
User=paperless
Group=paperless
WorkingDirectory=/opt/paperless-taxonomy
ExecStart=/usr/bin/python3 -m mcp.server.fastmcp run paperless_taxonomy_server.py
Restart=always
RestartSec=10s
Environment=PYTHONUNBUFFERED=1
Environment=PAPERLESS_API_URL=http://localhost:8000/api
Environment=PAPERLESS_API_TOKEN=mock_token_key

# Security Isolation
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md): The implementation platform for this taxonomy.
- [Scan-to-Task Playbook](../../playbooks/scan-to-task.md): A workflow that uses these tags to trigger tasks.
- [Warranty Extraction](../../reference-implementations/llm-prompts/warranty-extraction.md): Uses the `Admin/Warranty` tag as a trigger.
- [Manual Metadata Schema](../../reference-implementations/metadata-schemas/manuals.md): Uses the `Admin/Manual` tag.
- [Webhook Ingestion](../../reference-implementations/paperless/webhook-ingestion.md): How documents and tags enter the system.
- [n8n](../../services/n8n.md): The engine that processes tags and triggers actions.
- [Home Admin Agent Architecture](../../knowledge_base/home-admin-agent-architecture.md): The "brain" that interacts with the tagged archive.
- [Vikunja](../../services/vikunja.md): The task manager used for `needs-action` routing.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md): The interface for agents to interact with Paperless.

## Sources / References
- [Paperless-ngx Tags Documentation](https://docs.paperless-ngx.com/usage/#tags)
- [Tagging Strategies for Personal Documents](https://github.com/joanmarcriera/Home-office-automations)
- [Paperless-ngx API Documentation](https://docs.paperless-ngx.com/api/)

---
## Contribution Metadata
- Last reviewed: 2026-10-12
- Confidence: high
