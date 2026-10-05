# Dashworks

## What it is
Dashworks is an enterprise-grade AI search and knowledge graph orchestration platform designed to unify, index, and synthesize information across fragmented internal SaaS and on-premise applications. As of early 2027, Dashworks serves as a core "Internal Brain" layer for autonomous AI agents, deploying native **Model Context Protocol (FastMCP 3.1)** task servers to interface frontier models (**Gemma 4**, **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**) directly with permissioned organizational data.

By indexing real-time content, document metadata, and user permission models across tools like Slack, Google Drive, Jira, Confluence, GitHub, Notion, and Salesforce, Dashworks delivers grounded, cited answer synthesis through natural language search interfaces, agentic context injection APIs, and web extensions.

```
+-----------------------------------------------------------------------------------+
|                         ENTERPRISE SAAS & ON-PREM DATA SOURCES                    |
|                                                                                   |
|  Slack | Google Drive | GitHub | Jira | Confluence | Notion | Salesforce | Zendesk  |
+------------------------------------+----------------------------------------------+
                                     |
                                     v
+------------------------------------+----------------------------------------------+
|                   DASHWORKS KNOWLEDGE GRAPH ENGINE                                |
|                                                                                   |
|  +-------------------------+    +-----------------------+    +------------------+ |
|  | Multi-Source Indexer    |    | Permission Mapper     |    | Vector & Hybrid  | |
|  | (Incremental Webhooks)  |    | (Source ACL Mirroring)|    | Retrieval Engine | |
|  +------------+------------+    +-----------+-----------+    +--------+---------+ |
|               |                             |                         |           |
|               +-----------------------------+-------------------------+           |
|                                             |                                     |
|                                             v                                     |
|  +-----------------------------------------------------------------------------+  |
|  |                     FASTMCP 3.1 KNOWLEDGE CONNECTOR                         |  |
|  |           Unified Search Tool  |  Citation Verification Server             |  |
|  +--------------------------------------+--------------------------------------+  |
+-----------------------------------------|-----------------------------------------+
                                          |
                                          v
+-----------------------------------------+-----------------------------------------+
|                  AUTONOMOUS AGENTIC EXECUTION & RAG RUNTIME                       |
|                                                                                   |
|  +-----------------------+      +------------------------+     +----------------+ |
|  | Grounded Context      |      | Pydantic v2 Verified   |     | Citation Link  | |
|  | (Zero-Hallucination)  |      | Search Payload          |     | Attributer     | |
|  +-----------------------+      +------------------------+     +----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Modern enterprise teams face severe operational friction due to information fragmentation across disconnected SaaS tools:

1. **Context Fragmentation and Time Loss**: Employees spend hours searching across separate search bars in Slack, Jira, Google Docs, and GitHub to answer basic operational questions. Dashworks unifies cross-platform search into a single conversational entry point.
2. **Agent Hallucinations on Private Data**: Autonomous agents running frontier models lack access to proprietary company context. Dashworks supplies grounded RAG context with direct source URL citations to prevent hallucinated decisions.
3. **Data Security and ACL Leakage**: Standard search tools often bypass fine-grained document permission levels. Dashworks mirrors source access control lists (ACLs) in real time, ensuring users and agents can only query information they are explicitly authorized to view.
4. **Stale Vector Embeddings**: In-house vector database setups require constant engineering effort to keep document chunks updated. Dashworks manages automated incremental syncing via SaaS webhooks.

## Where it fits in the stack
**Category**: Enterprise AI / Knowledge Management & RAG Layer.

- **Storage & Retrieval Layer**: Connects raw enterprise content to vector and semantic hybrid indices while honoring source ACLs.
- **MCP Integration Layer**: Interfaced via FastMCP 3.1 servers, allowing agent orchestration frameworks like [Ag2](../frameworks/ag2.md), [Smolagents](../frameworks/smolagents.md), [LangGraph](../frameworks/langgraph.md), or [Agno](../agents/agno.md) to perform search queries during multi-step reasoning loops.
- **Identity & Access**: Integrates with enterprise Single Sign-On (SSO) systems ([Okta](okta.md), Azure AD, Google Workspace) for identity pass-through.

## Typical use cases
- **Universal Enterprise Search**: Employees asking "What is our Q1 product roadmap for the Gemma 4 integration?" and receiving a synthesized response backed by Slack threads, Jira tickets, and Google Slides.
- **Autonomous Agentic RAG Injection**: Supplying real-time, grounded facts to software development agents attempting to resolve customer support tickets or fix GitHub issues.
- **Automated Executive Briefings**: Synthesizing cross-channel project updates into weekly executive summaries.
- **Employee Onboarding Assistance**: Allowing new hires to query company policy, technical setup guides, and team norms directly inside Slack or web browser extensions.

## Strengths
- **100+ Turnkey SaaS Connectors**: Pre-built native integrations for major business productivity applications with minimal setup overhead.
- **Strict ACL Mirroring**: Automatically syncs permissions from Google Drive, Slack, and Jira to prevent unauthorized data exposure.
- **Synthesized Answers with Direct Citations**: Provides conversational responses with inline deep links to original source documents.
- **Native FastMCP 3.1 Integration**: Standardized tool interface enabling agent frameworks to execute natural language queries against company data safely.

## Limitations
- **Cloud SaaS Hosting Dependencies**: Requires indexing enterprise metadata and document text on Dashworks cloud infrastructure, which may require compliance review for strict on-premise environments.
- **Indexing Latency**: Minor delays (1–5 minutes) between document creation in source apps and full index availability.
- **User-Based Subscription Pricing**: Per-seat SaaS pricing models require budgeting considerations as organization scale increases.

## When to use it
- When team productivity is hampered by information scattered across dozens of disconnected SaaS tools.
- When you need a plug-and-play enterprise RAG solution without maintaining custom chunking, embedding, and vector database pipelines.
- When autonomous AI agents require audited, permissioned access to internal company knowledge.

## When not to use it
- For strict air-gapped or on-premise defense environments where cloud SaaS indexing is prohibited (prefer self-hosted solutions like [Khoj](../intake_storage/khoj.md) or custom [Weaviate](../infrastructure/weaviate.md) deployments).
- For small teams using a single unified workspace (e.g., a single Notion or Linear workspace).

## Getting started
1. Register your enterprise account on the Dashworks SaaS platform and configure Single Sign-On (SSO).
2. Authorize connectors for core SaaS apps (Slack, Google Workspace, GitHub, Jira) via OAuth or API tokens.
3. Deploy the FastMCP 3.1 tool server for local or cluster-based agent integration.

## CLI examples

### Querying Dashworks via Curl
```bash
# Execute a search query against Dashworks REST API
curl -X POST https://api.dashworks.ai/v1/search \
  -H "Authorization: Bearer ${DASHWORKS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are our FastMCP 3.1 deployment guidelines?",
    "max_results": 5,
    "include_citations": true
  }'
