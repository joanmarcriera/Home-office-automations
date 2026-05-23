# Dashworks

## What it is
An AI-powered search and knowledge management platform designed for teams to find information across all their internal apps.

## What problem it solves
Eliminates information silos by providing a unified interface to search through Slack, Google Drive, Jira, Confluence, and other enterprise tools.

## Where it fits in the stack
**Category**: Enterprise AI / Knowledge Management

## Typical use cases
- **Internal Knowledge Retrieval**: Finding specific documents, messages, or tickets across multiple platforms.
- **Onboarding**: Helping new employees find relevant information and answers to common questions.
- **Executive Summarization**: Getting a quick overview of project statuses or meeting notes from various sources.

## Getting started
Dashworks is a SaaS platform. Integration typically involves connecting your enterprise apps via their web dashboard. For developers, the Dashworks API allows for programmatically querying the knowledge base and managing users.

## Technical Examples

### Querying the Knowledge Base (cURL)
You can use the Dashworks Search API to retrieve answers across all connected sources.

```bash
curl -X POST https://api.dashworks.ai/v1/search \
  -H "Authorization: Bearer $DASHWORKS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is our policy on remote work?",
    "stream": false,
    "filters": {
      "sources": ["slack", "confluence"]
    }
  }'
```

### Python SDK Example
Using the `requests` library to interface with Dashworks:

```python
import requests
import os

DASHWORKS_API_KEY = os.getenv("DASHWORKS_API_KEY")

def ask_dashworks(question: str):
    url = "https://api.dashworks.ai/v1/search"
    headers = {
        "Authorization": f"Bearer {DASHWORKS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": question,
        "max_results": 5
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Example usage
answer = ask_dashworks("Who is the project lead for Alpha?")
print(answer['summary'])
```

## Strengths
- **Wide Integration Support**: Connects to 100+ popular enterprise applications.
- **Personalized Results**: Learns from user behavior and permissions to provide relevant answers.
- **Privacy-First**: Built with enterprise security and data privacy in mind.

## Limitations
- **Subscription Cost**: Enterprise pricing model.
- **Setup Complexity**: Requires administrative access to multiple third-party systems for full effect.

## When to use it
- When your team spends too much time searching for information across different apps.
- When you need a "single source of truth" for internal knowledge.

## When not to use it
- For small teams with very few documents or apps.
- If you prefer a completely local, self-hosted search solution.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (SaaS)
- **Self-hostable**: No

## Related tools / concepts
- [Glean](glean.md) — primary competitor in enterprise search.
- [Guru](guru.md) — knowledge management with verification focus.
- [Coveo](coveo.md) — enterprise-grade search and recommendations.
- [Notion AI](../ai_knowledge/notion-ai.md) — AI search within Notion workspaces.
- [Elastic](elastic.md) — underlying search technology for many enterprise tools.
- [Langfuse](../tools/process_understanding/langfuse.md) — observability for AI queries.
- [Knowledge Management](../knowledge_base/index.md) — core concept and patterns.

## Sources / references
- [Dashworks Official Site](https://www.dashworks.ai/)

## Contribution Metadata
- Last reviewed: 2026-05-23
- Confidence: high
