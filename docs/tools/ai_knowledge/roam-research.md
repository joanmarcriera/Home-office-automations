# Roam Research

## What it is
Roam Research is a "note-taking tool for networked thought." It popularized the concept of bi-directional linking and a non-hierarchical, "graph-based" approach to personal knowledge management (PKM). By early January 2027, it serves as a robust engine for personal knowledge graphs that integrate with frontier AI models via the **Model Context Protocol (MCP) 3.1 / FastMCP 3.1 specifications**, enabling agentic reasoning across complex webs of information.

## What problem it solves
Traditional folder-based note-taking systems often force users to categorize information prematurely. Roam allows for organic growth of knowledge by connecting ideas via `[[links]]` and `#tags`, creating a web of interrelated concepts where "the graph is the file system." This enables discovery of non-obvious connections between disparate research points.

## Where it fits in the stack
[AI & Knowledge](./index.md). It serves as a primary source of unstructured personal data that can be used for building personal knowledge graphs or providing high-signal context for [RAG systems](../../knowledge_base/patterns/rag-pattern.md).

## Typical use cases
- **Research Synthesis**: Connecting disparate notes from books, articles, and lectures.
- **Daily Logging**: Using the "Daily Notes" page as a scratchpad that automatically links to project pages.
- **Zettelkasten**: Implementing a permanent note system for long-term thinking.
- **Recursive Task Management**: Managing nested tasks that reference specific research blocks.
- **Agentic Knowledge Retrieval**: Using an agent to traverse the graph and synthesize answers from multiple blocks.

## Strengths
- **Bi-directional Linking**: Automatically shows "unlinked references," surfacing hidden connections.
- **Block-level Granularity**: Every paragraph (block) is a first-class citizen with a unique ID, allowing for block embedding and referencing.
- **Fluid Interface**: Encourages frictionless entry of information without worrying about "where it goes."
- **Programmability**: Powerful "Roam/js" and "Roam/css" extensions allow users to build custom functionality.
- **AI Integration**: Native support for SOTA models like **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0** for graph-wide reasoning.

## Limitations
- **Proprietary/Closed Source**: Data is stored on Roam's servers (though encrypted graphs are supported).
- **Learning Curve**: The "daily notes" first workflow and complex syntax take time to master.
- **Performance**: Large graphs can experience lag; search can slow down with 50k+ blocks.
- **Syncing**: Mobile-to-desktop syncing can occasionally experience conflicts in high-velocity multi-device setups.

## When to use it
- When you prioritize discovering connections between ideas over strict organization.
- When your work involves heavy cross-referencing and research synthesis.
- When you want a platform that can be extended with custom JavaScript.
- When you need a knowledge base that "thinks" like a graph.

## When not to use it
- When you require a local-first, fully open-source solution (use [Logseq](./logseq.md) or [Obsidian](./obsidian.md) instead).
- When you need a simple, folder-based filing system.
- When high-performance mobile access is a dealbreaker (Roam's mobile app is primarily a wrapper).

## Getting started
Users can quickly get started with Roam using its core syntax:
- `[[Page Name]]`: Creates or links to a page.
- `#Tag`: Creates or links to a page (shorthand for `[[Tag]]`).
- `((Block ID))`: References a specific block.
- `{{[[TODO]]}}`: Creates a checkbox.
- `{{[[query]]: {and: [[Task]] {not: [[DONE]]}}}}`: Creates a dynamic query.
- **MCP Setup**: Install the Roam MCP server supporting **FastMCP 3.1** to allow tools like [Claude Code](../development_ops/claude-code.md) to query your graph.

## CLI examples
Using community-developed CLI tools like `roam-to-git`, you can automate the backup of your graph to a local Git repository in Markdown format.

```bash
# Example backup script
roam-to-git ./my-roam-backup --graph MyGraph --token $ROAM_TOKEN

# Listing backup contents
ls -R ./my-roam-backup/markdown/
```

## API examples
The Roam Alpha API allows for programmatic interaction with graphs, essential for syncing homelab data or automated agents.

### Programmatic Sync with Pydantic v2 Validation
This example demonstrates how to validate block schemas using Pydantic v2 and write a clean, validated block to Roam Research.

```python
import os
import requests
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, SecretStr

# Define schema schemas with Pydantic v2
class RoamBlock(BaseModel):
    string: str = Field(..., min_length=1, description="Text content of the block")
    uid: Optional[str] = Field(None, min_length=9, max_length=9, description="Optional 9-character UID")

class RoamLocation(BaseModel):
    parent_uid: str = Field(..., alias="parent_uid", description="UID of the parent page or block")
    order: int = Field(0, ge=0, description="Order index of the block")

    class Config:
        populate_by_name = True

class WriteBlockRequest(BaseModel):
    action: str = Field("create-block", description="API Action")
    location: RoamLocation
    block: RoamBlock

def push_to_roam(graph_name: str, api_token: SecretStr, parent_uid: str, text: str) -> dict:
    url = f"https://api.roamresearch.com/v1/alpha/graph/{graph_name}/write"

    # Validate payload through Pydantic v2
    try:
        payload = WriteBlockRequest(
            location=RoamLocation(parent_uid=parent_uid, order=0),
            block=RoamBlock(string=text)
        )
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
        raise

    headers = {
        "Authorization": f"Bearer {api_token.get_secret_value()}",
        "Content-Type": "application/json"
    }

    # Model serialization to dict/json matching the API's camelCase / snake_case alias structures
    response = requests.post(
        url,
        headers=headers,
        json=payload.model_dump(by_alias=True)
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Example execution with mock token
    token = SecretStr(os.environ.get("ROAM_API_TOKEN", "mock_token_for_validation_purposes"))
    try:
        res = push_to_roam(
            graph_name="my-research-graph",
            api_token=token,
            parent_uid="daily-notes-uid",
            text="[[Home Automation]] Alert: Front door opened at 14:00"
        )
        print("Block written successfully:", res)
    except Exception as e:
        print("Failed to push block:", e)
```

### Graph Analysis (JSON Export)
Roam allows for full graph exports in JSON format, which can be analyzed by local LLMs like **Llama 4**.

```json
[
  {
    "title": "Project Alpha",
    "uid": "proj-alpha-123",
    "children": [
      {
        "string": "Key research finding [[Source-1]]",
        "uid": "abc-123",
        "children": [
            { "string": "Supporting data point", "uid": "def-456" }
        ]
      }
    ]
  }
]
```

## Related tools / concepts
- [Logseq](./logseq.md) — Open-source alternative.
- [Obsidian](./obsidian.md) — Local-first alternative.
- [Networked Thought](../../knowledge_base/README.md) — Core PKM concept.
- [Joplin](./joplin.md) — Privacy-first notes.
- [Notion AI](./notion-ai.md) — Workspace-integrated AI.
- [AnyType](../intake_storage/anytype.md) — Local-first graph workspace.
- [SilverBullet](../intake_storage/silverbullet.md) — Markdown-native PWA.
- [Tika](../../services/tika.md) — For indexing Roam exports.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agent interaction.

## Sources / references
- [Official Website](https://roamresearch.com/)
- [Roam Research API Documentation](https://developer.roamresearch.com/)
- [Roam/js Extensions](https://roamjs.com/)
- **Licensing**: Proprietary SaaS ($15/month).

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
