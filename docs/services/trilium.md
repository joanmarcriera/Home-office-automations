# Trilium Notes (TriliumNext)

Trilium Notes is a hierarchical note-taking application with a focus on building large personal knowledge bases. Following the transition of the original project to maintenance mode, the community-driven [TriliumNext](https://github.com/TriliumNext/TriliumNext) fork has become the primary active branch, introducing significant modern features for the late October / November 2026 agentic era.

## What it is
Trilium Notes is a hierarchical note-taking application focused on building large personal knowledge bases. It features deep nesting, powerful scripting (JavaScript), and advanced visualization of note relationships. The **TriliumNext** fork continues this legacy with improved performance, security, and modern note types like native spreadsheets. In late October / November 2026, it is a primary destination for structured memory for frontier agents like Claude 5.1 and GPT-5.5.

## What problem it solves
Managing thousands of notes with complex inter-relationships is difficult in standard "flat" or "shallow" note apps. Trilium solves this by treating notes as a forest of trees, allowing a single note to exist in multiple places (cloning), and providing an automation engine to manage metadata and note lifecycle. It prevents "knowledge rot" by allowing deep structural organization that mirrors complex mental models.

## Where it fits in the stack
**Category**: Services / Knowledge Management. It serves as the **core intellectual repository** for structured long-term knowledge, research, and documentation. It integrates with the broader homelab via its REST API, acting as a destination for automated data ingestion from n8n or agentic workflows.

## Typical use cases
- **Personal Knowledge Base (PKB)**: Building a "second brain" with deep hierarchical structure.
- **Agentic Journaling**: Using scripts to automatically summarize daily logs via Claude 5.1, GPT-5.5, or Gemini 4.0.
- **Technical Snippet Management**: Storing and executing code snippets within the knowledge tree.
- **Structured Data Analysis**: Managing household or research data using the built-in **Spreadsheet** note type.
- **Document Archival**: Digitizing paper notes and PDFs via built-in **OCR** and indexing.

## Strengths
- **Extreme Flexibility**: Hierarchical structure with support for cloning notes into multiple locations.
- **Programmability**: Built-in JavaScript scripting engine for automating note behavior and metadata.
- **Native Spreadsheets**: Integrated Excel-like editing via Univer Sheets, allowing calculations within the KB.
- **Advanced OCR**: Built-in engine automatically extracts and indexes text from images, PDFs, and Office documents.
- **Self-Hostable**: Strong synchronization capabilities for private, local-first knowledge management.

## Limitations
- **Learning Curve**: The high feature density and scripting capabilities require time to master.
- **UI Complexity**: The interface can feel cluttered compared to modern minimal "block-based" editors.
- **Legacy Scripting**: Older scripts using `api.axios` must be migrated to the native `fetch()` API in versions 0.103+.

## When to use it
- When you need a "forest" rather than a "flat list" for your notes.
- When you want to programmatically automate your knowledge base (e.g., auto-tagging, dynamic dashboards).
- When you require integrated spreadsheet capabilities and deep document search in a single tool.
- When you prefer a local-first, self-hosted solution over proprietary SaaS.

## When not to use it
- For quick, ephemeral scratchpad notes (use a simple tool like [Logseq](../tools/ai_knowledge/logseq.md)).
- If you prefer a highly polished, mobile-first SaaS experience with minimal configuration.

## Getting started

The easiest way to self-host TriliumNext is via Docker.

### Installation (Docker)
```bash
docker run -d -p 8080:8080 -v ~/trilium-data:/home/node/trilium-data triliumnext/notes:latest
```

### Initial Setup
1. Access the UI at `http://localhost:8080`.
2. Follow the setup wizard to create your account and data directory.
3. Enable **OCR** in the Media options to begin indexing your document attachments.

## CLI examples
While Trilium lacks a standalone CLI binary, it is fully manageable via the REST API and Docker commands.

```bash
# Health Check
curl http://localhost:8080/api/health

# Search via API (requires setup of authentication token)
curl -H "Authorization: <your_token>" "http://localhost:8080/api/notes?search=markdown"

# Note Export
curl -H "Authorization: <your_token>" "http://localhost:8080/api/notes/<note_id>/export?format=html" -o note.html
```

## API examples

### Create a Note (Python with Pydantic v2 Validation)
Utilize Claude 5.1, GPT-5.5, or Gemini 4.0 to orchestrate note creation via the REST API and MCP 3.1 / FastMCP 3.1. This snippet provides robust request validation utilizing Pydantic v2 before interacting with the Trilium REST API.

```python
import requests
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List

class TriliumNoteCreate(BaseModel):
    parentNoteId: str = Field(default="root", description="ID of the parent note")
    title: str = Field(..., min_length=1, max_length=255, description="Title of the note")
    type: str = Field(default="text", description="Type of the note (e.g., text, code, spreadsheet)")
    content: str = Field(..., description="Markdown or HTML content of the note")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed_types = {"text", "code", "relation", "book", "file", "image", "spreadsheet"}
        if v not in allowed_types:
            raise ValueError(f"type must be one of {allowed_types}")
        return v

class TriliumNoteResponse(BaseModel):
    noteId: str
    parentNoteId: str
    title: str
    type: str
    content: Optional[str] = None
    attributes: Optional[List[Dict[str, Any]]] = None

def create_trilium_note(url: str, token: str, payload: TriliumNoteCreate) -> TriliumNoteResponse:
    headers = {"Authorization": token}

    # Validation step is done automatically by Pydantic model instantiation
    response = requests.post(f"{url}/notes", json=payload.model_dump(), headers=headers)
    response.raise_for_status()

    raw_response = response.json()
    return TriliumNoteResponse(**raw_response)

# Example usage:
# note_payload = TriliumNoteCreate(parentNoteId="root", title="Agentic Insights", type="text", content="Validated via Pydantic v2.")
# response_note = create_trilium_note("http://localhost:8080/api", "my-api-token", note_payload)
# print(response_note.noteId)
```

### Modern Scripting (JavaScript)
TriliumNext v0.103+ utilizes native `fetch`.

```javascript
// Fetch-based pattern for internal scripts
const response = await fetch('https://api.example.com/data');
const data = await response.json();
api.log(`Data retrieved: ${data.message}`);
```

## Related tools / concepts
- [Obsidian](../tools/ai_knowledge/obsidian.md) — The primary markdown-based alternative.
- [Logseq](../tools/ai_knowledge/logseq.md) — For privacy-first outliner-based knowledge.
- [Joplin](../tools/ai_knowledge/joplin.md) — For a simpler, cross-platform notebook experience.
- [AnyType](../tools/intake_storage/anytype.md) — A decentralized, object-based alternative.
- [SilverBullet](../tools/intake_storage/silverbullet.md) — A hackable, markdown-based knowledge base.
- [n8n](n8n.md) — For automating data ingestion into Trilium.
- [Paperless-ngx](paperless-ngx.md) — For dedicated document management and advanced OCR workflows.
- [Excalidraw](excalidraw.md) — For embedding hand-drawn diagrams into notes.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — For local inference and knowledge synthesis.
- [Claude 5.1](../tools/ai_knowledge/claude.md) — For high-performance agentic reasoning over the PKB.
- [GPT-5.5](../tools/providers/huggingface.md) — For multi-agent cognitive loops.

## Sources / references
- [TriliumNext GitHub Repository](https://github.com/TriliumNext/TriliumNext)
- [Trilium Wiki](https://github.com/zadam/trilium/wiki)
- [TriliumNext Releases and Changelog](https://github.com/TriliumNext/TriliumNext/releases)

## Contribution Metadata
- Last reviewed: 2026-11-12
- Confidence: high
