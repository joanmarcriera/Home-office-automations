# Coveo

## What it is
An enterprise-grade AI search and recommendation platform that provides intelligent search, personalized recommendations, and generative AI capabilities.

## What problem it solves
Powers search and discovery experiences for large-scale websites, e-commerce platforms, and internal employee portals, using AI to improve relevance and conversion.

## Where it fits in the stack
**Category**: Enterprise AI / Search & Recommendations

## Typical use cases
- **E-commerce Search**: Providing relevant product search results and personalized recommendations to customers.
- **Customer Service Portals**: Helping customers find answers in support documentation more effectively.
- **Workplace Search**: Connecting employees to the information they need across a vast corporate knowledge base.

## Getting started
Coveo is typically integrated at the enterprise infrastructure level. Developers interact with it via the Search API for building custom search interfaces and the Push API for indexing content from custom sources.

## Technical Examples

### Performing a Search Request (cURL)
Query a Coveo search index programmatically.

```bash
curl -X POST "https://platform.cloud.coveo.com/rest/search/v2" \
  -H "Authorization: Bearer $COVEO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "AI transformation",
    "numberOfResults": 10
  }'
```

### Pushing Content to an Index (Python)
Using the Coveo Push API to index a custom document.

```python
import requests
import os

COVEO_ORG_ID = os.getenv("COVEO_ORG_ID")
COVEO_SOURCE_ID = os.getenv("COVEO_SOURCE_ID")
COVEO_API_KEY = os.getenv("COVEO_API_KEY")

def push_to_coveo(doc_id, title, content):
    url = f"https://api.cloud.coveo.com/push/v1/organizations/{COVEO_ORG_ID}/sources/{COVEO_SOURCE_ID}/documents"
    params = {"documentId": doc_id}
    headers = {
        "Authorization": f"Bearer {COVEO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": title,
        "data": content,
        "FileExtension": ".txt"
    }

    response = requests.put(url, params=params, headers=headers, json=payload)
    response.raise_for_status()
    return response.status_code

# Example usage
push_to_coveo("doc_001", "AI Best Practices", "Content for the AI document...")
```

## Strengths
- **Scalability**: Built for the most demanding enterprise workloads and data volumes.
- **AI Relevance**: Uses advanced machine learning to constantly improve search result quality.
- **Rich Analytics**: Provides deep insights into user search behavior and content performance.

## Limitations
- **Enterprise Complexity**: High-end solution with significant setup and integration effort.
- **Cost**: Premium enterprise pricing.

## When to use it
- For large enterprises needing a robust, highly customizable AI search platform.
- When search relevance directly impacts revenue or support efficiency at scale.

## When not to use it
- For small websites or simple internal search needs.
- If you are looking for a quick, "out of the box" personal search tool.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Enterprise SaaS)
- **Self-hostable**: No

## Related tools / concepts
- [Elastic](elastic.md) — foundational search technology.
- [Glean](glean.md) — employee search and workspace discovery.
- [Algolia](../ai_knowledge/index.md) — API-first search for developers.
- [Pinecone](../tools/infrastructure/index.md) — vector database for AI search.
- [Milvus](../tools/infrastructure/index.md) — open-source vector database.
- [Search Patterns](../knowledge_base/index.md) — general AI search architecture.
- [OpenTelemetry](../tools/development_ops/index.md) — observability for search performance.

## Sources / references
- [Coveo Official Site](https://www.coveo.com/)

## Contribution Metadata
- Last reviewed: 2026-05-23
- Confidence: high
