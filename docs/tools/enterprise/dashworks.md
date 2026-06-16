# Dashworks

## What it is
Dashworks is an AI-powered search and knowledge management platform that enables teams to find information across all their internal applications through a unified, conversational interface.

## What problem it solves
It solves the "information silos" problem by centralizing access to data stored in fragmented tools like Slack, Google Drive, Jira, Confluence, and GitHub. Dashworks allows users to ask natural language questions and receive grounded answers based on their company's collective knowledge.

## Where it fits in the stack
**Category**: Enterprise AI / Knowledge Management
It acts as the "internal brain" of an organization, providing a Retrieval-Augmented Generation (RAG) layer that connects frontier models (GPT-5.5, Claude 4.8 Opus) to proprietary enterprise data.

## Typical use cases
- **Internal Knowledge Retrieval**: Quickly finding specific policies, project updates, or technical specs across multiple platforms.
- **Automated Employee Onboarding**: Answering new hires' questions about company culture, tools, and processes without human intervention.
- **Executive Summarization**: Generating brief summaries of project progress by analyzing messages and documents from disparate sources.

## Strengths
- **Massive Integration Ecosystem**: Support for over 100+ enterprise connectors out of the box.
- **Permissions-Aware Search**: Respects existing access controls in source systems, ensuring users only see information they are authorized to access.
- **Conversational Answers**: Beyond just links, it provides synthesized answers with citations to original sources.
- **Ease of Deployment**: SaaS-based setup that can get a team up and running in minutes.

## Limitations
- **External Dependency**: As a SaaS platform, it requires trusting a third party with metadata or content indexing.
- **Subscription-Based**: Costs can scale significantly for large enterprises compared to self-hosted search engines.
- **Indexing Latency**: There may be a short delay between an update in a source system and its availability in Dashworks search.

## When to use it
- When your team loses significant productivity searching for info across too many tools.
- If you need a "plug-and-play" RAG solution for your internal company data.
- For organizations that prioritize ease of use and rapid time-to-value for internal search.

## When not to use it
- For highly sensitive industries that mandate 100% on-premise data residency.
- If you have a very small team where information is easily managed in a single tool (e.g., just Notion).
- If you require deep, custom machine learning model training on your specific domain (consider a custom stack with Pinecone and Claude).

## Getting started
Dashworks is primarily accessed via its web application and browser extension. Developers can leverage the Dashworks API to build custom search experiences or integrate Dashworks into their own internal tools and AI agents.

## CLI examples
While Dashworks does not provide a standalone CLI, its API can be queried using standard tools like `curl`.

```bash
# Query Dashworks to find information about a project
curl -X POST https://api.dashworks.ai/v1/search \
  -H "Authorization: Bearer $DASHWORKS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the status of the Blackwell integration?",
    "stream": false
  }'
```

## API examples
The Dashworks API allows for programmatically accessing the organizational knowledge base, which is particularly useful for augmenting AI agent prompts.

```python
import requests
import os

DASHWORKS_API_KEY = os.getenv("DASHWORKS_API_KEY")

def query_internal_brain(question: str):
    """
    Interfaces with Dashworks to retrieve internal company knowledge.
    """
    url = "https://api.dashworks.ai/v1/search"
    headers = {
        "Authorization": f"Bearer {DASHWORKS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": question,
        "max_results": 3,
        "semantic_search": True
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Example: AI agent checking for internal compliance rules
info = query_internal_brain("What are our June 2026 data retention policies?")
print(f"Verified Answer: {info.get('answer')}")
```

## Related tools / concepts
- [Glean](glean.md) — the primary enterprise-scale competitor for unified search.
- [Guru](guru.md) — focused on verified knowledge "cards" and wiki management.
- [Coveo](coveo.md) — enterprise-grade search and recommendation platform.
- [Notion AI](../ai_knowledge/notion-ai.md) — integrated AI search within the Notion ecosystem.
- [Elastic](elastic.md) — open-source search foundation used for building custom indexes.
- [Pinecone](../infrastructure/pinecone.md) — vector database for building custom enterprise RAG.
- [Langfuse](../process_understanding/langfuse.md) — observability for tracking Dashworks-powered AI queries.

## Sources / references
- [Dashworks Official Site](https://www.dashworks.ai/)
- [Dashworks API Documentation](https://docs.dashworks.ai/)
- [Enterprise Search Patterns](../../knowledge_base/patterns/search-patterns.md)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
