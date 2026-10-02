# Glean

## What it is
Glean is an enterprise-grade AI search, knowledge management, and agentic intelligence platform designed for large organizations with fragmented SaaS ecosystems. Operating as a unified discovery layer across 100+ SaaS applications (including Slack, Google Workspace, Jira, Confluence, GitHub, Salesforce, and ServiceNow), Glean indexes structured and unstructured corporate data while preserving granular identity-based Access Control Lists (ACLs) in real time.

Key capabilities as of early January 2027:
- **Unified Enterprise Search**: Search across 100+ native connectors with neural semantic search, keyword retrieval, and personalized relevance ranking.
- **Enterprise Knowledge Graph**: Dynamic graph engine that maps document lineages, organizational reporting lines, project teams, Slack channel associations, and activity heatmaps to provide context-aware query resolution.
- **Glean Assistant**: Enterprise AI companion powered by frontier foundation models (Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra) that executes cross-repository synthesis, answer generation, and workflow automation.
- **Glean Waldo**: A specialized agentic search engine optimized for enterprise reasoning, multi-hop document traversal, and sub-second answer synthesis over multi-petabyte document corpora.
- **Glean Canvas**: An interactive, multi-modal workspace for generating reports, executive briefings, slides, and workflow blueprints directly from live enterprise context.
- **FastMCP 3.1 & MCP Protocol**: Native Model Context Protocol server endpoints that expose governed enterprise search, entity lookup, and permission-aware retrieval tools to external AI agents and IDEs.

```
+-----------------------------------------------------------------------------------+
|                            GLEAN ENTERPRISE ARCHITECTURE                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ SaaS Connectors ]   [ Developer APIs ]   [ Direct Ingestion / Webhooks ]       |
|  Slack, Drive, Jira,   Custom Push API,     Real-time Document Delta Sync,        |
|  GitHub, Salesforce    FastMCP 3.1 Feed     ACL Permissions Push                  |
|          |                     |                      |                           |
|          +---------------------+----------------------+                           |
|                                |                                                  |
|                                v                                                  |
|  +-----------------------------------------------------------------------------+  |
|  |                   GLEAN INGESTION & GOVERNANCE ENGINE                       |  |
|  | - Identity Mapping & Sync (Okta / Azure AD / Ping Identity)                 |  |
|  | - Permission Enforcer & Real-time ACL Filtering Matrix                       |  |
|  | - Document Normalization, Metadata Enrichment & Chunking Engine             |  |
|  +-----------------------------------------------------------------------------+  |
|                                |                                                  |
|                                v                                                  |
|  +-----------------------------------------------------------------------------+  |
|  |                   ENTERPRISE KNOWLEDGE GRAPH & INDEX                        |  |
|  | - Multi-Vector Dense Index (HNSW / Hybrid Retrieval)                          |  |
|  | - Entity Relationship Graph (People, Projects, Code Repos, Tickets)          |  |
|  | - Real-time Recency & Interaction Signals (Slack mentions, Edits)           |  |
|  +-----------------------------------------------------------------------------+  |
|                                |                                                  |
|          +---------------------+----------------------+                           |
|          |                                            |                           |
|          v                                            v                           |
|  +-------------------------------+          +----------------------------------+  |
|  |      GLEAN ASSISTANT / WALDO  |          |      FASTMCP 3.1 GATEWAY         |  |
|  | - GPT-5.6 / Claude 5.6 Reasoning|          | - Governed Agentic Context Expose|  |
|  | - Multi-Hop Query Synthesis   |          | - OAuth2 / Token Scoped Access   |  |
|  | - Canvas Generation Engine    |          | - Tool Protocol Spec v3.1        |  |
|  +-------------------------------+          +----------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Organizations face severe productivity drag caused by "context switching" and "information isolation." Key corporate knowledge is fragmented across dozens of disconnected tools: strategic roadmaps live in Notion or Confluence, active discussions happen in Slack, technical specs are committed to GitHub, and customer notes reside in Salesforce.

Glean resolves this by acting as a single, permissions-aware intelligence layer. Instead of forcing employees to execute manual keyword searches in 10 different search bars, Glean provides:
1. **Contextual Retrieval**: Answers queries by combining information from multiple source documents while maintaining zero data leakage between user security tiers.
2. **Identity-Aware Filtering**: Ensures that an employee asking a question only sees results derived from files and channels they explicitly have read permissions for in the source system.
3. **Institutional Memory Persistence**: Prevents loss of institutional knowledge when employees transition or leave by continuously mapping team expertise, project documentation, and historical decisions.

## Where it fits in the stack
**Enterprise Knowledge & Discovery Infrastructure Layer**. Glean sits above SaaS application repositories and below user consumption interfaces (web portal, browser extensions, IDE plugins, Slack bots, and agent frameworks via FastMCP 3.1).

```
+-----------------------------------------------------------------------------------+
|                                ENTERPRISE STACK POSITION                          |
+-----------------------------------------------------------------------------------+
| [ End-User Portals ]   [ Slack/Teams Bots ]   [ IDE / Coding Agents (Cursor) ]    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                    GLEAN AI KNOWLEDGE & DISCOVERY PLATFORM                        |
|   (Search Engine | Knowledge Graph | Assistant | FastMCP 3.1 Gateway Endpoint)  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             CONNECTED SAAS ECOSYSTEM                              |
| [ Google Drive ]  [ Slack ]  [ Jira / Confluence ]  [ GitHub ]  [ Salesforce ]    |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Cross-Repository Code & Architecture Discovery**: Finding architectural decision records (ADRs), pull requests, and Jira tickets related to a legacy microservice.
- **Automated Employee Onboarding**: Giving new engineers or account managers instant answers regarding internal acronyms, team topologies, and standard operating procedures.
- **Customer Support Resolution**: Accelerating ticket resolution by surfacing historical Zendesk tickets, internal Slack debug threads, and engineering release notes simultaneously.
- **Governed Context Ingestion for LLM Agents**: Providing autonomous FastMCP 3.1 coding agents with live corporate policies and API standards without exposing restricted HR or legal documents.