```

## API examples

### Python FastMCP 3.1 Server for Dashworks Enterprise Search
The following script exposes Dashworks enterprise search to AI agents as a FastMCP 3.1 tool server with strict Pydantic v2 request/response validation.

```python
import os
import requests
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dashworks_mcp_server")

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    "Dashworks-Enterprise-Knowledge-Server",
    version="3.1.0",
    description="FastMCP 3.1 server for querying enterprise knowledge graph via Dashworks"
)

# Pydantic v2 Schemas
class CitationSchema(BaseModel):
    title: str = Field(..., description="Source document or message title.")
    url: str = Field(..., description="Direct link to source document.")
    source_app: str = Field(..., alias="sourceApp", description="Origin SaaS application (e.g., slack, jira, gdrive).")

class DashworksSearchResponseSchema(BaseModel):
    query: str = Field(..., description="Original search query.")
    answer: str = Field(..., description="Synthesized natural language answer.")
    citations: List[CitationSchema] = Field(default_factory=list, description="List of ground-truth citations.")
    confidence_score: float = Field(..., alias="confidenceScore", ge=0.0, le=1.0)

class SearchQueryRequestSchema(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000, description="Natural language search question.")
    allowed_sources: Optional[List[str]] = Field(
        default_factory=lambda: ["slack", "google-drive", "github", "jira", "confluence"],
        description="Filter search results to specific authorized source applications."
    )
    max_results: int = Field(default=5, ge=1, le=20)

    @model_validator(mode="after")
    def validate_sources(self) -> "SearchQueryRequestSchema":
        valid_apps = {"slack", "google-drive", "github", "jira", "confluence", "notion", "salesforce"}
        if self.allowed_sources:
            unsupported = [app for app in self.allowed_sources if app not in valid_apps]
            if unsupported:
                raise ValueError(f"Unsupported source applications specified: {unsupported}")
        return self

