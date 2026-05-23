# Guru

## What it is
A collaborative knowledge management platform that uses AI to organize and deliver information to teams within their existing workflows.

## What problem it solves
Captures and verifies internal knowledge, making it easily accessible via browser extensions, Slack, and other tools, reducing the need for repetitive questions.

## Where it fits in the stack
**Category**: Enterprise AI / Knowledge Management

## Typical use cases
- **Sales Enablement**: Providing sales teams with verified product info and talk tracks.
- **Customer Support**: Giving agents quick access to FAQs and troubleshooting guides.
- **Internal Wiki Replacement**: Modernizing the company handbook with AI-driven search and verification.

## Getting started
Guru uses a browser extension and web app for knowledge management. Developers can use the Guru API to create, search, and verify knowledge "Cards" programmatically.

## Technical Examples

### Searching for Knowledge Cards (cURL)
Use the API to search your Guru workspace for specific information.

```bash
curl -X GET "https://api.getguru.com/api/v1/search/cards?q=vacation+policy" \
  -u "$GURU_USER_EMAIL:$GURU_API_TOKEN" \
  -H "Accept: application/json"
```

### Creating a Knowledge Card via Python
Programmatically ingest information into Guru as a verified Card.

```python
import requests
import json
import os

# Guru uses Basic Auth (Email + API Token)
USER = os.getenv("GURU_USER_EMAIL")
TOKEN = os.getenv("GURU_API_TOKEN")
AUTH = (USER, TOKEN)

def create_guru_card(title, content, collection_id):
    url = "https://api.getguru.com/api/v1/cards"
    payload = {
        "title": title,
        "content": content,
        "collectionId": collection_id,
        "shareStatus": "TEAM"
    }

    response = requests.post(url, auth=AUTH, json=payload)
    response.raise_for_status()
    return response.json()

# Example usage
new_card = create_guru_card(
    "2026 Holiday Schedule",
    "<p>Here are the official holidays for 2026...</p>",
    "YOUR_COLLECTION_ID"
)
print(f"Created Card ID: {new_card['id']}")
```

## Strengths
- **Knowledge Verification**: Ensures information is accurate and up-to-date with a verification workflow.
- **In-Workflow Delivery**: Delivers info directly where teams work (e.g., inside Gmail, Slack, or Zendesk).
- **AI-Powered Search**: Understands natural language queries and suggests relevant knowledge cards.

## Limitations
- **Content Maintenance**: Requires active participation from "subject matter experts" to keep info verified.
- **Cost**: Per-user subscription pricing.

## When to use it
- When you need to ensure that the information your team is using is verified and current.
- When you want to reduce "shoulder-tapping" for information.

## When not to use it
- If your team is too small to justify the overhead of knowledge management.
- For purely personal note-taking.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (SaaS)
- **Self-hostable**: No

## Related tools / concepts
- [Dashworks](dashworks.md) — AI-powered unified search across internal apps.
- [Glean](glean.md) — enterprise search and knowledge platform.
- [Notion AI](../ai_knowledge/notion-ai.md) — AI workspace for notes and documents.
- [Obsidian](../knowledge_base/index.md) — local knowledge management alternative.
- [Logseq](../tools/development_ops/logseq.md) — privacy-first local knowledge base.
- [AnyType](../tools/intake_storage/anytype.md) — decentralized knowledge base.
- [SilverBullet](../tools/intake_storage/silverbullet.md) — extensible open-source wiki.

## Sources / references
- [Guru Official Site](https://www.getguru.com/)

## Contribution Metadata
- Last reviewed: 2026-05-23
- Confidence: high