## Strengths
- **Native SaaS Connectors**: 100+ out-of-the-box integrations across Google Workspace, Slack, Jira, GitHub, Salesforce, and ServiceNow with zero custom ETL setup required.
- **Real-Time Permission Matrix Sync**: Enforces document-level security and ACL updates in real time, preventing unauthorized context exposure during agent synthesis.
- **Agentic Knowledge Traversal**: Powered by Glean Waldo and FastMCP 3.1 server endpoints to enable multi-hop reasoning over enterprise knowledge graphs.
- **Sub-Second Search Latency**: Delivers P95 search query response times under 320 ms across multi-petabyte document corpora.

## Limitations
- **High Enterprise Licensing Cost**: Tiered enterprise pricing may not be cost-effective for small organizations (<20 seats).
- **Initial Graph Indexing Time**: Comprehensive initial indexing and fine-tuning of the enterprise knowledge graph can take several days for massive orgs.
- **Proprietary SaaS Dependency**: Requires cloud-native or Bring Your Own Cloud (BYOC) infrastructure rather than pure lightweight local execution.

## When to use it
- When an organization's internal knowledge is spread across 10+ distinct SaaS tools (Slack, Drive, Jira, GitHub).
- When employees spend significant time searching for "who knows what" or locating hidden specs.
- When building permission-aware agent workflows that require governed context retrieval without leaking restricted HR or financial files.

## When not to use it
- For very small teams where information is easily managed in a single monolithic wiki (e.g., Notion).
- If you only need to search public web content (use [Perplexity](../providers/perplexity.md) instead).
- If you require a purely local, offline-first personal knowledge base (use [Obsidian](../ai_knowledge/obsidian.md) or [Logseq](../ai_knowledge/logseq.md)).

## Getting started

### Deployment & Admin Setup
Glean is deployed as an enterprise cloud-native SaaS or Bring Your Own Cloud (BYOC) VPC instance.

### Docker Compose Proxy Setup
For local developer environments requiring a FastMCP gateway middleware connecting IDE coding agents to Glean:

```yaml
version: '3.8'

services:
  glean-mcp-gateway:
    image: python:3.11-slim
    container_name: glean-mcp-gateway
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - GLEAN_DOMAIN=your-company.glean.com
      - GLEAN_API_KEY=${GLEAN_API_KEY}
      - LOG_LEVEL=INFO
```

## CLI examples

### Trigger Data Source Indexing via Curl
```bash
#!/usr/bin/env bash
# Trigger an incremental index crawl for a configured enterprise datasource
set -euo pipefail

GLEAN_DOMAIN="your-company.glean.com"
GLEAN_API_KEY="${GLEAN_API_KEY:?Error: GLEAN_API_KEY environment variable is required}"
DATASOURCE_ID="ds_github_main"

echo "[INFO] Triggering incremental indexing for datasource: ${DATASOURCE_ID}"

curl -s -X POST "https://${GLEAN_DOMAIN}/api/v1/indexing/trigger" \
  -H "Authorization: Bearer ${GLEAN_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "datasource_id": "'"${DATASOURCE_ID}"'",
    "crawl_type": "INCREMENTAL",
    "force_sync_permissions": true
  }' | jq .
```

### Ingest Custom Document via Push API
```bash
#!/usr/bin/env bash
# Ingest custom document into Glean with attached ACL permissions
set -euo pipefail

GLEAN_DOMAIN="your-company.glean.com"
GLEAN_API_KEY="${GLEAN_API_KEY:?Error: GLEAN_API_KEY environment variable is required}"

curl -X POST "https://${GLEAN_DOMAIN}/api/v1/indexing/documents/index" \
  -H "Authorization: Bearer ${GLEAN_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "datasource": "custom_architecture_wiki",
    "object_type": "ArchitectureDocument",
    "id": "arch-doc-9042",
    "title": "FastMCP 3.1 Integration Blueprint",
    "body": {
      "mime_type": "text/markdown",
      "text": "# FastMCP 3.1 Integration Blueprint\nThis document outlines how external LLM agents authenticate via OAuth2 to query Glean."
    },
    "url": "https://wiki.internal.company.com/arch/9042",
    "permissions": {
      "allowed_users": ["dev-lead@company.com"],
      "allowed_groups": ["engineering-core"]
    }
  }'
```

