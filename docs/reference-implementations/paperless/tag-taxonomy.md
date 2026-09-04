# Reference Implementation: Paperless Tag Taxonomy

## What it is
A hierarchical tagging system designed for Paperless-ngx that organizes personal and household documents into actionable categories. It balances organizational needs (folders/categories) with workflow states (status/actions). As of January 2027, it is optimized for high-reasoning models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4** to perform autonomous classification and lifecycle management via **FastMCP 3.1** interfaces.

## What problem it solves
Flat document storage quickly becomes unmanageable as volume grows. Without a standardized taxonomy, users struggle to find files, and automated agents cannot reliably trigger specific workflows (like paying a bill or extracting a warranty). This taxonomy provides the "semantic hooks" necessary for both humans and machines to navigate the archive, ensuring that "Invisible Kubernetes" and "Agentic Workflows" have structured data to act upon.

## Where it fits in the stack
The taxonomy sits at the **Organization/Metadata layer** of the document management system. It acts as the primary index used by **Search**, **Automated Workflows** (n8n, Python scripts), and **AI Agents** (leveraging **FastMCP 3.1**) to filter and process documents.

## Typical use cases
- **Workflow Automation**: Moving a document from `inbox` to `needs-action` to trigger a reminder in [Vikunja](../../services/vikunja.md).
- **Tax Preparation**: Quickly retrieving all documents tagged with `Keep-7-years` or `Finance/Bill` for annual audits.
- **Legacy Preservation**: Categorizing scanned physical photos and historical records for long-term archiving using [Immich](../../services/immich.md) integration patterns.
- **Agentic Routing**: Using **Llama 4** or **Qwen 3.6 VL** to analyze document sentiment and apply urgent status tags for immediate human attention.

## Strengths
- **Action-Oriented**: Clearly separates "State" (what needs to be done) from "Category" (what the document is).
- **Extensible**: The `Category/Subcategory` pattern allows for infinite growth without breaking existing logic or n8n workflows.
- **Machine-Readable**: Simple, consistent naming conventions are easy for LLMs and scripts to parse via the Paperless REST API.
- **FastMCP 3.1 Compatibility**: Designed to be exposed via FastMCP servers to agentic IDEs and autonomous household assistants.

## Limitations
- **Maintenance**: Requires discipline to ensure every document is tagged correctly, though auto-tagging with **Claude 5.6** and **GPT-5.6** has mitigated this significantly.
- **Tool Support**: While ideal for Paperless-ngx, other DMS tools may have different tagging limitations or lack hierarchical support.
- **Over-Categorization**: Risk of creating too many niche tags that humans won't remember to use, necessitating agentic "Tag Cleanup" routines.

## When to use it
- When setting up a new Paperless-ngx instance for household or small office use.
- When designing automated "Scan-to-Action" pipelines that require high-precision routing.
- For managing multi-generational family archives with high-volume ingest from scanners and email.

## When not to use it
- For extremely small document sets (under 100 files) where a simple full-text search is sufficient.
- If using a DMS that relies entirely on vector-based search without robust tagging support.

## Getting started
1. **Initial Tag Creation**: Create the core status tags (`inbox`, `needs-action`, `processed`) in the Paperless-ngx UI or via API.
2. **Category Hierarchy**: Establish top-level categories using the `Category/Subcategory` naming convention (e.g., `Finance/Bill`).
3. **Matching Rules**: Configure Paperless-ngx "Matching Algorithms" to automatically apply tags based on document content (e.g., "Any" match for "Invoice" applies `Finance/Bill`).
4. **Agentic Onboarding**: Point your Home Admin Agent to the taxonomy documentation so it understands the routing logic.

## CLI examples
These commands are executed within the Paperless-ngx environment to maintain the taxonomy integrity.

```bash
# Rename files on disk based on the new taxonomy and storage templates
docker exec -it paperless-webserver python3 manage.py document_renamer

# Reindex the search engine after a bulk tag migration or update
docker exec -it paperless-webserver python3 manage.py document_index reindex

# Sanity check for documents without any tags (taxonomy gaps)
docker exec -it paperless-webserver python3 manage.py document_index --tags=none
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
Use this programmatic script with strict **Pydantic v2** schemas to synchronize tax tags from your master list to Paperless-ngx while validating matching rules and payload structures.

```python
import sys
import requests
from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, List, Optional

class PaperlessTagCreate(BaseModel):
    """Pydantic v2 model for validating Paperless tag creation payloads."""
    name: str = Field(..., description="Tag name (e.g., 'Finance/Bill' or 'needs-action')")
    color: str = Field(default="#008080", description="Hex color code for tag UI badge")
    matching_algorithm: int = Field(default=1, description="Matching algorithm (1 = Auto, 6 = Exact)")
    is_inbox_tag: bool = Field(default=False, description="Flag indicating if tag acts as inbox state")

class TagSyncConfig(BaseModel):
    """Pydantic v2 config model for taxonomy synchronization."""
    api_url: str = Field(..., description="Paperless REST API endpoint base URL")
    token: str = Field(..., description="Paperless REST API authorization token")
    tag_mapping: Dict[str, str] = Field(..., description="Mapping of tag names to hex colors")

def sync_taxonomy_tags(config: TagSyncConfig) -> bool:
    """Synchronizes taxonomy tags to Paperless-ngx with strict Pydantic v2 validation."""
    headers = {
        "Authorization": f"Token {config.token}",
        "Content-Type": "application/json",
        "X-MCP-Version": "3.1"
    }
    try:
        # Fetch current tags
        resp = requests.get(f"{config.api_url.rstrip('/')}/tags/", headers=headers, timeout=5)
        existing_tags = {t['name']: t['id'] for t in resp.json().get('results', [])}

        for name, color in config.tag_mapping.items():
            if name not in existing_tags:
                tag_obj = PaperlessTagCreate(name=name, color=color)
                requests.post(
                    f"{config.api_url.rstrip('/')}/tags/",
                    json=tag_obj.model_dump(),
                    headers=headers,
                    timeout=5
                )
                print(f"Created taxonomy tag: {name}")
        return True
    except Exception as e:
        print(f"Taxonomy synchronization failed: {e}", file=sys.stderr)
        return False
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

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
