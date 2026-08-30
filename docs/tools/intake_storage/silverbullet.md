# SilverBullet

## What it is
SilverBullet is an open-source, extensible, Markdown-based personal knowledge management system that runs in the browser. It features a unique "Space Script" capability that allows the entire environment to be programmed and queried using JavaScript and a custom query language. As of early 2027, it supports the **MCP 3.1 / FastMCP 3.1 Task Protocol**, allowing it to serve as a highly programmable, local-first backend for agentic workflows.

## What problem it solves
It combines the simplicity of Markdown with the power of a programmable database. It solves the limitation of static Markdown notes by allowing for live queries, automated indexing, and custom templates that can transform a folder of text files into a functional application (e.g., a task manager, a project tracker, or a library catalog).

## Where it fits in the stack
**Category**: Tool / Knowledge Management. It is a "hacker-friendly" alternative to Obsidian or Logseq, specifically designed for users who want to extend their knowledge base using code and queries directly within their notes. In early 2027, it often serves as a local-first source for advanced reasoning models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL** via its integrated FastMCP 3.1 server.

## Typical use cases
- **Programmable Wiki**: Building an internal knowledge base with automated indexes.
- **Task Management**: Creating custom task dashboards using live queries.
- **Agentic Knowledge Retrieval**: Exposing notes to AI agents via FastMCP 3.1 for autonomous research.
- **Data Scraping**: Using Space Scripts to pull information from external APIs into notes.
- **Personal CRM**: Managing contacts and interactions with structured metadata and automated summaries.

## Strengths
- **Extensibility**: Entirely programmable via Space Scripts (JavaScript).
- **Live Queries**: Built-in SQL-like query language for Markdown blocks.
- **FastMCP 3.1 Support**: Native support for the Model Context Protocol Task Protocol in early 2027.
- **Web-native**: Runs in the browser but can sync to local storage or a remote server.
- **PWA support**: Excellent mobile experience via Progressive Web App technology.

## Limitations
- **Technical Barrier**: Requires some knowledge of JavaScript or SilverBullet's query language to unlock its full potential.
- **Smaller Ecosystem**: Fewer community plugins compared to [Obsidian](../ai_knowledge/obsidian.md).
- **Self-Hosting**: While it can run locally, a server component is required for the best multi-device experience.

## When to use it
- When you want a knowledge base that you can program and extend yourself.
- If you prefer a browser-based workflow but want the power of a local-first application.
- When you need to perform complex data queries across your entire note collection.

## When not to use it
- If you want a polished, consumer-grade app with a massive library of one-click plugins.
- If you are uncomfortable with writing occasional scripts or queries to manage your data.

## Getting started

### 1. Installation
The easiest way to run SilverBullet is via Docker:
```bash
docker run -d \
  --name silverbullet \
  -p 3030:3030 \
  -v ./space:/space \
  zefhemel/silverbullet:latest
```
Alternatively, install via `npm`: `npm install -g @silverbulletmd/silverbullet`.

### 2. Space Initialization
Once running, navigate to `http://localhost:3030`. SilverBullet will automatically generate an **Index Page** with sections for quick notes and tasks.

### Hello World Example
Create a new page (e.g., `Hello`) and add your first "Space Script" to verify the environment:
1. Create a page with `Hello` title.
2. Add the following block:
```javascript
#script
silverbullet.registerFunction("hello", (name) => {
  return `Hello, ${name}!`;
});
```
3. You can now use `{{hello("World")}}` in any page.

## CLI examples
```bash
# Start SilverBullet in a specific directory
silverbullet ./my_notes_space

# Specify a custom port for the server
silverbullet --port 8080 ./my_space

# Run in "read-only" mode for public sharing
silverbullet --readonly ./my_space

# Start the integrated FastMCP server (v0.9.0+ / early 2027)
silverbullet mcp ./my_space
```

## API examples

### Integrated Query (SQL-like)
Embed live queries directly in your Markdown files to aggregate data:
```markdown
<!-- #query task where done = false limit 5 -->
| Name | Page |
| ---- | ---- |
| {{name}} | [[{{page}}]] |
<!-- /query -->
```

### Space Script (JavaScript)
Register custom commands that can be invoked from the command palette:
```javascript
#script
silverbullet.registerCommand({
  name: "Current Date",
  callback: () => {
    const date = new Date().toLocaleDateString();
    editor.insertAtCursor(`Today is ${date}`);
  }
});
```

### Direct API (HTTP)
SilverBullet exposes a REST API for space manipulation (requires authentication if configured):
```bash
# Fetch the content of a specific page
curl http://localhost:3030/api/pages/Index/content
```

### Python: FastMCP 3.1 Task Protocol Space Script and Query Validation (Pydantic v2)
When writing local Python daemons to synchronize, scrape, or extract structured metadata from a SilverBullet space, validating queries prevents malformed objects from polluting markdown databases.

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class SilverBulletPageSchema(BaseModel):
    name: str = Field(..., min_length=1, description="Normalized page title")
    last_modified: int = Field(..., alias="lastModified", description="Epoch timestamp of last modification")
    perm: str = Field("rw", pattern="^(ro|rw)$", description="Read-only or read-write permissions")
    task_id: Optional[str] = Field(None, alias="taskId", description="FastMCP 3.1 task context ID")
    tags: List[str] = Field(default_factory=list, description="Associated space page tags")

def validate_space_page_payload(json_data: str) -> SilverBulletPageSchema:
    """
    Validates SilverBullet page metadata fetched via HTTP API using strict Pydantic v2 validation.
    """
    try:
        # Load and parse via Pydantic v2
        data = json.loads(json_data)
        return SilverBulletPageSchema.model_validate(data)
    except (ValidationError, json.JSONDecodeError) as e:
        print(f"Data verification failed: {e}")
        raise

if __name__ == "__main__":
    raw_payload = '{"name": "Index", "lastModified": 1797897600, "perm": "rw", "taskId": "task-sb-2027", "tags": ["inbox", "work"]}'
    try:
        validated_page = validate_space_page_payload(raw_payload)
        print(f"Validated Page: {validated_page.name} (Tags: {validated_page.tags})")
    except ValidationError:
        pass
```

## Related tools / concepts
- [Obsidian](../ai_knowledge/obsidian.md) (Popular Markdown alternative)
- [Logseq](../ai_knowledge/logseq.md) (Block-based alternative)
- [AnyType](anytype.md) (Local-first alternative)
- [Trilium Notes](../../services/trilium.md) (Hierarchical programmable wiki)
- [Local LLMs](../ai_knowledge/local_llms.md) (Integrating AI with SilverBullet data)
- [Model Context Protocol](../automation_orchestration/mcp.md) (Connectivity standard)
- [Claude 5.6](../ai_knowledge/claude-mythos.md) (Advanced reasoning for notes)
- [Gemma 4](../ai_knowledge/gemini.md) (Efficient local processing)
- [Component Map](../../architecture/component_map.md) (Architectural positioning)
- [KnowledgeOps Standards](../../standards.md) (Governing programmable knowledge)
- [n8n](../../services/n8n.md) (External automation for SilverBullet)
- **Licensing**: MIT License (Open Source). Free to use and self-host.

## Sources / References
- [Official Website](https://silverbullet.md/)
- [GitHub Repository](https://github.com/silverbulletmd/silverbullet)
- [SilverBullet Documentation](https://silverbullet.md/Getting%20Started)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