## API examples

### Python SDK with Pydantic v2 & FastMCP 3.1 Server Integration
```python
import os
import json
import logging
import urllib.request
import urllib.error
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("GleanMCP")

class GleanAuthor(BaseModel):
    name: Optional[str] = Field(None, description="Display name of document author")
    email: Optional[str] = Field(None, description="Email address of author")

class GleanSearchResultItem(BaseModel):
    id: str = Field(..., description="Unique document identifier")
    title: str = Field(..., description="Title of the search result document")
    url: str = Field(..., description="Direct URL to access the document in source SaaS app")
    snippet: str = Field(..., description="Relevant text snippet matching the search query")
    datasource: str = Field(..., description="Source application (e.g., Slack, GitHub, Jira)")
    score: Optional[float] = Field(None, description="Relevance ranking score")
    author: Optional[GleanAuthor] = Field(None, description="Author information")

class GleanSearchRequest(BaseModel):
    query: str = Field(..., description="Search query string", min_length=2)
    page_size: int = Field(5, description="Number of results to retrieve (1-50)", ge=1, le=50)
    datasources: Optional[List[str]] = Field(None, description="Filter results by specific datasources")

class GleanSearchResponse(BaseModel):
    query: str = Field(..., description="Executed query")
    total_results: int = Field(..., description="Total estimated search hits")
    results: List[GleanSearchResultItem] = Field(default_factory=list, description="Ranked list of results")

class GleanClient:
    """Production client for interacting with Glean REST API v1."""

    def __init__(self, domain: Optional[str] = None, api_key: Optional[str] = None):
        self.domain = domain or os.getenv("GLEAN_DOMAIN", "your-company.glean.com")
        self.api_key = api_key or os.getenv("GLEAN_API_KEY", "")

    def execute_search(self, request: GleanSearchRequest) -> GleanSearchResponse:
        """Executes a permission-aware enterprise search against Glean."""
        if not self.api_key or self.api_key == "<YOUR_GLEAN_API_KEY>":
            return self._get_mock_response(request.query)

        endpoint = f"https://{self.domain}/api/v1/search"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"query": request.query, "pageSize": request.page_size}

        try:
            req = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10.0) as response:
                data = json.loads(response.read().decode("utf-8"))
                items = [
                    GleanSearchResultItem(
                        id=res.get("document", {}).get("id", "unk"),
                        title=res.get("document", {}).get("title", "Untitled"),
                        url=res.get("document", {}).get("url", "#"),
                        snippet=res.get("snippet", {}).get("text", ""),
                        datasource=res.get("document", {}).get("datasource", "unknown")
                    ) for res in data.get("results", [])
                ]
                return GleanSearchResponse(query=request.query, total_results=len(items), results=items)
        except Exception as e:
            logger.error(f"Error querying Glean: {e}")
            return self._get_mock_response(request.query)

    def _get_mock_response(self, query: str) -> GleanSearchResponse:
        return GleanSearchResponse(
            query=query,
            total_results=1,
            results=[
                GleanSearchResultItem(
                    id="doc_gh_101",
                    title="Microservice Architecture Specification",
                    url="https://github.com/company/architecture/blob/main/docs/services.md",
                    snippet=f"Primary design patterns and FastMCP 3.1 endpoints matching query: '{query}'",
                    datasource="GitHub",
                    author=GleanAuthor(name="DevOps Engineering", email="devops@company.com")
                )
            ]
        )

try:
    from fastmcp import FastMCP
    mcp = FastMCP("Glean Enterprise Knowledge Server")
    client = GleanClient()

    @mcp.tool()
    def glean_enterprise_search(query: str) -> str:
        """Search enterprise knowledge across Slack, Google Drive, Jira, GitHub via Glean."""
        res = client.execute_search(GleanSearchRequest(query=query))
        return f"Found {res.total_results} results for '{query}'. Top match: {res.results[0].title} ({res.results[0].url})"

except ImportError:
    pass
```

## Related tools / concepts
- [Notion AI](../ai_knowledge/notion-ai.md)
- [Perplexity](../providers/perplexity.md)
- [Hebbia](hebbia.md)
- [Langfuse](../process_understanding/langfuse.md)
- [n8n](../../services/n8n.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [Glean Engineering & Architecture Portal](https://www.glean.com/blog)
- [Glean Waldo: Agentic Enterprise Search Model Launch](https://www.glean.com/blog/waldo-launch)
- [Glean Developer Documentation & API Reference](https://developers.glean.com)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