@mcp.tool()
def search_internal_knowledge(
    query: str,
    sources: Optional[List[str]] = None,
    max_results: int = 5
) -> Dict[str, Any]:
    """
    Queries Dashworks knowledge graph to answer internal enterprise questions with direct citations.
    """
    api_key = os.environ.get("DASHWORKS_API_KEY")
    if not api_key:
        return {"status": "error", "message": "DASHWORKS_API_KEY environment variable is missing."}

    # Validate input via Pydantic v2
    try:
        request_obj = SearchQueryRequestSchema(
            query=query,
            allowed_sources=sources,
            max_results=max_results
        )
    except ValidationError as ve:
        return {"status": "validation_error", "errors": ve.errors()}

    url = "https://api.dashworks.ai/v1/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": request_obj.query,
        "sources": request_obj.allowed_sources,
        "max_results": request_obj.max_results,
        "include_citations": True
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        raw_data = response.json()

        # Parse and validate API response
        formatted_response = DashworksSearchResponseSchema(
            query=request_obj.query,
            answer=raw_data.get("answer", "No answer synthesized."),
            citations=[
                CitationSchema(
                    title=c.get("title", "Untitled"),
                    url=c.get("url", "#"),
                    sourceApp=c.get("app", "unknown")
                ) for c in raw_data.get("citations", [])
            ],
            confidenceScore=raw_data.get("confidence", 0.95)
        )

        return {
            "status": "success",
            "data": formatted_response.model_dump(by_alias=True, mode="json")
        }

    except requests.RequestException as re:
        logger.error(f"Dashworks API request error: {re}")
        return {"status": "api_error", "message": str(re)}
    except ValidationError as ve:
        logger.error(f"Response parsing failed: {ve}")
        return {"status": "parsing_error", "errors": ve.errors()}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Python Test Harness
```python
def test_dashworks_query():
    sample_request = {
        "query": "What are our data retention rules for customer logs in 2027?",
        "sources": ["confluence", "google-drive"],
        "max_results": 3
    }
    print("--- Simulating Dashworks Pydantic Validation ---")
    req = SearchQueryRequestSchema.model_validate(sample_request)
    print(f"Validated Query: '{req.query}'")
    print(f"Target Sources: {req.allowed_sources}")

if __name__ == "__main__":
    test_dashworks_query()
```

## Related tools / concepts
- [Glean](glean.md) — Enterprise knowledge search and AI platform competitor.
- [Hebbia](../enterprise/hebbia.md) — Neural document search engine for financial and complex legal documents.
- [Genuia / Dashworks Architecture](../enterprise/dashworks.md) — Enterprise RAG integration frameworks.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Standardized agent tool connection bus.
- [Dolt](../intake_storage/dolt.md) — Version-controlled database for tracking RAG query evaluation logs.
- [Agno](../agents/agno.md) — High-performance agent framework leveraging Dashworks tool servers.

## Sources / references
- [Dashworks Official SaaS Platform](https://www.dashworks.ai/)
- [Dashworks Developer Documentation & API Guides](https://docs.dashworks.ai/)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.org/docs/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
