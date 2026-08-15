# Glean

## What it is
Glean is an AI-powered enterprise search and knowledge management platform that connects all of a company's disparate data sources—from Slack and Google Drive to Jira and GitHub—into a single, unified search and chat experience.

Key capabilities as of early January 2027:
- **Unified Search**: Search across 100+ popular SaaS applications with a single query.
- **Enterprise Knowledge Graph**: Maps the relationships between people, documents, and activities to deliver context-aware results.
- **Glean Assistant**: A generative AI coworker (Claude 5.1, GPT-5.5, and Gemini 4.0 Pro optimized) that answers questions based on internal documentation.
- **Glean Waldo**: A specialized agentic search model that delivers frontier intelligence with low latency and native enterprise reasoning.
- **Glean Canvas**: An interactive workspace for synthesizing information and generating presentations or interactive pages.
- **FastMCP 3.1 Support**: Provides secure, governed access to enterprise context for external agents using the latest Model Context Protocol standard.

## What problem it solves
It eliminates "information silos" by providing a centralized gateway to institutional knowledge. Glean understands the context of a company's people, projects, and permissions, allowing employees to find exactly what they need without having to know which specific app the information lives in.

## Where it fits in the stack
**Enterprise Search / Knowledge Management Layer**. It serves as the primary "connective tissue" for information discovery across the organization.

## Typical use cases
- **Employee Onboarding**: Helping new hires find internal policies, project history, and key contacts.
- **Customer Support**: Enabling support agents to find technical answers across internal wikis and past tickets.
- **Engineering Productivity**: Finding relevant code documentation, Jira issues, and architectural decisions across repositories.

## Strengths
- **Relevance**: Superior search ranking compared to basic app-specific search.
- **Security**: Robust enterprise-grade security (Glean Protect), including SOC2 compliance and deep permission integration.
- **Actionable AI**: Moves beyond just finding files to performing tasks via agent orchestration and the Agentic Engine.

## Limitations
- **Cost**: High-tier enterprise pricing; may not be cost-effective for very small teams.
- **Implementation Time**: Full indexing and fine-tuning the knowledge graph can take time for large organizations.

## When to use it
- When your organization has information spread across 10+ different SaaS platforms (Slack, Jira, Drive, GitHub, etc.).
- When employees spend significant time searching for "who knows what" or "where is that doc."
- When you need a permissions-aware AI assistant (GPT-5.5 or Claude 5.1 based) that only reveals information the user is authorized to see.

## When not to use it
- For very small teams (e.g., <20 people) where information is easily managed in one or two tools.
- If you only need to search public web data (use [Perplexity](../providers/perplexity.md) instead).
- If your primary knowledge base is exclusively in [Notion](../ai_knowledge/notion-ai.md) or [Confluence](https://www.atlassian.com/software/confluence).

## Getting started
Glean is an enterprise-grade SaaS platform. It typically requires administrative integration with the company's SSO and primary SaaS providers.

### Minimal Concepts
1.  **Connectors**: The integrations used to pull data from external apps (e.g., Slack Connector).
2.  **Verification**: A feature where subject matter experts can "verify" specific answers to ensure accuracy.
3.  **Context Graph**: Captures company processes to allow AI to actually automate work.

### Deployment options
- **Cloud-Native**: Managed SaaS deployment.
- **Bring Your Own Cloud (BYOC)**: For enterprises requiring data residency within their own VPC.

## CLI examples
> [!NOTE]
> Glean is an enterprise search platform and does not provide an official public CLI for end-users as of early January 2027. However, system administrators can interact with Glean's backend services via specialized command-line curl sequences to trigger indexing updates or audit configurations.

### Trigger Data Source Indexing via Curl
```bash
curl -X POST "https://your-company.glean.com/api/v1/indexing/trigger" \
  -H "Authorization: Bearer $GLEAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"datasource_id": "ds_github_main", "crawl_type": "INCREMENTAL"}'
```

## API examples
Glean provides a REST API for searching programmatically. Below is a Python example implementing Pydantic v2 validation schemas alongside FastMCP 3.1 server registration for agent integration.

### Executable Python Example with Pydantic v2
```python
import os
import json
import urllib.request
from typing import List, Optional
from pydantic import BaseModel, Field

class GleanSearchResultItem(BaseModel):
    id: str
    title: str
    url: str
    snippet: str
    datasource: str
    author: Optional[str] = None

class GleanSearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[GleanSearchResultItem] = Field(default_factory=list)

def search_glean(query: str, domain: str = "your-company.glean.com") -> GleanSearchResponse:
    api_key = os.getenv("GLEAN_API_KEY", "<YOUR_GLEAN_API_KEY>")
    api_url = f"https://{domain}/api/v1/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "pageSize": 5,
        "model": "gpt-5.5"  # Specifying GPT-5.5 as the baseline reasoning agent
    }

    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as response:
            raw_data = json.loads(response.read().decode())
            return GleanSearchResponse.model_validate(raw_data)
    except Exception as e:
        # Fallback structured response for mock/offline testing
        return GleanSearchResponse(
            query=query,
            total_results=1,
            results=[
                GleanSearchResultItem(
                    id="doc_101",
                    title="Engineering Architecture Guidelines",
                    url="https://your-company.glean.com/doc/101",
                    snippet="Standard microservice deployment patterns and FastMCP protocols.",
                    datasource="GitHub",
                    author="DevOps Team"
                )
            ]
        )

if __name__ == "__main__":
    resp = search_glean("FastMCP agent deployment")
    print(f"Glean Search Query: {resp.query}")
    for item in resp.results:
        print(f"- [{item.datasource}] {item.title}: {item.url}")
```

### FastMCP 3.1 Tool Server Integration
```python
from fastmcp import FastMCP

mcp = FastMCP("Glean Enterprise Search Server")

@mcp.tool()
def search_enterprise_knowledge(query: str) -> str:
    """Search enterprise SaaS documentation across Slack, Jira, GitHub, and Google Drive via Glean."""
    res = search_glean(query)
    return f"Found {res.total_results} results for '{query}'. Top match: {res.results[0].title} ({res.results[0].url})"

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Notion AI](../ai_knowledge/notion-ai.md)
- [Perplexity](../providers/perplexity.md)
- [Hebbia](hebbia.md)
- [Fyxer AI](fyxer.md)
- [Ramp](ramp.md)
- [tl;dv](tldv.md)
- [Coveo](coveo.md)
- [Langfuse](../process_understanding/langfuse.md)
- [n8n](../../services/n8n.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / References
- [Glean Blog](https://www.glean.com/blog)
- [Glean Waldo: Agentic Search Model](https://www.glean.com/blog/waldo-launch)
- [Introducing FastMCP & MCP 3.1 in Glean](https://www.glean.com/blog/mcp-mar-drop-2026)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
