# Roam Research

## What it is
Roam Research is a "note-taking tool for networked thought." It popularized the concept of bi-directional linking and a non-hierarchical, "graph-based" approach to personal knowledge management (PKM).

## What problem it solves
Traditional folder-based note-taking systems often force users to categorize information prematurely. Roam allows for organic growth of knowledge by connecting ideas via `[[links]]` and `#tags`, creating a web of interrelated concepts where "the graph is the file system."

## Where it fits in the stack
[AI & Knowledge](./index.md). It serves as a primary source of unstructured personal data that can be used for building personal knowledge graphs or providing high-signal context for [RAG systems](../../knowledge_base/README.md).

## Typical use cases
- **Research Synthesis**: Connecting disparate notes from books, articles, and lectures.
- **Daily Logging**: Using the "Daily Notes" page as a scratchpad that automatically links to project pages.
- **Zettelkasten**: Implementing a permanent note system for long-term thinking.
- **Recursive Task Management**: Managing nested tasks that reference specific research blocks.

## Strengths
- **Bi-directional Linking**: Automatically shows "unlinked references," surfacing hidden connections.
- **Block-level Granularity**: Every paragraph (block) is a first-class citizen with a unique ID, allowing for block embedding and referencing.
- **Fluid Interface**: Encourages frictionless entry of information without worrying about "where it goes."
- **Programmability**: Powerful "Roam/js" and "Roam/css" extensions allow users to build custom functionality.

## Limitations
- **Proprietary/Closed Source**: Data is stored on Roam's servers (though encrypted graphs are supported).
- **Learning Curve**: The "daily notes" first workflow and complex syntax take time to master.
- **Performance**: Large graphs can experience lag in the web interface; search can slow down with 10k+ pages.

## When to use it
- When you prioritize discovering connections between ideas over strict organization.
- When your work involves heavy cross-referencing and research synthesis.
- When you want a platform that can be extended with custom JavaScript.

## When not to use it
- When you require a local-first, open-source solution (use [Logseq](./logseq.md) or [Obsidian](./obsidian.md) instead).
- When you need a simple, folder-based filing system.
- When high-performance mobile access is a dealbreaker (Roam's mobile app is a wrapper).

## Getting started

### Basic Syntax
- `[[Page Name]]`: Creates or links to a page.
- `#Tag`: Creates or links to a page (shorthand for `[[Tag]]`).
- `((Block ID))`: References a specific block.
- `{{[[TODO]]}}`: Creates a checkbox.

## API: Roam Alpha API
The Roam Alpha API allows for programmatic interaction with graphs. This is essential for syncing your homelab data into your knowledge graph.

```python
import requests
import json

# Replace with your graph name and token
GRAPH_NAME = "my-research-graph"
API_TOKEN = "your_roam_api_token"

def create_block(location_id, text):
    url = f"https://api.roamresearch.com/v1/alpha/graph/{GRAPH_NAME}/write"
    payload = {
        "action": "create-block",
        "location": {"parent-uid": location_id, "order": 0},
        "block": {"string": text}
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Example: Push a home automation alert to Roam
create_block("daily-notes-uid", "[[Home Automation]] Alert: Front door opened at 14:00")
```

## Advanced: JSON Graph Export/Import
Roam allows for full graph exports in JSON format, which can be used to feed local LLMs or perform graph analysis.

```json
[
  {
    "title": "Project Alpha",
    "children": [
      {
        "string": "Key research finding [[Source-1]]",
        "uid": "abc-123",
        "create-time": 1716460000000,
        "children": [
            { "string": "Supporting data point", "uid": "def-456" }
        ]
      }
    ]
  }
]
```

## Integration: Roam to Markdown
Using CLI tools like `roam-to-git`, you can automate the backup of your graph to a local Git repository in Markdown format, enabling integration with this repo's documentation standards.

```bash
# Example backup script
roam-to-git ./my-roam-backup --graph MyGraph --token $ROAM_TOKEN
```

## Licensing and cost
- **Proprietary**: Yes.
- **Cost**: Paid ($15/month or $165/year). No free tier beyond a short trial.
- **Self-hostable**: No.

## Related tools / concepts
- [Logseq](./logseq.md) (Open-source alternative)
- [Obsidian](./obsidian.md) (Local-first alternative)
- [Networked Thought](../../knowledge_base/README.md)
- [Joplin](./joplin.md)
- [Notion AI](./notion-ai.md)
- [AnyType](../intake_storage/anytype.md)
- [SilverBullet](../intake_storage/silverbullet.md)
- [Tika](../../services/tika.md) (for indexing Roam exports)

## Sources / references
- [Official Website](https://roamresearch.com/)
- [Roam Research API Documentation](https://developer.roamresearch.com/)
- [Roam/js Extensions](https://roamjs.com/)

## Contribution Metadata
- Last reviewed: 2026-05-23
- Confidence: high
